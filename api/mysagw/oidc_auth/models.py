import logging

from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

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
    SALUTATION_MAP = {
        "Mr.": Identity.SALUTATION_MR,
        "Mrs.": Identity.SALUTATION_MRS,
        "neutral": Identity.SALUTATION_NEUTRAL,
    }
    TITLE_MAP = {
        "Dr.": Identity.TITLE_DR,
        "Prof.": Identity.TITLE_PROF,
        "Prof. Dr.": Identity.TITLE_PROF_DR,
        "PD Dr.": Identity.TITLE_PD_DR,
        "": Identity.TITLE_NONE,
    }

    def __init__(self, token: str, claims: dict):
        super().__init__()

        self.claims = claims
        self.id = self.claims[settings.OIDC_ID_CLAIM]
        self.email = self.claims.get(settings.OIDC_EMAIL_CLAIM)
        self.first_name = self.claims.get(settings.OIDC_FIRST_NAME_CLAIM)
        self.last_name = self.claims.get(settings.OIDC_LAST_NAME_CLAIM)
        salutation = self.claims.get(settings.OIDC_SALUTATION_CLAIM, "neutral")
        self.salutation = self.SALUTATION_MAP[salutation]

        title = self.claims.get(settings.OIDC_TITLE_CLAIM, "")
        self.title = self.TITLE_MAP[title]
        self.groups = self.claims.get(settings.OIDC_GROUPS_CLAIM, [])
        self.group = self.groups[0] if self.groups else None
        self.token = token
        self.is_authenticated = True
        self.identity = self._update_or_create_identity()

    def _update_or_create_identity(self):
        """
        Update or create Identity.

        Analogous to QuerySet.get_or_create(), in order to handle race conditions as
        gracefully as possible.
        """
        if self.claims.get(settings.OIDC_CLIENT_GRANT_USERNAME_CLAIM) in [
            settings.OIDC_RP_CLIENT_USERNAME,
            settings.OIDC_MONITORING_CLIENT_USERNAME,
        ]:
            return None
        if Identity.objects.filter(
            is_organisation=True, email__iexact=self.email
        ).exists():
            msg = "Can't create Identity, because there is already an organisation with this email address."
            raise ValidationError(msg)
        try:
            identity = Identity.objects.filter(is_organisation=False).get(
                Q(idp_id=self.id) | Q(email__iexact=self.email),
            )
            # we only want to save if necessary in order to prevent adding historical
            # records on every request
            if (
                identity.idp_id != self.id
                or (identity.email and identity.email.lower()) != self.email.lower()
            ):
                identity.idp_id = self.id
                identity.email = self.email
                identity.modified_by_user = self.id
                identity.save()
        except Identity.MultipleObjectsReturned:
            # TODO: trigger notification for staff members or admins
            logger.warning(
                "Found one Identity with same idp_id and one with same email. Matching"
                " on idp_id.",
            )
            return Identity.objects.get(idp_id=self.id)
        except Identity.DoesNotExist:
            try:
                with transaction.atomic(using=Identity.objects.db):
                    return Identity.objects.create(
                        idp_id=self.id,
                        email=self.email,
                        first_name=self.first_name,
                        last_name=self.last_name,
                        salutation=self.salutation,
                        title=self.title,
                        modified_by_user=self.id,
                        created_by_user=self.id,
                    )
            except IntegrityError:  # pragma: no cover
                # race condition happened
                try:
                    return Identity.objects.get(idp_id=self.id)
                except Identity.DoesNotExist:
                    pass
                raise
        else:
            return identity

    def __str__(self):
        return f"{self.email} - {self.id}"
