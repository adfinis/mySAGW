import re

import pytest
from django.conf import settings
from rest_framework import status

from mysagw.conftest import TEST_FILES_DIR
from mysagw.utils import build_url


@pytest.fixture
def receipt_mock(requests_mock):
    caluma_data = {
        "data": {
            "node": {
                "document": {"form": {"name": "Foo form"}},
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
                                                                            "value": [
                                                                                {
                                                                                    "downloadUrl": "https://mysagw.local/caluma-media/download-url-png",
                                                                                    "metadata": {
                                                                                        "content_type": "image/png",
                                                                                    },
                                                                                },
                                                                                {
                                                                                    "downloadUrl": "https://mysagw.local/caluma-media/download-url-png2",
                                                                                    "metadata": {
                                                                                        "content_type": "image/png",
                                                                                    },
                                                                                },
                                                                                {
                                                                                    "downloadUrl": "https://mysagw.local/caluma-media/song.mp3",
                                                                                    "metadata": {
                                                                                        "content_type": "audio/mpeg",
                                                                                    },
                                                                                },
                                                                            ]
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
                                                                            "value": [
                                                                                {
                                                                                    "downloadUrl": "https://mysagw.local/caluma-media/download-url-pdf",
                                                                                    "metadata": {
                                                                                        "content_type": "application/pdf",
                                                                                    },
                                                                                }
                                                                            ]
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
                                                                            "value": [
                                                                                {
                                                                                    "downloadUrl": "https://mysagw.local/caluma-media/download-url-pdf-encrypted",
                                                                                    "metadata": {
                                                                                        "content_type": "application/pdf",
                                                                                    },
                                                                                }
                                                                            ]
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
                                        "edges": [{"node": {"value": "Dorfplatz 1"}}]
                                    },
                                    "applicant_postcode": {
                                        "edges": [{"node": {"value": "8000"}}]
                                    },
                                    "applicant_city": {
                                        "edges": [{"node": {"value": "Zürich"}}]
                                    },
                                    "applicant_land": {
                                        "edges": [{"node": {"value": "Schweiz"}}]
                                    },
                                    "fibu": {"edges": [{"node": {"value": "2021"}}]},
                                    "zahlungszweck": {
                                        "edges": [{"node": {"value": "Foo Bar"}}]
                                    },
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
                    "mitgliedinstitution": {
                        "edges": [
                            {
                                "node": {
                                    "value": "foo-institute",
                                    "question": {
                                        "options": {
                                            "edges": [
                                                {
                                                    "node": {
                                                        "label": "Foo institute",
                                                        "slug": "foo-institute",
                                                    }
                                                },
                                                {
                                                    "node": {
                                                        "label": "Bar institute",
                                                        "slug": "bar-institute",
                                                    }
                                                },
                                            ]
                                        }
                                    },
                                }
                            }
                        ]
                    },
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
                "decisionCredit": {
                    "edges": [
                        {
                            "node": {
                                "document": {
                                    "circKontonummer": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "question": {
                                                        "options": {
                                                            "edges": [
                                                                {
                                                                    "node": {
                                                                        "label": "23 konto1",
                                                                        "slug": "konto1",
                                                                    }
                                                                },
                                                                {
                                                                    "node": {
                                                                        "label": "24 konto2",
                                                                        "slug": "konto2",
                                                                    }
                                                                },
                                                            ]
                                                        }
                                                    },
                                                    "value": "konto1",
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    ]
                },
                "advanceCredits": {
                    "edges": [
                        {
                            "node": {
                                "document": {
                                    "vorschussbetrag": {
                                        "edges": [{"node": {"value": 5000}}]
                                    },
                                    "vorschussdatum": {
                                        "edges": [{"node": {"value": "2023-05-04"}}]
                                    },
                                }
                            }
                        }
                    ]
                },
            }
        }
    }

    requests_mock.post("http://testserver/graphql", status_code=200, json=caluma_data)

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
        )
    )

    return requests_mock.post(
        matcher,
        status_code=status.HTTP_200_OK,
        content=cover,
        headers={"CONTENT-TYPE": "application/pdf"},
    )
