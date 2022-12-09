# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_identity_export[admin] 1"] = [
    [
        "first_name",
        "last_name",
        "localized_salutation",
        "localized_title",
        "language",
        "is_organisation",
        "organisation_name",
        "email",
        "additional_emails",
        "phone_numbers",
        "address_addition_1",
        "address_addition_2",
        "address_addition_3",
        "street_and_number",
        "po_box",
        "postcode",
        "town",
        "country",
    ],
    [
        "Caitlin",
        "Adams",
        "",
        "",
        "de",
        0,
        "",
        "ryanjohnson@example.net",
        """portertodd@example.com
sharonjohnson@example.org
suzanne77@example.net""",
        """+41774226576
+41311370448
+41772344015""",
        "",
        "",
        "",
        "7562 Navarro Summit Suite 837",
        "",
        "54786",
        "Tiffanyside",
        "Andorra",
    ],
    [
        "Craig",
        "Brady",
        "Monsieur",
        "",
        "fr",
        0,
        "",
        "qskinner@example.com",
        """fjohnson@example.com
stevenssamuel@example.net
ydiaz@example.net""",
        """+41312929485
+41317142073
+41444486160""",
        "",
        "",
        "",
        "21610 Liu Underpass",
        "",
        "14517",
        "Port Donald",
        "Taiwan",
    ],
    [
        "Christopher",
        "Brown",
        "Mrs.",
        "",
        "en",
        0,
        "",
        "jackellis@example.com",
        """amy74@example.net
bakerjesse@example.org
ztran@example.com""",
        """+41412171090
+41790516770
+41798420328""",
        "",
        "",
        "",
        "8185 Benjamin Ridge Suite 151",
        "",
        "35443",
        "Brownton",
        "Irak",
    ],
    [
        "Samantha",
        "Brown",
        "",
        "",
        "de",
        0,
        "",
        "carlcunningham@example.net",
        """charles79@example.net
johnstonalexis@example.org
laurafrost@example.com""",
        """+41768080237
+41441740467
+41569353057""",
        "",
        "",
        "",
        "8714 Thomas Parkways",
        "",
        "31593",
        "Victoriamouth",
        "Kuwait",
    ],
    [
        "Elizabeth",
        "Collins",
        "",
        "",
        "de",
        0,
        "",
        "bryantjessica@example.com",
        """everettfernando@example.com
glassdrew@example.org
linda52@example.org""",
        """+41316164119
+41440080179
+41777230396""",
        "",
        "",
        "",
        "17187 Hernandez Fall",
        "",
        "64195",
        "South Mariahside",
        "Bulgarien",
    ],
    [
        "Cameron",
        "Howard",
        "",
        "",
        "de",
        0,
        "",
        "calebsoto@example.net",
        """cohenthomas@example.org
fostersusan@example.net
robertferguson@example.com""",
        """+41417090372
+41417372016
+41441953915""",
        "",
        "",
        "",
        "7980 Kyle Vista Apt. 991",
        "",
        "68698",
        "Jonesshire",
        "Antigua und Barbuda",
    ],
    [
        "Jared",
        "Hunter",
        "",
        "",
        "de",
        0,
        "",
        "jenniferwilliams@example.org",
        """amy27@example.net
evanskimberly@example.net
smithaaron@example.com""",
        """+41778338833
+41568398644
+41794151762""",
        "",
        "",
        "",
        "36714 Ellis Meadows Suite 555",
        "",
        "56706",
        "Tiffanyview",
        "Gambia",
    ],
    [
        "Carolyn",
        "Stephens",
        "",
        "",
        "de",
        0,
        "",
        "khayes@example.org",
        """chapmanjonathan@example.com
harriscynthia@example.com
smithpatrick@example.com""",
        """+41761631936
+41441652479
+41774821908""",
        "",
        "",
        "",
        "8402 Alexander Cove",
        "",
        "32866",
        "New Charlottestad",
        "Zypern",
    ],
    [
        "Cynthia",
        "Ware",
        "",
        "",
        "de",
        0,
        "",
        "jonathan94@example.org",
        """gmartinez@example.com
watsontravis@example.org
xbrandt@example.org""",
        """+41313311645
+41782813895
+41783574710""",
        "",
        "",
        "",
        "5440 Booth Knoll Apt. 817",
        "",
        "97693",
        "Aprilbury",
        "Kongo",
    ],
    [
        "Hector",
        "Wilson",
        "",
        "",
        "de",
        1,
        "Bryan and Sons",
        "lhernandez@example.net",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ],
    [
        "Thomas",
        "Woods",
        "",
        "",
        "de",
        0,
        "",
        "tanya60@example.net",
        """ihardy@example.com
qstewart@example.com
stokesmichael@example.net""",
        """+41316245787
+41318252219
+41792181419""",
        "",
        "",
        "",
        "720 Scott Square",
        "",
        "35967",
        "Robertfurt",
        "Dominikanische Republik",
    ],
]

snapshots["test_identity_export_labels_context[admin] 1"] = {
    "identities": [
        [
            {
                "address_addition_1": "",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "Dominica",
                "first_name": "Caitlin",
                "last_name": "Adams",
                "localized_title": "",
                "organisation_name": "",
                "po_box": "",
                "postcode": "69035",
                "street_and_number": "3129 Autumn Roads",
                "town": "Karamouth",
            },
            {
                "address_addition_1": "",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "China",
                "first_name": "Craig",
                "last_name": "Brady",
                "localized_title": "",
                "organisation_name": "",
                "po_box": "",
                "postcode": "25734",
                "street_and_number": "492 Theresa Islands Apt. 327",
                "town": "New Sherrifurt",
            },
        ],
        [
            {
                "address_addition_1": "",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "Peru",
                "first_name": "Christopher",
                "last_name": "Brown",
                "localized_title": "",
                "organisation_name": "",
                "po_box": "",
                "postcode": "74278",
                "street_and_number": "202 Lori Station Apt. 776",
                "town": "Karenview",
            },
            {
                "address_addition_1": "",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "Belize",
                "first_name": "Samantha",
                "last_name": "Brown",
                "localized_title": "",
                "organisation_name": "",
                "po_box": "",
                "postcode": "87711",
                "street_and_number": "00390 Massey Center",
                "town": "Michaelland",
            },
        ],
        [
            {
                "address_addition_1": "Haus der Akademien",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "Bahrain",
                "first_name": "Elizabeth",
                "last_name": "Collins",
                "localized_title": "",
                "organisation_name": "SAGW",
                "po_box": "23",
                "postcode": "09424",
                "street_and_number": "92828 Martin Meadow Suite 942",
                "town": "Taylorshire",
            },
            {
                "address_addition_1": "",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "Schweiz",
                "first_name": "Cameron",
                "last_name": "Howard",
                "localized_title": "",
                "organisation_name": "",
                "po_box": "",
                "postcode": "56598",
                "street_and_number": "0356 Arroyo Isle Suite 694",
                "town": "North Sandraville",
            },
        ],
        [
            {
                "address_addition_1": "",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "Papua Neu Guinea",
                "first_name": "Jared",
                "last_name": "Hunter",
                "localized_title": "",
                "organisation_name": "",
                "po_box": "",
                "postcode": "66800",
                "street_and_number": "70906 Ryan Crossing Apt. 052",
                "town": "West Darylfort",
            },
            {
                "address_addition_1": "",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "Israel",
                "first_name": "Susan",
                "last_name": "Park",
                "localized_title": "",
                "organisation_name": "",
                "po_box": "",
                "postcode": "87372",
                "street_and_number": "09693 Buchanan Pines Apt. 875",
                "town": "East Andrew",
            },
        ],
        [
            {
                "address_addition_1": "",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "Ruanda",
                "first_name": "Carolyn",
                "last_name": "Stephens",
                "localized_title": "",
                "organisation_name": "",
                "po_box": "",
                "postcode": "42361",
                "street_and_number": "589 Patricia Club",
                "town": "New Dale",
            },
            {
                "address_addition_1": "",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "Mozambique",
                "first_name": "Cynthia",
                "last_name": "Ware",
                "localized_title": "",
                "organisation_name": "",
                "po_box": "",
                "postcode": "72713",
                "street_and_number": "2841 Levi Throughway",
                "town": "South Amanda",
            },
        ],
        [
            {
                "address_addition_1": "",
                "address_addition_2": "",
                "address_addition_3": "",
                "country": "Irak",
                "first_name": "Thomas",
                "last_name": "Woods",
                "localized_title": "",
                "organisation_name": "",
                "po_box": "",
                "postcode": "35443",
                "street_and_number": "99841 Quinn Common",
                "town": "Brownton",
            },
            {},
        ],
    ]
}

snapshots["test_membership_export[admin] 1"] = [
    [
        "first_name",
        "last_name",
        "localized_salutation",
        "localized_title",
        "language",
        "email",
        "address_addition_1",
        "address_addition_2",
        "address_addition_3",
        "street_and_number",
        "po_box",
        "postcode",
        "town",
        "country",
        "organisation",
        "role",
        "inactive",
        "tenure",
        "next_election",
    ],
    [
        "Thomas",
        "Woods",
        "",
        "",
        "de",
        "tanya60@example.net",
        "",
        "",
        "",
        "5440 Booth Knoll Apt. 817",
        "",
        "97693",
        "Aprilbury",
        "Kongo",
        "Nonsafe",
        "Binnenschiffer",
        0,
        "",
        "",
    ],
    [
        "Samantha",
        "Brown",
        "",
        "",
        "de",
        "carlcunningham@example.net",
        "",
        "",
        "",
        "8714 Thomas Parkways",
        "",
        "31593",
        "Victoriamouth",
        "Kuwait",
        "Allsafe",
        "Mechaniker",
        0,
        "",
        "",
    ],
    [
        "Jared",
        "Hunter",
        "",
        "",
        "de",
        "jenniferwilliams@example.org",
        "",
        "",
        "",
        "36714 Ellis Meadows Suite 555",
        "",
        "56706",
        "Tiffanyview",
        "Gambia",
        "Nonsafe",
        "Designer",
        0,
        "",
        "",
    ],
    [
        "Elizabeth",
        "Collins",
        "",
        "",
        "de",
        "bryantjessica@example.com",
        "",
        "",
        "",
        "17187 Hernandez Fall",
        "",
        "64195",
        "South Mariahside",
        "Bulgarien",
        "Allsafe",
        "",
        0,
        "2020-01-01 - 2020-01-02",
        "2020-11-23",
    ],
    [
        "Cynthia",
        "Ware",
        "",
        "",
        "de",
        "jonathan94@example.org",
        "",
        "",
        "",
        "8402 Alexander Cove",
        "",
        "32866",
        "New Charlottestad",
        "Zypern",
        "Nonsafe",
        "Arzt",
        0,
        "",
        "",
    ],
    [
        "Cameron",
        "Howard",
        "",
        "",
        "de",
        "calebsoto@example.net",
        "",
        "",
        "",
        "7980 Kyle Vista Apt. 991",
        "",
        "68698",
        "Jonesshire",
        "Antigua und Barbuda",
        "Allsafe",
        "Designer",
        1,
        "2020-01-01 - ",
        "",
    ],
]
