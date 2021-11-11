import re

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from mysagw.utils import build_url


@pytest.mark.parametrize(
    "client,dms_failure,missing_receipts,expected_status",
    [
        ("user", False, False, status.HTTP_403_FORBIDDEN),
        ("staff", False, False, status.HTTP_200_OK),
        ("admin", False, False, status.HTTP_200_OK),
        ("admin", True, False, status.HTTP_400_BAD_REQUEST),
        ("admin", False, True, status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_get_receipts(
    db,
    client,
    dms_failure,
    missing_receipts,
    expected_status,
    receipt_mock,
    requests_mock,
    snapshot,
):
    if dms_failure:
        matcher = re.compile(
            build_url(
                settings.DOCUMENT_MERGE_SERVICE_URL,
                "template",
                ".*",
                "merge",
                trailing=True,
            )
        )
        requests_mock.post(
            matcher,
            status_code=status.HTTP_400_BAD_REQUEST,
            json={"error": "something went wrong"},
            headers={"CONTENT-TYPE": "application/json"},
        )
    elif missing_receipts:
        requests_mock.post(
            "http://testserver/graphql", status_code=200, json={"data": {}}
        )

    case_id = "e535ac0c-f3be-4a36-b2d4-1ef405ec71c8"
    url = reverse("receipts-detail", args=[case_id])

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    snapshot.assert_match(response.getvalue())
