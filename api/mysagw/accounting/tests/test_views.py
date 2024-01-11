import re

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from mysagw.accounting.tests.additional_data_caluma_response import (
    CALUMA_DATA_EMPTY,
    CALUMA_DATA_FULL,
)
from mysagw.utils import build_url


@pytest.mark.freeze_time("1970-01-01")
@pytest.mark.parametrize(
    "client,dms_failure,caluma_data,dms_mock_calls,expected_status",
    [
        ("user", False, CALUMA_DATA_FULL, 0, status.HTTP_403_FORBIDDEN),
        ("staff", False, CALUMA_DATA_FULL, 2, status.HTTP_200_OK),
        ("admin", True, CALUMA_DATA_FULL, 1, status.HTTP_500_INTERNAL_SERVER_ERROR),
        ("admin", False, CALUMA_DATA_FULL, 2, status.HTTP_200_OK),
        ("admin", False, CALUMA_DATA_EMPTY, 1, status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_get_receipts(
    db,
    client,
    dms_failure,
    caluma_data,
    dms_mock_calls,
    expected_status,
    receipt_mock,
    requests_mock,
    snapshot,
):
    dms_mock = receipt_mock(caluma_data, caluma_data == CALUMA_DATA_FULL)
    if dms_failure:
        matcher = re.compile(
            build_url(
                settings.DOCUMENT_MERGE_SERVICE_URL,
                "template",
                ".*",
                "merge",
                trailing=True,
            ),
        )
        dms_mock = requests_mock.post(
            matcher,
            status_code=status.HTTP_400_BAD_REQUEST,
            json=["something went wrong"],
            headers={"CONTENT-TYPE": "application/json"},
        )

    case_id = "e535ac0c-f3be-4a36-b2d4-1ef405ec71c8"
    url = reverse("receipts", args=[case_id])

    response = client.get(url)

    assert response.status_code == expected_status
    assert len(dms_mock.request_history) == dms_mock_calls
    for i in range(dms_mock_calls):
        snapshot.assert_match(dms_mock.request_history[i].json())

    if dms_failure:
        assert response.json() == {
            "source": "DMS",
            "status": 400,
            "errors": ["something went wrong"],
        }

    if expected_status == status.HTTP_200_OK:
        snapshot.assert_match(response.headers["content-disposition"])
