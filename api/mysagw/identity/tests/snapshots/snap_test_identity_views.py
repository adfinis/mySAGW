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
        "language",
        "is_organisation",
        "organisation_name",
        "email",
        "additional_emails",
        "phone_numbers",
        "address_addition",
        "street_and_number",
        "po_box",
        "postcode",
        "town",
        "country",
    ],
    [
        "Carol",
        "Anderson",
        "",
        "de",
        0,
        "",
        "thomas86@yahoo.com",
        """cassandra17@hotmail.com
jonathan55@gmail.com
tonymata@hotmail.com""",
        """+41316558056
+41566278583
+41777769447""",
        "",
        "2805 Kristin Estate Apt. 842",
        "",
        "40940",
        "Jimenezview",
        "CN",
    ],
    [
        "William",
        "Brown",
        "Monsieur",
        "fr",
        0,
        "",
        "chennicole@hotmail.com",
        """chadlong@green.com
justincain@williams-moody.com
utaylor@hotmail.com""",
        """+41779705140
+41312929485
+41561727655""",
        "",
        "6778 Parker Canyon Apt. 565",
        "",
        "44382",
        "Sandersview",
        "NP",
    ],
    [
        "Anthony",
        "Dawson",
        "Mrs.",
        "en",
        0,
        "",
        "carlcunningham@hardin.com",
        """adamsbryce@gmail.com
cherylkeller@hotmail.com
karen86@gmail.com""",
        """+41441099841
+41316299487
+41779957818""",
        "",
        "8671 Mitchell Grove",
        "",
        "14020",
        "Rachaelhaven",
        "PY",
    ],
    [
        "Nicole",
        "Fields",
        "",
        "de",
        0,
        "",
        "larryrichmond@gmail.com",
        """lawrencejones@rosales-long.net
mwilson@lee.org
sanchezvictor@cortez-mitchell.info""",
        """+41415799371
+41417404672
+41760802375""",
        "",
        "408 Huff Freeway",
        "",
        "47813",
        "Cobbburgh",
        "LU",
    ],
    [
        "Ronald",
        "Hernandez",
        "",
        "de",
        0,
        "",
        "hallsean@chavez.com",
        """ijones@harris.com
joseph46@yahoo.com
michele02@hotmail.com""",
        """+41787187622
+41762222301
+41795211227""",
        "",
        "831 Powell Freeway Apt. 642",
        "",
        "27677",
        "North Justin",
        "BD",
    ],
    [
        "Justin",
        "Irwin",
        "",
        "de",
        0,
        "",
        "wrightapril@gmail.com",
        """david42@sanders.com
ljones@thompson.net
msnyder@yahoo.com""",
        """+41773498099
+41763628840
+41775944798""",
        "",
        "4377 Matthew Corners",
        "",
        "40848",
        "Lake Walter",
        "SG",
    ],
    [
        "Lori",
        "Joseph",
        "",
        "de",
        1,
        "Thomas and Sons",
        "tkennedy@gmail.com",
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
        "Martinez",
        "",
        "de",
        0,
        "",
        "sarahmalone@allen.com",
        """bryan87@kent-wright.com
jennifer21@hotmail.com
samuel75@gmail.com""",
        """+41795432280
+41317366555
+41787336714""",
        "",
        "48822 Daniel Ford",
        "",
        "93728",
        "Lake Robertahaven",
        "FM",
    ],
    [
        "Grace",
        "Mccoy",
        "",
        "de",
        0,
        "",
        "phyllis84@hotmail.com",
        """leachashley@yahoo.com
rachel63@mcclain.com
sdean@lane.com""",
        """+41313199552
+41566840210
+41767703937""",
        "",
        "1046 Jennifer Roads Suite 784",
        "",
        "63854",
        "Staceymouth",
        "CN",
    ],
    [
        "Kimberly",
        "Stanley",
        "",
        "de",
        0,
        "",
        "jamesacosta@zimmerman.com",
        """brenda22@hotmail.com
mendozachristina@ayers-lawson.info
vgordon@yang-hill.org""",
        """+41414519945
+41316482941
+41319070673""",
        "",
        "55884 William Passage",
        "",
        "58917",
        "East Charlestown",
        "GT",
    ],
    [
        "Karen",
        "Young",
        "",
        "de",
        0,
        "",
        "leerussell@hotmail.com",
        """hmolina@yahoo.com
justindominguez@gmail.com
lori16@gmail.com""",
        """+41445751864
+41418894603
+41778561623""",
        "",
        "9416 Maurice Centers",
        "",
        "59259",
        "Antonioville",
        "LR",
    ],
]
