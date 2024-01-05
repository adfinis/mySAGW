CALUMA_DATA_FULL = {
    "data": {
        "node": {
            "additionalData": {
                "edges": [
                    {
                        "node": {
                            "document": {
                                "answers": {
                                    "edges": [
                                        {
                                            "node": {
                                                "question": {
                                                    "slug": "additional-data-quittungen",
                                                },
                                                "tableValue": [
                                                    {
                                                        "answers": {
                                                            "edges": [
                                                                {
                                                                    "node": {
                                                                        "question": {
                                                                            "slug": "additional-data-row-quittung",
                                                                        },
                                                                        "filesValue": [
                                                                            {
                                                                                "downloadUrl": "https://mysagw.local/caluma-media/download-url-png",
                                                                                "metadata": {
                                                                                    "content_type": "image/png",
                                                                                },
                                                                                "name": "File 1",
                                                                            },
                                                                            {
                                                                                "downloadUrl": "https://mysagw.local/caluma-media/download-url-png2",
                                                                                "metadata": {
                                                                                    "content_type": "image/png",
                                                                                },
                                                                                "name": "File 2",
                                                                            },
                                                                            {
                                                                                "downloadUrl": "https://mysagw.local/caluma-media/song.mp3",
                                                                                "metadata": {
                                                                                    "content_type": "audio/mpeg",
                                                                                },
                                                                                "name": "File 3",
                                                                            },
                                                                        ],
                                                                    },
                                                                },
                                                            ],
                                                        },
                                                    },
                                                    {
                                                        "answers": {
                                                            "edges": [
                                                                {
                                                                    "node": {
                                                                        "filesValue": [
                                                                            {
                                                                                "downloadUrl": "https://mysagw.local/caluma-media/download-url-pdf",
                                                                                "metadata": {
                                                                                    "content_type": "application/pdf",
                                                                                },
                                                                                "name": "File 4",
                                                                            },
                                                                        ],
                                                                        "question": {
                                                                            "slug": "additional-data-row-quittung",
                                                                        },
                                                                    },
                                                                },
                                                            ],
                                                        },
                                                    },
                                                    {
                                                        "answers": {
                                                            "edges": [
                                                                {
                                                                    "node": {
                                                                        "filesValue": [
                                                                            {
                                                                                "downloadUrl": "https://mysagw.local/caluma-media/download-url-pdf-encrypted",
                                                                                "metadata": {
                                                                                    "content_type": "application/pdf",
                                                                                },
                                                                                "name": "File 5",
                                                                            },
                                                                        ],
                                                                        "question": {
                                                                            "slug": "additional-data-row-quittung",
                                                                        },
                                                                    },
                                                                },
                                                            ],
                                                        },
                                                    },
                                                ],
                                            },
                                        },
                                        {
                                            "node": {
                                                "question": {
                                                    "slug": "additional-data-zahlung",
                                                },
                                                "stringValue": "additional-data-zahlung-1",
                                            },
                                        },
                                    ],
                                },
                                "applicant_address": {
                                    "edges": [{"node": {"value": "Teststrasse 23"}}],
                                },
                                "applicant_city": {"edges": []},
                                "applicant_land": {"edges": []},
                                "applicant_name": {
                                    "edges": [{"node": {"value": "Winston Smith"}}],
                                },
                                "applicant_postcode": {"edges": []},
                                "bank": {"edges": []},
                                "bank_town": {"edges": []},
                                "form": {
                                    "name": "Weitere Daten",
                                    "questions": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "__typename": "ChoiceQuestion",
                                                    "choiceOptions": {
                                                        "edges": [
                                                            {
                                                                "node": {
                                                                    "label": "Option 1",
                                                                    "slug": "additional-data-zahlung-1",
                                                                },
                                                            },
                                                            {
                                                                "node": {
                                                                    "label": "Option 2",
                                                                    "slug": "additional-data-zahlung-2",
                                                                },
                                                            },
                                                        ],
                                                    },
                                                    "infoText": "",
                                                    "label": "Zahlung",
                                                    "meta": {
                                                        "widgetOverride": "cf-field/input/powerselect",
                                                    },
                                                    "slug": "additional-data-zahlung",
                                                },
                                            },
                                            {
                                                "node": {
                                                    "__typename": "TextQuestion",
                                                    "infoText": "",
                                                    "label": "Land",
                                                    "meta": {},
                                                    "slug": "additional-data-land",
                                                },
                                            },
                                            {
                                                "node": {
                                                    "__typename": "TableQuestion",
                                                    "infoText": "",
                                                    "label": "Quittungen",
                                                    "meta": {},
                                                    "rowForm": {
                                                        "name": "Quittungen",
                                                        "questions": {
                                                            "edges": [
                                                                {
                                                                    "node": {
                                                                        "__typename": "FilesQuestion",
                                                                        "infoText": "",
                                                                        "label": "Quittungen",
                                                                        "meta": {},
                                                                        "slug": "additional-data-row-quittung",
                                                                    },
                                                                },
                                                            ],
                                                        },
                                                        "slug": "quittungen",
                                                    },
                                                    "slug": "additional-data-quittungen",
                                                },
                                            },
                                            {
                                                "node": {
                                                    "__typename": "TextareaQuestion",
                                                    "infoText": "",
                                                    "label": "Bemerkungen",
                                                    "meta": {},
                                                    "slug": "additional-data-bemerkungen",
                                                },
                                            },
                                        ],
                                    },
                                    "slug": "additional-data-form",
                                },
                                "iban": {"edges": []},
                                "zahlungszweck": {"edges": []},
                            },
                        },
                    },
                ],
            },
            "advanceCredits": {
                "edges": [
                    {
                        "node": {
                            "document": {
                                "vorschussbetrag": {
                                    "edges": [{"node": {"value": 500.0}}],
                                },
                                "vorschussdatum": {
                                    "edges": [{"node": {"value": "2024-01-19"}}],
                                },
                            },
                        },
                    },
                ],
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
                                                                    "label": "Option 1",
                                                                    "slug": "circ-kontonummer-1",
                                                                },
                                                            },
                                                            {
                                                                "node": {
                                                                    "label": "Option 2",
                                                                    "slug": "circ-kontonummer-2",
                                                                },
                                                            },
                                                            {
                                                                "node": {
                                                                    "label": "Option 3",
                                                                    "slug": "circ-kontonummer-3",
                                                                },
                                                            },
                                                        ],
                                                    },
                                                },
                                                "value": "circ-kontonummer-1",
                                            },
                                        },
                                    ],
                                },
                            },
                        },
                    },
                ],
            },
            "defineAmount": {
                "edges": [
                    {
                        "node": {
                            "document": {
                                "total": {"edges": [{"node": {"value": 500.0}}]},
                            },
                        },
                    },
                ],
            },
            "main": {
                "form": {"name": "Application"},
                "dossierno": {"edges": [{"node": {"value": "2024-0001"}}]},
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
                                                },
                                            },
                                            {
                                                "node": {
                                                    "label": "Bar institute",
                                                    "slug": "bar-institute",
                                                },
                                            },
                                        ],
                                    },
                                },
                            },
                        },
                    ],
                },
                "sektion": {"edges": [{"node": {"value": "section-6"}}]},
                "vp_year": {"edges": []},
            },
        },
    },
}

CALUMA_DATA_EMPTY = {
    "data": {
        "node": {
            "additionalData": {"edges": []},
            "advanceCredits": {"edges": []},
            "decisionCredit": {"edges": []},
            "defineAmount": {"edges": []},
            "main": {
                "form": {"name": "Application"},
                "dossierno": {"edges": [{"node": {"value": "2024-0001"}}]},
                "mitgliedinstitution": {"edges": []},
                "sektion": {"edges": []},
                "vp_year": {"edges": []},
            },
        },
    },
}
