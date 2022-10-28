import re

import pytest
from django.conf import settings
from rest_framework import status

from mysagw.case.tests.application_caluma_response import CALUMA_DATA
from mysagw.utils import build_url


@pytest.fixture
def dms_mock(requests_mock):
    matcher = re.compile(
        build_url(
            settings.DOCUMENT_MERGE_SERVICE_URL,
            "template",
            ".*",
            "merge",
            trailing=True,
        )
    )

    return requests_mock.post(
        matcher,
        status_code=status.HTTP_200_OK,
        content=b"foo",
        headers={"CONTENT-TYPE": "application/pdf"},
    )


@pytest.fixture
def acknowledgement_mock(requests_mock):
    def mockit():
        caluma_data = {
            "data": {
                "node": {
                    "main": {
                        "dossier_nr": {"edges": [{"node": {"value": "2022-0001"}}]}
                    },
                    "submit": {
                        "edges": [
                            {
                                "node": {
                                    "closedByUser": "e5dabdd0-bafb-4b75-82d2-ccf9295b623b"
                                }
                            }
                        ]
                    },
                    "revise": {
                        "edges": [
                            {
                                "node": {
                                    "closedByUser": "e5dabdd0-bafb-4b75-82d2-ccf9295b623b",
                                    "closedAt": "1970-01-02T06:04:35.345403+00:00",
                                }
                            },
                            {
                                "node": {
                                    "closedByUser": "e5dabdd0-bafb-4b75-82d2-ccf9295b623b",
                                    "closedAt": "1970-01-01T05:58:47.177316+00:00",
                                }
                            },
                        ]
                    },
                }
            }
        }

        requests_mock.post(
            "http://testserver/graphql", status_code=200, json=caluma_data
        )

    return mockit


@pytest.fixture
def credit_approval_mock(requests_mock):
    def mockit():
        caluma_data = {
            "data": {
                "node": {
                    "main": {
                        "dossier_nr": {"edges": [{"node": {"value": "2022-0001"}}]}
                    },
                    "decisionAndCredit": {
                        "edges": [
                            {
                                "node": {
                                    "document": {
                                        "credit": {"edges": [{"node": {"value": "23"}}]}
                                    }
                                }
                            }
                        ]
                    },
                    "submit": {
                        "edges": [
                            {
                                "node": {
                                    "closedByUser": "e5dabdd0-bafb-4b75-82d2-ccf9295b623b"
                                }
                            }
                        ]
                    },
                    "revise": {"edges": []},
                }
            }
        }

        requests_mock.post(
            "http://testserver/graphql", status_code=200, json=caluma_data
        )

    return mockit


@pytest.fixture
def application_mock(requests_mock):
    requests_mock.post("http://testserver/graphql", status_code=200, json=CALUMA_DATA)
