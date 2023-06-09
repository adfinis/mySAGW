import os

import environ
from django.conf import settings
from django.utils.translation import gettext_lazy as _

env = environ.Env()


# Mailing
settings.EMAIL_HOST = os.environ.get("EMAIL_HOST", "mail")
settings.EMAIL_PORT = os.environ.get("EMAIL_PORT", 1025)
settings.EMAIL_HOST_USER = os.environ.get(
    "EMAIL_HOST_USER", "noreply@mysagw.adfinis.com"
)
settings.SERVER_EMAIL = os.environ.get("SERVER_EMAIL", settings.EMAIL_HOST_USER)
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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
settings.LANGUAGE_CODE = env.str("LANGUAGE_CODE", "de")
settings.LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
    ("fr", _("French")),
]
settings.LOCALIZED_FIELDS_FALLBACKS = {
    "de": ["en", "fr"],
    "fr": ["en", "de"],
    "en": ["de", "fr"],
}
settings.LOCALIZED_FIELDS_EXPERIMENTAL = False

# Case

settings.CASE_STATUS = {
    "submit-document": "submit",
    "review-document": "audit",
    "revise-document": "revise",
    "additional-data": "submit-receipts",
    "define-amount": "decision",
    "complete-document": "decision",
}

settings.APPLICANT_TASK_SLUGS = [
    "submit-document",
    "revise-document",
    "additional-data",
    "additional-data-form",
]

settings.CIRCULATION_TASK_SLUGS = [
    "circulation-decision",
]

settings.REVISION_QUESTIONS = {
    "review-document": [
        "priorisierung-der-antrage-kommentar",
        "review-document-decision",
    ],
    "decision-and-credit": [
        "gesprochener-rahmenkredit",
        "decision-and-credit-remark",
        "decision-and-credit-decision",
    ],
    "define-amount": [
        "define-amount-amount-float",
        "define-amount-remark",
        "define-amount-decision",
    ],
}

settings.ADDITIONAL_DATA_FORM = {
    "periodika-antrag": "periodika-abrechnung",
}

settings.INTERNAL_APPLICATION_FORM_SLUG = "intern"
settings.INTERNAL_APPLICATION_TYPE_QUESTION_SLUG = "intern-gesuchsart"
settings.INTERNAL_APPLICATION_PERIODICS_CHOICES = (
    "intern-gesuchsart-intern-abrechnung-periodika",
    "intern-gesuchsart-intern-antrag-periodika",
)

settings.CASE_ID_CACHE_SECONDS = int(os.environ.get("CASE_ID_CACHE_SECONDS", "60"))

# Validation

settings.BIRTHDATE_SLUG_PART = "geburtsdatum"

# Logging

settings.LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "WARNING" if settings.DEBUG else "ERROR",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console", "mail_admins"],
            "level": "WARNING" if settings.DEBUG else "ERROR",
            "propagate": False,
        },
        "graphql": {
            "handlers": ["console", "mail_admins"],
            "level": "WARNING" if settings.DEBUG else "ERROR",
            "propagate": True,
        },
        "caluma": {
            "handlers": ["console", "mail_admins"],
            "level": "WARNING" if settings.DEBUG else "ERROR",
            "propagate": True,
        },
    },
}
