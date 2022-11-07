SUBJECT_EN = "New information concerning {dossier_nr}"
BODY_EN = """Dear {first_name} {last_name}

After having verified the billing of the application mentioned below, we can confirm that the following amount will be transferred according to the payment details which have been provided:

CHF {payout_amount}

Reference: {dossier_nr}
You can access your document via the following link:
{link}

If you have any questions, please contact us via e-mail (sagw@sagw.ch), phone (+41 31 306 92 50) or online (www.sagw.ch/kontakt-mysagw). Please bear in mind to state the reference number of your application.

Yours sincerely

Your SAGW team

******

This is an automatically generated message. Please do not reply. The contact details of SASH can be found on the following website:
www.sagw.ch/kontakt-mysagw
"""

SUBJECT_DE = "Neue Informationen zu {dossier_nr}"
BODY_DE = """Guten Tag {first_name} {last_name}

Wir haben die Abrechnung des nachfolgenden Gesuchs geprüft. Wir können Ihnen demnach in den kommenden Tagen folgenden Beitrag auf die uns vorliegende Zahlungsverbindung überweisen:

CHF {payout_amount}

Referenz: {dossier_nr}
Über den nachfolgenden Link können Sie direkt auf Ihr Dokument zugreifen, wo Sie die Angaben zu den noch benötigten Informationen finden:
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

Nous avons vérifié le décompte de la demande dont la référence figure ci-dessous. Nous verserons dans les prochains jours, sur les coordonnées de paiement dont nous disposons, le montant suivant:

CHF {payout_amount}

Référence : {dossier_nr}
Vous pouvez accéder directement à votre document en cliquant sur le lien suivant:
{link}

Si vous avez des questions, n’hésitez pas à nous contacter à l’adresse sagw@sagw.ch, au numéro de téléphone +41 31 306 92 50 ou via www.sagw.ch/kontakt-mysagw. Nous vous prions de toujours indiquer le numéro de référence lorsque vous posez une question.

Avec nos meilleures salutations,

Votre équipe de l'ASSH

******

Ceci est un message électronique généré automatiquement, merci de ne pas y répondre. Vous trouverez les coordonnées de l'ASSH sur la page suivante :
www.sagw.ch/kontakt-mysagw
"""


EMAIL_SUBJECTS = {"de": SUBJECT_DE, "fr": SUBJECT_FR, "en": SUBJECT_EN}
EMAIL_BODIES = {"de": BODY_DE, "fr": BODY_FR, "en": BODY_EN}
