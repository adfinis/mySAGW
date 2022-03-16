SUBJECT_EN = "New information concerning {dossier_nr}"
BODY_EN = """Dear {first_name} {last_name}

The status of the following application/document has changed:

Reference: {dossier_nr}
You can access your document directly via the following link:
{link}

If you have any questions, please feel free to contact us via sagw@sagw.ch, the telephone number +41 31 306 92 50 or at www.sagw.ch/kontakt-mysagw. Please always quote the reference number if you have a question.

Yours sincerely

Your SAGW team

******

This is an automatically generated email, please do not reply to this message. You can find the contact details of SAGW on the following page:
www.sagw.ch/kontakt-mysagw
"""

SUBJECT_DE = "Neue Informationen zu {dossier_nr}"
BODY_DE = """Guten Tag {first_name} {last_name}

Der Status des nachfolgenden Gesuchs/Dokument hat sich geändert:

Referenz: {dossier_nr}
Über den nachfolgenden Link können Sie direkt auf Ihr Dokument zugreifen:
{link}

Sollten Sie Fragen haben, können Sie uns gerne über sagw@sagw.ch, die Telefonnummer +41 31 306 92 50 oder unter www.sagw.ch/kontakt-mysagw kontaktieren. Gerne bitten wir Sie, bei einer Frage immer die Referenznummer anzugeben.

Freundliche Grüsse

Ihr SAGW-Team

******

Dies ist eine automatisch generierte Email, bitte antworten Sie nicht auf diese Nachricht. Die Kontaktangaben der SAGW können Sie der nachfolgenden Seite entnehmen:
www.sagw.ch/kontakt-mysagw
"""

SUBJECT_FR = "Nouvelles informations concernant {dossier_nr}"
BODY_FR = """Bonjour {first_name} {last_name}

Le statut de la demande/du document ci-dessous a changé:

Référence : {dossier_nr}
Cliquez sur le lien ci-dessous pour ouvrir votre document:
{link}

Si vous avez des questions, n'hésitez pas à nous contacter via sagw@sagw.ch, au numéro de téléphone +41 31 306 92 50 ou à l'adresse www.sagw.ch/kontakt-mysagw. Nous vous prions de toujours indiquer le numéro de référence lorsque vous posez une question.

Avec nos meilleures salutations,

Votre équipe de l'ASSH

******

Ceci est un message électronique généré automatiquement, merci de ne pas y répondre. Vous trouverez les coordonnées de l'ASSH sur la page suivante :
www.sagw.ch/kontakt-mysagw
"""


EMAIL_SUBJECTS = {"de": SUBJECT_DE, "fr": SUBJECT_FR, "en": SUBJECT_EN}
EMAIL_BODIES = {"de": BODY_DE, "fr": BODY_FR, "en": BODY_EN}
