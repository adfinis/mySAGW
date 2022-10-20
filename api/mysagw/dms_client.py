import io
import json

import requests
from django.conf import settings
from requests import HTTPError

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

    def upload_template(self, slug, file, update=False, headers: dict = None):
        headers = headers if headers else {}

        url = build_url(self.url, "template", trailing=True)
        method = requests.post
        if update:
            url = build_url(url, slug, trailing=True)
            method = requests.patch

        data = {"engine": self.engine, "slug": slug}
        files = {"template": file}

        return self._request(method, url, data=data, files=files, headers=headers)

    def get_error_content(self, response):
        if response.headers["Content-Type"].startswith("application/json"):
            content = response.json()
            if isinstance(content, list):
                content = {"error": content[0]}
            content["source"] = "DMS"
            return json.dumps({"errors": content})
        elif response.headers["Content-Type"].startswith("text/plain"):
            return f"[DMS] {response.content.decode()}".encode("utf-8")
        return response.content

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

    def get_merged_document(self, context, template):
        result = io.BytesIO()
        client = DMSClient()
        try:
            resp = client.merge(
                template,
                data=context,
                convert="pdf",
            )
            result.write(resp.content)
            result.seek(0)
            return resp.status_code, resp.headers["Content-Type"], result
        except HTTPError as e:
            content = client.get_error_content(e.response)
            return e.response.status_code, e.response.headers["Content-Type"], content
