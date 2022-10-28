# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Äthiopien""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Äthiopien""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Äthiopien""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Äthiopien""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Äthiopien""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Äthiopien""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Ethiopia""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Ethiopia""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Ethiopia""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Ethiopia""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Ethiopia""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Ethiopia""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Éthiopie""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Éthiopie""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Éthiopie""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Éthiopie""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Éthiopie""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
8190 Roger View
35543 Stewartbury
Éthiopie""",
            "email": "gallagherheather@example.com",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "tests_download_application[admin-e5dabdd0-bafb-4b75-82d2-ccf9295b623b] 1"
] = {
    "convert": "pdf",
    "data": {
        "dossier_nr": "2022-0001",
        "name": "Test Download",
        "questions": {
            "test-top-level": {
                "info_text": "Eine Info.",
                "label": "Test top level",
                "type": "TextQuestion",
                "value": "some value",
            }
        },
        "sub_forms": {
            "test-download-types": {
                "name": "Test Download Types",
                "questions": {
                    "test-calc": {
                        "info_text": None,
                        "label": "Test calc",
                        "type": "CalculatedFloatQuestion",
                        "value": 46.5,
                    },
                    "test-choice": {
                        "info_text": None,
                        "label": "Test choice",
                        "options": [
                            ["test-choice-choice-1", "choice 1"],
                            ["test-choice-choice-2", "choice 2"],
                            ["test-choice-choice-3", "choice 3"],
                        ],
                        "type": "ChoiceQuestion",
                        "value": "test-choice-choice-2",
                    },
                    "test-date": {
                        "info_text": "Bitte geben Sie das Datum ein.",
                        "label": "Test date",
                        "type": "DateQuestion",
                        "value": "2022-10-14",
                    },
                    "test-file": {
                        "info_text": None,
                        "label": "Test file",
                        "type": "FilesQuestion",
                        "value": ["test.pdf"],
                    },
                    "test-float": {
                        "info_text": None,
                        "label": "Test float",
                        "type": "FloatQuestion",
                        "value": 23.5,
                    },
                    "test-int": {
                        "info_text": None,
                        "label": "Test int",
                        "type": "IntegerQuestion",
                        "value": 23,
                    },
                    "test-many-choices": {
                        "info_text": None,
                        "label": "Test Many Choices",
                        "type": "TextQuestion",
                        "value": "choice 7",
                    },
                    "test-many-multiple-choices": {
                        "info_text": None,
                        "label": "Test Many Multiple Choices",
                        "options": [
                            ["test-many-multiple-choices-choice-3", "choice 3"],
                            ["test-many-multiple-choices-choice-6", "choice 6"],
                            ["test-many-multiple-choices-choice-11", "choice 11"],
                        ],
                        "type": "MultipleChoiceQuestion",
                        "value": [
                            "test-many-multiple-choices-choice-3",
                            "test-many-multiple-choices-choice-6",
                            "test-many-multiple-choices-choice-11",
                        ],
                    },
                    "test-multiple-choice": {
                        "info_text": None,
                        "label": "Test multiple choice",
                        "options": [
                            ["test-multiple-choice-choice-1", "choice 1"],
                            ["test-multiple-choice-choice-2", "choice 2"],
                            ["test-multiple-choice-choice-3", "choice 3"],
                        ],
                        "type": "MultipleChoiceQuestion",
                        "value": [
                            "test-multiple-choice-choice-1",
                            "test-multiple-choice-choice-3",
                        ],
                    },
                    "test-static": {
                        "info_text": None,
                        "label": "Test static",
                        "type": "StaticQuestion",
                        "value": "Some static content",
                    },
                    "test-table": {
                        "info_text": None,
                        "label": "Test table",
                        "rows": [
                            {
                                "name": "Test table form",
                                "questions": {
                                    "row-1": {
                                        "info_text": None,
                                        "label": "Row 1",
                                        "type": "TextQuestion",
                                        "value": "Foo",
                                    },
                                    "row-2": {
                                        "info_text": None,
                                        "label": "Row 2",
                                        "type": "IntegerQuestion",
                                        "value": 2,
                                    },
                                    "row-3": {
                                        "info_text": None,
                                        "label": "Row 3",
                                        "type": "FloatQuestion",
                                        "value": 2.2,
                                    },
                                    "row-4": {
                                        "info_text": None,
                                        "label": "Row 4",
                                        "options": [
                                            ["row-4-choice-1", "choice 1"],
                                            ["row-4-choice-2", "choice 2"],
                                            ["row-4-choice-3", "choice 3"],
                                        ],
                                        "type": "ChoiceQuestion",
                                        "value": "row-4-choice-1",
                                    },
                                    "row-5": {
                                        "info_text": None,
                                        "label": "Row 5",
                                        "options": [
                                            ["row-5-choice-1", "choice 1"],
                                            ["row-5-choice-2", "choice 2"],
                                            ["row-5-choice-3", "choice 3"],
                                        ],
                                        "type": "MultipleChoiceQuestion",
                                        "value": ["row-5-choice-3"],
                                    },
                                },
                            },
                            {
                                "name": "Test table form",
                                "questions": {
                                    "row-1": {
                                        "info_text": None,
                                        "label": "Row 1",
                                        "type": "TextQuestion",
                                        "value": "Bar",
                                    },
                                    "row-2": {
                                        "info_text": None,
                                        "label": "Row 2",
                                        "type": "IntegerQuestion",
                                        "value": 4,
                                    },
                                    "row-3": {
                                        "info_text": None,
                                        "label": "Row 3",
                                        "type": "FloatQuestion",
                                        "value": 5.5,
                                    },
                                    "row-4": {
                                        "info_text": None,
                                        "label": "Row 4",
                                        "options": [
                                            ["row-4-choice-1", "choice 1"],
                                            ["row-4-choice-2", "choice 2"],
                                            ["row-4-choice-3", "choice 3"],
                                        ],
                                        "type": "ChoiceQuestion",
                                        "value": "row-4-choice-2",
                                    },
                                    "row-5": {
                                        "info_text": None,
                                        "label": "Row 5",
                                        "options": [
                                            ["row-5-choice-1", "choice 1"],
                                            ["row-5-choice-2", "choice 2"],
                                            ["row-5-choice-3", "choice 3"],
                                        ],
                                        "type": "MultipleChoiceQuestion",
                                        "value": ["row-5-choice-3", "row-5-choice-1"],
                                    },
                                },
                            },
                        ],
                        "type": "TableQuestion",
                    },
                    "test-text": {
                        "info_text": None,
                        "label": "Test text",
                        "type": "TextQuestion",
                        "value": "Foo",
                    },
                    "test-textarea": {
                        "info_text": None,
                        "label": "Test textarea",
                        "type": "TextareaQuestion",
                        "value": """Bar

Baz""",
                    },
                },
            }
        },
    },
}

snapshots[
    "tests_download_application[admin-e5dabdd0-bafb-4b75-82d2-ccf9295b623b] 2"
] = 'inline; filename="2022-0001 - Gesuch.pdf"'
