import re

import pytest
from django.conf import settings
from rest_framework import status

from mysagw.conftest import TEST_FILES_DIR
from mysagw.utils import build_url


@pytest.fixture
def dms_cover_mock(requests_mock):
    def mockit(failure=False):
        matcher = re.compile(
            build_url(
                settings.DOCUMENT_MERGE_SERVICE_URL,
                "template",
                ".*",
                "merge",
                trailing=True,
            ),
        )

        mock_args = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "json": ["something went wrong"],
            "headers": {"CONTENT-TYPE": "application/json"},
        }

        if not failure:
            with (TEST_FILES_DIR / "test_cover.pdf").open("rb") as f:
                cover = f.read()

            mock_args["status_code"] = status.HTTP_200_OK
            del mock_args["json"]
            mock_args["content"] = cover
            mock_args["headers"] = {"CONTENT-TYPE": "application/pdf"}

        return requests_mock.post(matcher, **mock_args)

    return mockit
