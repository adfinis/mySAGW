SUBJECT_BULK_INVITE_EN = "You have been invited to applications on mySAGW"
BODY_BULK_INVITE_EN = """Hello {first_name} {last_name}

You have been invited to the following applications on mySAGW:

{links}
"""

SUBJECT_BULK_INVITE_DE = "Sie wurden zu Gesuchen auf mySAGW eingeladen"
BODY_BULK_INVITE_DE = """Hallo {first_name} {last_name}

Sie wurden zu folgenden Gesuchen auf mySAGW eingeladen:

{links}
"""

SUBJECT_BULK_INVITE_FR = "Vous avez été invité à soumettre des demandes sur mySAGW"
BODY_BULK_INVITE_FR = """Bonjour {first_name} {last_name}

Vous avez été invitée à soumettre les demandes suivantes sur mySAGW ::

{links}
"""


EMAIL_BULK_INVITE_SUBJECTS = {
    "de": SUBJECT_BULK_INVITE_DE,
    "fr": SUBJECT_BULK_INVITE_FR,
    "en": SUBJECT_BULK_INVITE_EN,
}
EMAIL_BULK_INVITE_BODIES = {
    "de": BODY_BULK_INVITE_DE,
    "fr": BODY_BULK_INVITE_FR,
    "en": BODY_BULK_INVITE_EN,
}
