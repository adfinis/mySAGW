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
