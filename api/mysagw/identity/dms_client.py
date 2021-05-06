import requests
from django.conf import settings

from mysagw.utils import build_url


class DMSClient:
    def __init__(
        self,
        url: str = settings.DOCUMENT_MERGE_SERVICE_URL,
        engine: str = settings.DOCUMENT_MERGE_SERVICE_ENGINE,
    ):
        self.url = url
        self.engine = engine

    def _request(self, method, *args, **kwargs):
        response = method(*args, **kwargs)
        response.raise_for_status()
        return response

    def merge(
        self,
        template_slug: str,
        data: dict,
        convert: str = None,
        headers: dict = None,
    ):
        headers = headers if headers else {}

        url = build_url(self.url, "template", template_slug, "merge", trailing=True)

        return self._request(
            requests.post, url, headers=headers, json={"data": data, "convert": convert}
        )
