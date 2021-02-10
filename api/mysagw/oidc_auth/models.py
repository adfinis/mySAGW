from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from mysagw.identity.models import Identity


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
    def _validate_claims(self, claims):
        for claim in [
            settings.OIDC_ID_CLAIM,
            settings.OIDC_EMAIL_CLAIM,
            settings.OIDC_GROUPS_CLAIM,
        ]:
            if claim not in claims:
                raise SuspiciousOperation(f'Couldn\'t find "{claim}" claim')

    def __init__(self, token: str, claims: dict):
        super().__init__()
        self._validate_claims(claims)

        self.claims = claims
        self.id = self.claims[settings.OIDC_ID_CLAIM]
        self.username = self.claims[settings.OIDC_EMAIL_CLAIM]
        self.groups = self.claims[settings.OIDC_GROUPS_CLAIM]
        self.group = self.groups[0] if self.groups else None
        self.token = token
        self.is_authenticated = True

        self.identity = None
        for matcher in [{"idp_id": self.id}, {"email": self.username}]:
            try:
                self.identity = Identity.objects.get(**matcher)
                self.identity.email = self.username
                self.identity.idp_id = self.id
            except Identity.DoesNotExist:
                continue

        if not self.identity:
            self.identity = Identity.objects.create(
                idp_id=self.id,
                email=self.username,
            )
        self.identity.save()

    def __str__(self):
        return self.username
