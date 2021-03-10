import logging

from django.conf import settings
from django.db.models import Q

from mysagw.identity.models import Identity

logger = logging.getLogger(__name__)


class BaseUser:  # pragma: no cover
    def __init__(self):
        self.username = None
        self.groups = []
        self.group = None
        self.token = None
        self.claims = {}
        self.is_authenticated = False

    def __str__(self):
        raise NotImplementedError

    @property
    def is_admin(self):
        return settings.ADMIN_GROUP in self.groups

    @property
    def is_staff(self):
        return self.is_admin or settings.STAFF_GROUP in self.groups


class OIDCUser(BaseUser):
    def __init__(self, token: str, claims: dict):
        super().__init__()

        self.claims = claims
        self.id = self.claims[settings.OIDC_ID_CLAIM]
        self.username = self.claims[settings.OIDC_EMAIL_CLAIM]
        self.groups = self.claims[settings.OIDC_GROUPS_CLAIM]
        self.group = self.groups[0] if self.groups else None
        self.token = token
        self.is_authenticated = True
        self.identity = self._get_or_create_identity()

    def _get_or_create_identity(self):
        try:
            identity = Identity.objects.get(Q(idp_id=self.id) | Q(email=self.username))
            # we only want to save if necessary in order to prevent adding historical
            # records on every request
            if identity.idp_id != self.id or identity.email != self.username:
                identity.idp_id = self.id
                identity.email = self.username
                identity.modified_by_user = self.username
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
                email=self.username,
                modified_by_user=self.username,
                created_by_user=self.username,
            )
        return identity

    def __str__(self):
        return self.username
