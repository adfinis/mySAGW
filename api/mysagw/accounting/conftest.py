import re
from pathlib import Path

import pytest
from django.conf import settings
from rest_framework import status

from mysagw.utils import build_url

FILES_DIR = Path(__file__).parent.resolve() / "tests" / "files"


@pytest.fixture
def receipt_mock(requests_mock):
    caluma_data = {
        "data": {
            "node": {
                "additionalData": {
                    "edges": [
                        {
                            "node": {
                                "document": {
                                    "quittungen": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "value": [
                                                        {
                                                            "answers": {
                                                                "edges": [
                                                                    {
                                                                        "node": {
                                                                            "file": {
                                                                                "downloadUrl": "https://mysagw.local/caluma-media/download-url-png"
                                                                            }
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            "answers": {
                                                                "edges": [
                                                                    {
                                                                        "node": {
                                                                            "file": {
                                                                                "downloadUrl": "https://mysagw.local/caluma-media/download-url-pdf"
                                                                            }
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            "answers": {
                                                                "edges": [
                                                                    {
                                                                        "node": {
                                                                            "file": {
                                                                                "downloadUrl": "https://mysagw.local/caluma-media/download-url-pdf-encrypted"
                                                                            }
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {"answers": {"edges": []}},
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    "applicant_name": {
                                        "edges": [{"node": {"value": "Winston Smith"}}]
                                    },
                                    "applicant_address": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "value": "Dorfplatz 1\n8000Zürich"
                                                }
                                            }
                                        ]
                                    },
                                    "fibu": {"edges": [{"node": {"value": "2021"}}]},
                                    "iban": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "value": "CH56 0483 5012 3456 7800 9"
                                                }
                                            }
                                        ]
                                    },
                                    "bank": {
                                        "edges": [{"node": {"value": "Big Bank"}}]
                                    },
                                    "bank_town": {
                                        "edges": [{"node": {"value": "Bern"}}]
                                    },
                                }
                            }
                        }
                    ]
                },
                "main": {
                    "dossierno": {"edges": [{"node": {"value": "2021-0006"}}]},
                    "sektion": {"edges": [{"node": {"value": "section-6"}}]},
                    "vp_year": {"edges": []},
                },
                "defineAmount": {
                    "edges": [
                        {
                            "node": {
                                "document": {
                                    "total": {"edges": [{"node": {"value": 5000.0}}]}
                                }
                            }
                        },
                    ]
                },
            }
        }
    }

    requests_mock.post("http://testserver/graphql", status_code=200, json=caluma_data)

    with (FILES_DIR / "test.png").open("rb") as f:
        png = f.read()

    with (FILES_DIR / "test.pdf").open("rb") as f:
        pdf = f.read()

    with (FILES_DIR / "test_encrypted.pdf").open("rb") as f:
        pdf_encrypted = f.read()

    with (FILES_DIR / "test_cover.pdf").open("rb") as f:
        cover = f.read()

    requests_mock.get(
        "https://mysagw.local/caluma-media/download-url-png",
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
        )
    )

    requests_mock.post(
        matcher,
        status_code=status.HTTP_200_OK,
        content=cover,
        headers={"CONTENT-TYPE": "application/pdf"},
    )
