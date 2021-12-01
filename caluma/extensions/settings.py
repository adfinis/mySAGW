import os

from django.conf import settings

# Mailing
settings.EMAIL_HOST = os.environ.get("EMAIL_HOST", "mail")
settings.EMAIL_PORT = os.environ.get("EMAIL_PORT", 1025)
settings.EMAIL_HOST_USER = os.environ.get(
    "EMAIL_HOST_USER", "noreply@mysagw.adfinis.com"
)
settings.EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
settings.EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", False)
from_name = os.environ.get("MAILING_FROM_NAME", "mySAGW")
from_mail = os.environ.get("MAILING_FROM_MAIL", "noreply@mysagw.adfinis.com")
settings.MAILING = {"from_email": from_mail, "from_name": from_name}
settings.MAILING_SENDER = f"{from_name} <{from_mail}>"

# API
settings.API_BASE_URI = os.environ.get("API_BASE_URI", "https://mysagw.local/api/v1")
settings.SELF_URI = os.environ.get("SELF_URI", "https://mysagw.local")
raw_verify_ssl = os.environ.get("API_VERIFY_SSL", "true")
settings.API_VERIFY_SSL = True if raw_verify_ssl == "true" else False

settings.OIDC_ADMIN_CLIENT_ID = os.environ.get("OIDC_ADMIN_CLIENT_ID", "test_client")
settings.OIDC_ADMIN_CLIENT_SECRET = os.environ.get(
    "OIDC_ADMIN_CLIENT_SECRET", "fb13e564-75dd-4fc3-a993-3dad9064e71e"
)
settings.OIDC_TOKEN_ENDPOINT = os.environ.get(
    "OIDC_TOKEN_ENDPOINT",
    "https://mysagw.local/auth/realms/mysagw/protocol/openid-connect/token",
)

# Case

settings.CASE_STATUS = {
    "submit-document": "submit",
    "review-document": "audit",
    "revise-document": "revise",
    "additional-data": "submit-receipts",
    "define-amount": "decision",
}

settings.APPLICANT_TASK_SLUGS = [
    "submit-document",
    "revise-document",
    "additional-data",
    "additional-data-form",
]

settings.ADDITIONAL_DATA_FORM = {
    "periodika-antrag": "periodika-abrechnung",
}

settings.CASE_ID_CACHE_SECONDS = int(os.environ.get("CASE_ID_CACHE_SECONDS", "60"))
