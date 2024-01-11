import re

import pytest
from django.conf import settings
from rest_framework import status

from mysagw.conftest import TEST_FILES_DIR
from mysagw.utils import build_url


@pytest.fixture
def receipt_mock(requests_mock):
    def mockit(data, additional_data_available):
        def json_callback(request, context):
            if request.json()["query"].startswith("query DocumentId"):
                return (
                    {
                        "data": {
                            "node": {
                                "additionalData": {
                                    "edges": [
                                        {"node": {"document": {"id": "GLOBAL_ID"}}},
                                    ],
                                },
                            },
                        },
                    }
                    if additional_data_available
                    else {"data": {"node": {"additionalData": {"edges": []}}}}
                )
            return data

        requests_mock.post(
            "http://testserver/graphql",
            status_code=200,
            json=json_callback,
        )

        with (TEST_FILES_DIR / "small.png").open("rb") as f:
            png = f.read()

        with (TEST_FILES_DIR / "test.pdf").open("rb") as f:
            pdf = f.read()

        with (TEST_FILES_DIR / "test_encrypted.pdf").open("rb") as f:
            pdf_encrypted = f.read()

        with (TEST_FILES_DIR / "test_cover.pdf").open("rb") as f:
            cover = f.read()

        requests_mock.get(
            "https://mysagw.local/caluma-media/download-url-png",
            status_code=status.HTTP_200_OK,
            content=png,
            headers={"content-type": "image/png"},
        )

        requests_mock.get(
            "https://mysagw.local/caluma-media/download-url-png2",
            status_code=status.HTTP_200_OK,
            content=png,
            headers={"content-type": "image/png"},
        )

        requests_mock.get(
            "https://mysagw.local/caluma-media/download-url-pdf",
            status_code=status.HTTP_200_OK,
            content=pdf,
            headers={"CONTENT-TYPE": "application/pdf"},
        )

        requests_mock.get(
            "https://mysagw.local/caluma-media/download-url-pdf-encrypted",
            status_code=status.HTTP_200_OK,
            content=pdf_encrypted,
            headers={"CONTENT-TYPE": "application/pdf"},
        )

        matcher = re.compile(
            build_url(
                settings.DOCUMENT_MERGE_SERVICE_URL,
                "template",
                ".*",
                "merge",
                trailing=True,
            ),
        )

        return requests_mock.post(
            matcher,
            status_code=status.HTTP_200_OK,
            content=cover,
            headers={"CONTENT-TYPE": "application/pdf"},
        )

    return mockit
