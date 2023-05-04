from datetime import datetime, timedelta

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from .settings import settings


class APIClient:
    def __init__(
        self,
        base_uri=settings.API_BASE_URI,
        token=None,
    ):
        self.base_uri = base_uri
        self.token = token

    def get_admin_token(self):
        """
        If needed fetch a (new) token from the oidc provider.

        The threshold for fetching a new token is 1 minute before expiration.
        :return: dict
        """
        thresh = datetime.now() + timedelta(minutes=1)

        if self.token is None or self.token["expires_at_dt"] <= thresh:
            client = BackendApplicationClient(client_id=settings.OIDC_ADMIN_CLIENT_ID)
            oauth = OAuth2Session(client=client)
            token = oauth.fetch_token(
                token_url=settings.OIDC_TOKEN_ENDPOINT,
                client_id=settings.OIDC_ADMIN_CLIENT_ID,
                client_secret=settings.OIDC_ADMIN_CLIENT_SECRET,
                verify=settings.API_VERIFY_SSL,
                scope="openid",
            )
            token["expires_at_dt"] = datetime.utcfromtimestamp(int(token["expires_at"]))

            self.token = token["access_token"]

        return self.token

    def get(self, url, *args, **kwargs):
        return self._request(requests.get, url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self._request(requests.post, url, *args, **kwargs)

    def _request(self, method, url, *args, **kwargs):
        token = kwargs.pop("token", self.token)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json",
        }
        resp = method(f"{self.base_uri}{url}", *args, **kwargs, headers=headers)
        resp.raise_for_status()
        return resp.json()
