import base64
import functools
import hashlib
import warnings
from collections import namedtuple

import requests
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.OIDC_EMAIL_CLAIM = self.get_settings("OIDC_EMAIL_CLAIM")
        self.OIDC_OP_INTROSPECT_ENDPOINT = self.get_settings(
            "OIDC_OP_INTROSPECT_ENDPOINT"
        )
        self.OIDC_BEARER_TOKEN_REVALIDATION_TIME = self.get_settings(
            "OIDC_BEARER_TOKEN_REVALIDATION_TIME"
        )
        self.OIDC_VERIFY_SSL = self.get_settings("OIDC_VERIFY_SSL", True)

    def get_introspection(self, access_token, id_token, payload):
        """Return user details dictionary."""

        basic = base64.b64encode(
            f"{self.OIDC_RP_CLIENT_ID}:{self.OIDC_RP_CLIENT_SECRET}".encode("utf-8")
        ).decode()
        headers = {
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.post(
            self.OIDC_OP_INTROSPECT_ENDPOINT,
            verify=self.OIDC_VERIFY_SSL,
            headers=headers,
            data={"token": access_token},
        )
        response.raise_for_status()
        return response.json()

    def get_userinfo_or_introspection(self, access_token) -> dict:
        try:
            claims = self.cached_request(
                self.get_userinfo, access_token, "auth.userinfo"
            )
        except requests.HTTPError as e:
            if not (
                e.response.status_code in [401, 403]
                and self.OIDC_OP_INTROSPECT_ENDPOINT
            ):
                raise e

            # check introspection if userinfo fails (confidental client)
            claims = self.cached_request(
                self.get_introspection, access_token, "auth.introspection"
            )
            if "client_id" not in claims:
                raise SuspiciousOperation("client_id not present in introspection")

        return claims

    def get_or_create_user(self, access_token, id_token, payload):
        """Verify claims and return user, otherwise raise an Exception."""

        claims = self.get_userinfo_or_introspection(access_token)

        for claim in [
            settings.OIDC_ID_CLAIM,
            settings.OIDC_EMAIL_CLAIM,
            settings.OIDC_GROUPS_CLAIM,
        ]:
            if claim not in claims:
                raise SuspiciousOperation(f'Couldn\'t find "{claim}" claim')

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

    def cached_request(self, method, token, cache_prefix):
        token_hash = hashlib.sha256(force_bytes(token)).hexdigest()

        func = functools.partial(method, token, None, None)

        with warnings.catch_warnings():
            if settings.DEBUG:  # pragma: no cover
                warnings.simplefilter("ignore", InsecureRequestWarning)
            return cache.get_or_set(
                f"{cache_prefix}.{token_hash}",
                func,
                timeout=self.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
            )
