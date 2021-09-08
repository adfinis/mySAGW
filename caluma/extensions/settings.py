import os

from django.conf import settings

# Mailing
settings.EMAIL_HOST = os.environ.get("EMAIL_HOST", "mail")
settings.EMAIL_USE_TLS = False
settings.EMAIL_PORT = os.environ.get("EMAIL_PORT", 1025)
from_name = os.environ.get("MAILING_FROM_NAME", "mySAGW")
from_mail = os.environ.get("MAILING_FROM_MAIL", "noreply@mysagw.adfinis.com")
settings.MAILING = {"from_email": from_mail, "from_name": from_name}
settings.MAILING_SENDER = f"{from_name} <{from_mail}>"

# API
settings.API_BASE_URI = os.environ.get("API_BASE_URI", "http://api:8000/api/v1")
settings.SELF_URI = os.environ.get("SELF_URI", "https://mysagw.local")

# Case

settings.CASE_STATUS = {
    "submit-document": "submit",
    "review-document": "audit",
    "revise-document": "revise",
    "additional-data": "submit-receipts",
    "define-amount": "decision",
}
