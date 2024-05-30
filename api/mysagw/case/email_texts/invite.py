SUBJECT_INVITE_EN = "You have been invited to an application on mySAGW"
BODY_INVITE_EN = """Hello {first_name} {last_name}

You have been invited to an application on mySAGW:

{link}
"""

SUBJECT_INVITE_DE = "Sie wurden zu einem Gesuch auf mySAGW eingeladen"
BODY_INVITE_DE = """Hallo {first_name} {last_name}

Sie wurden zu einem Gesuch auf mySAGW eingeladen:

{link}
"""

SUBJECT_INVITE_FR = "Vous avez été invité à déposer une demande sur mySAGW"
BODY_INVITE_FR = """Bonjour {first_name} {last_name}

Vous avez été invité à déposer une demande sur mySAGW:

{link}
"""


EMAIL_INVITE_SUBJECTS = {
    "de": SUBJECT_INVITE_DE,
    "fr": SUBJECT_INVITE_FR,
    "en": SUBJECT_INVITE_EN,
}
EMAIL_INVITE_BODIES = {"de": BODY_INVITE_DE, "fr": BODY_INVITE_FR, "en": BODY_INVITE_EN}


EMAIL_SUBJECT_INVITE_REGISTER = "Sie wurden zu einem Gesuch auf mySAGW eingeladen"
EMAIL_BODY_INVITE_REGISTER = """DE:

Hallo

Bitte registrieren Sie sich auf {link}, um Zugang zu diesem Gesuch zu erhalten.

====================

EN:

Hello

Please register on {link} for getting access to this application.

====================

FR:

Bonjour

Veuillez vous inscrire sur {link} pour avoir accès à cette application.
"""
