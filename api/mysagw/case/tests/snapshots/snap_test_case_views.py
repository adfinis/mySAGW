# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Frau Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte Frau Dr. Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Frau Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte Frau Dr. Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Frau Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte Frau Dr. Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Frau Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte Frau Dr. Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Frau Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte Frau Dr. Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Frau Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte Frau Dr. Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Herr Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrter Herr Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Herr Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrter Herr Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Herr Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrter Herr Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Herr Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrter Herr Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Herr Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrter Herr Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Herr Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrter Herr Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Prof. Dr. Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Prof. Dr. Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Prof. Dr. Bruce Wilkins",
            "language": "de",
        },
    },
}

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Eingangsbest%C3%A4tigung.pdf"

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Prof. Dr. Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Prof. Dr. Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Sehr geehrte·r Prof. Dr. Bruce Wilkins",
            "language": "de",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[de-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = 'inline; filename="2022-0001 - Kreditgutsprache.pdf"'

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mrs. Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mrs. Dr. Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mrs. Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mrs. Dr. Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mrs. Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mrs. Dr. Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mrs. Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mrs. Dr. Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mrs. Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mrs. Dr. Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mrs. Dr. Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mrs. Dr. Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mr. Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mr. Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mr. Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mr. Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mr. Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mr. Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mr. Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mr. Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mr. Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mr. Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Mr. Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Mr. Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Prof. Dr. Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Prof. Dr. Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Prof. Dr. Bruce Wilkins",
            "language": "en",
        },
    },
}

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = 'inline; filename="2022-0001 - Acknowledgement of receipt.pdf"'

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Prof. Dr. Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Prof. Dr. Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr. Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Dear Prof. Dr. Bruce Wilkins",
            "language": "en",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[en-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = 'inline; filename="2022-0001 - Credit approval.pdf"'

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Madame Dr Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Madame Dr Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Madame Dr Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Madame Dr Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Madame Dr Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Madame Dr Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Madame Dr Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Madame Dr Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Madame Dr Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Madame Dr Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Madame Dr Bruce Wilkins
77130 Katherine Mountains
and
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Madame Dr Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-dr-female-1234567-something-and-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Monsieur Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Monsieur Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Monsieur Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Monsieur Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Monsieur Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Monsieur Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Monsieur Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Monsieur Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Monsieur Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Monsieur Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Monsieur Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Monsieur Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-none-male-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Bruce Wilkins
77130 Katherine Mountains
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-none-neutral-None-None-None-None-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Prof. Dr Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Prof. Dr Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Prof. Dr Bruce Wilkins",
            "language": "fr",
        },
    },
}

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-acknowledgement-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accus%C3%A9%20de%20r%C3%A9ception.pdf"

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Prof. Dr Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-admin] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Prof. Dr Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-staff] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 1"
] = {
    "convert": "pdf",
    "data": {
        "date": "1. Januar 1970",
        "dossier_nr": "2022-0001",
        "identity": {
            "address_block": """Prof. Dr Bruce Wilkins
77130 Katherine Mountains
more
1234567
16870 Grahammouth
Osttimor""",
            "greeting_salutation_and_name": "Prof. Dr Bruce Wilkins",
            "language": "fr",
        },
        "rahmenkredit": "23",
    },
}

snapshots[
    "test_download[fr-prof-dr-neutral-1234567-something-None-more-e5dabdd0-bafb-4b75-82d2-ccf9295b623b-credit-approval-user] 2"
] = "inline; filename*=utf-8''2022-0001%20-%20Accord%20de%20cr%C3%A9dit.pdf"
