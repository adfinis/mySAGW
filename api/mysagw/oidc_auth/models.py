import logging

from django.conf import settings
from django.db.models import Q

from mysagw.identity.models import Identity

logger = logging.getLogger(__name__)


class BaseUser:  # pragma: no cover
    def __init__(self):
        self.email = None
        self.groups = []
        self.group = None
        self.token = None
        self.claims = {}
        self.is_authenticated = False

    def __str__(self):
        raise NotImplementedError

    @property
    def is_admin(self):
        return (
            self.claims.get(settings.OIDC_CLIENT_GRANT_USERNAME_CLAIM)
            == settings.OIDC_RP_CLIENT_USERNAME
            or settings.ADMIN_GROUP in self.groups
        )

    @property
    def is_staff(self):
        return self.is_admin or settings.STAFF_GROUP in self.groups

    @property
    def is_monitoring_member(self):
        return (
            self.is_staff
            or self.claims.get(settings.OIDC_CLIENT_GRANT_USERNAME_CLAIM)
            == settings.OIDC_MONITORING_CLIENT_USERNAME
        )


class OIDCUser(BaseUser):
    def __init__(self, token: str, claims: dict):
        super().__init__()

        self.claims = claims
        self.id = self.claims[settings.OIDC_ID_CLAIM]
        self.email = self.claims.get(settings.OIDC_EMAIL_CLAIM)
        self.groups = self.claims.get(settings.OIDC_GROUPS_CLAIM, [])
        self.group = self.groups[0] if self.groups else None
        self.token = token
        self.is_authenticated = True
        self.identity = self._get_or_create_identity()

    def _get_or_create_identity(self):
        if self.claims.get(settings.OIDC_CLIENT_GRANT_USERNAME_CLAIM) in [
            settings.OIDC_RP_CLIENT_USERNAME,
            settings.OIDC_MONITORING_CLIENT_USERNAME,
        ]:
            return None
        try:
            identity = Identity.objects.get(
                Q(idp_id=self.id) | Q(email__iexact=self.email)
            )
            # we only want to save if necessary in order to prevent adding historical
            # records on every request
            if identity.idp_id != self.id or identity.email != self.email:
                identity.idp_id = self.id
                identity.email = self.email
                identity.modified_by_user = self.id
                identity.save()
        except Identity.MultipleObjectsReturned:
            # TODO: trigger notification for staff members or admins
            logger.warning(
                "Found one Identity with same idp_id and one with same email. Matching"
                " on idp_id."
            )
            identity = Identity.objects.get(idp_id=self.id)
        except Identity.DoesNotExist:
            identity = Identity.objects.create(
                idp_id=self.id,
                email=self.email,
                modified_by_user=self.id,
                created_by_user=self.id,
            )
        return identity

    def __str__(self):
        return f"{self.email} - {self.id}"
