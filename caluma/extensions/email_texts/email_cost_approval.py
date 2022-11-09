SUBJECT_EN = "New information concerning {dossier_nr}"
BODY_EN = """Dear {first_name} {last_name}

After a careful review your application we are pleased to inform you that a framework credit of CHF {framework_credit} has been approved for the project mentioned below.

You can download your application and the approval of the framework credit as PDF files under the heading «Download».

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

Wir haben Ihren Antrag geprüft und freuen uns, Ihnen mitteilen zu können, dass wir für das unten genannte Projekt einen Rahmenkredit von CHF {framework_credit} gesprochen haben.

Bei Bedarf können Sie Ihren Antrag und die Kostenzusprache als PDF unter der Rubrik «Download» herunterladen.

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

Nous avons examiné votre demande et avons le plaisir de vous informer que nous avons accordé un crédit-cadre de {framework_credit} CHF pour le projet mentionné ci-dessous.

Si nécessaire, vous pouvez télécharger votre demande et la confirmation de l’octroi du financement en format PDF sous la rubrique «Download».

Référence : {dossier_nr}
Cliquez sur le lien ci-dessous pour ouvrir votre document:
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
