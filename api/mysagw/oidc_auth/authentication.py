import functools
import hashlib
import warnings
from collections import namedtuple

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import SuspiciousOperation
from django.utils.encoding import force_bytes
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from simple_history.models import HistoricalRecords
from urllib3.exceptions import InsecureRequestWarning

from .models import OIDCUser


class MySAGWAuthenticationBackend(OIDCAuthenticationBackend):
    _HistoricalRequestUser = namedtuple("User", ["id"])

    def verify_claims(self, claims):
        # claims for human users
        claims_to_verify = [
            settings.OIDC_ID_CLAIM,
            settings.OIDC_EMAIL_CLAIM,
            settings.OIDC_GROUPS_CLAIM,
        ]

        # claims for application clients
        if claims.get(settings.OIDC_CLIENT_GRANT_USERNAME_CLAIM) in [
            settings.OIDC_RP_CLIENT_USERNAME,
            settings.OIDC_MONITORING_CLIENT_USERNAME,
        ]:
            claims_to_verify = [
                settings.OIDC_ID_CLAIM,
            ]

        for claim in claims_to_verify:
            if claim not in claims:
                raise SuspiciousOperation(f'Couldn\'t find "{claim}" claim')

    def get_or_create_user(self, access_token, id_token, payload):
        """Verify claims and return user, otherwise raise an Exception."""

        claims = self.cached_request(access_token, id_token, payload)

        self.verify_claims(claims)

        # simple history reads the user_id from the current user from the request. But
        # for the user to be available in the request, authentication needs to be
        # completed. That's why we just add a namedtuple to the request, so the correct
        # user_id will be set on the historical record when creating/updating the
        # identity
        HistoricalRecords.thread.request.user = self._HistoricalRequestUser(
            claims[settings.OIDC_ID_CLAIM]
        )

        user = OIDCUser(access_token, claims)

        return user

    def cached_request(self, access_token, id_token, payload):
        token_hash = hashlib.sha256(force_bytes(access_token)).hexdigest()

        func = functools.partial(self.get_userinfo, access_token, id_token, payload)

        with warnings.catch_warnings():
            if settings.DEBUG:  # pragma: no cover
                warnings.simplefilter("ignore", InsecureRequestWarning)
            return cache.get_or_set(
                f"auth.userinfo.{token_hash}",
                func,
                timeout=settings.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
            )
