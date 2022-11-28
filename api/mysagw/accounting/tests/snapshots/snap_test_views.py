# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_get_receipts[admin-False-False-200] 1"] = {
    "convert": "pdf",
    "data": {
        "applicant_address": "Dorfplatz 1",
        "applicant_city": "Zürich",
        "applicant_land": "Schweiz",
        "applicant_name": "Winston Smith",
        "applicant_postcode": "8000",
        "bank": "Big Bank",
        "bank_town": "Bern",
        "circ_kontonummer": "23 konto1",
        "date": "01. 01. 1970",
        "dossier_no": "2021-0006",
        "form": "Foo form",
        "iban": "CH56 0483 5012 3456 7800 9",
        "mitgliedinstitution": "Foo institute",
        "section": "6",
        "total": 5000.0,
        "vp_year": "",
        "zahlungszweck": "Foo Bar",
    },
}

snapshots["test_get_receipts[admin-False-True-200] 1"] = {
    "convert": "pdf",
    "data": {
        "applicant_address": "",
        "applicant_city": "",
        "applicant_land": "",
        "applicant_name": "",
        "applicant_postcode": "",
        "bank": "",
        "bank_town": "",
        "circ_kontonummer": "",
        "date": "01. 01. 1970",
        "dossier_no": "",
        "form": "",
        "iban": "",
        "mitgliedinstitution": "",
        "section": "",
        "total": "",
        "vp_year": "",
        "zahlungszweck": "",
    },
}

snapshots["test_get_receipts[staff-False-False-200] 1"] = {
    "convert": "pdf",
    "data": {
        "applicant_address": "Dorfplatz 1",
        "applicant_city": "Zürich",
        "applicant_land": "Schweiz",
        "applicant_name": "Winston Smith",
        "applicant_postcode": "8000",
        "bank": "Big Bank",
        "bank_town": "Bern",
        "circ_kontonummer": "23 konto1",
        "date": "01. 01. 1970",
        "dossier_no": "2021-0006",
        "form": "Foo form",
        "iban": "CH56 0483 5012 3456 7800 9",
        "mitgliedinstitution": "Foo institute",
        "section": "6",
        "total": 5000.0,
        "vp_year": "",
        "zahlungszweck": "Foo Bar",
    },
}
