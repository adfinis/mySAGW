import requests

from .settings import settings


class APIClient:
    def __init__(
        self,
        token,
        base_uri=settings.API_BASE_URI,
    ):
        self.token = token
        self.base_uri = base_uri

    def request(self, url, *args, **kwargs):
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.get(f"{self.base_uri}{url}", *args, **kwargs, headers=headers)
        resp.raise_for_status()
        return resp.json()
