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


class AnonymousUser(BaseUser):
    def __str__(self):
        return "AnonymousUser"


class OIDCUser(BaseUser):
    def __init__(self, token: str, claims: dict):
        super().__init__()

        self.claims = claims
        try:
            self.username = self.claims[settings.OIDC_USERNAME_CLAIM]
        except KeyError:
            raise SuspiciousOperation("Couldn't find username claim")
        self.groups = self.claims.get(settings.OIDC_GROUPS_CLAIM)
        self.group = self.groups[0] if self.groups else None
        self.token = token
        self.is_authenticated = True
        self.identity, _ = Identity.objects.get_or_create(idp_id=self.username)

    def __str__(self):
        return self.username
