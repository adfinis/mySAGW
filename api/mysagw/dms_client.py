import json

import requests
from django.conf import settings
from django.http import HttpResponse
from requests import HTTPError
from rest_framework import status

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
        client = DMSClient()
        try:
            resp = client.merge(
                template,
                data=context,
                convert="pdf",
            )
            return resp
        except HTTPError as e:
            return e.response


def get_dms_error_response(response):
    content = {
        "source": "DMS",
        "status": response.status_code,
    }
    if response.headers["Content-Type"].startswith("application/json"):
        content["errors"] = response.json()
    else:
        content["errors"] = response.content.decode("utf-8")
    return HttpResponse(
        json.dumps(content),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content_type="application/json",
    )
