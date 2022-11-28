import os
import re

import environ
from django.utils.translation import gettext_lazy as _

env = environ.Env()
django_root = environ.Path(__file__) - 2

ENV_FILE = env.str("ENV_FILE", default=django_root(".env"))
if os.path.exists(ENV_FILE):  # pragma: no cover
    environ.Env.read_env(ENV_FILE)

# per default production is enabled for security reasons
# for development create .env file with ENV=development
ENV = env.str("ENV", "production")


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == "production" else default_dev


SECRET_KEY = env.str("SECRET_KEY", default=default("uuuuuuuuuu"))
DEBUG = env.bool("DEBUG", default=default(True, False))
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=default(["*"]))


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "localized_fields",
    "phonenumber_field",
    "django_countries",
    "simple_history",
    "mysagw.identity.apps.DefaultConfig",
    "mysagw.snippets.apps.SnippetsConfig",
    "mysagw.accounting.apps.AccountingConfig",
    "mysagw.case.apps.CaseConfig",
    "mysagw.healthz.apps.HealthzConfig",
]

if ENV == "dev":
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "mysagw.urls"
WSGI_APPLICATION = "mysagw.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": env.str("DATABASE_NAME", default="mysagw"),
        "USER": env.str("DATABASE_USER", default="mysagw"),
        "PASSWORD": env.str("DATABASE_PASSWORD", default=default("mysagw")),
        "HOST": env.str("DATABASE_HOST", default="db"),
        "PORT": env.str("DATABASE_PORT", default=""),
        "OPTIONS": env.dict("DATABASE_OPTIONS", default={}),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = env.str("LANGUAGE_CODE", "de")
LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
    ("fr", _("French")),
]
LOCALIZED_FIELDS_FALLBACKS = {
    "de": ["en", "fr"],
    "fr": ["en", "de"],
    "en": ["de", "fr"],
}
LOCALIZED_FIELDS_EXPERIMENTAL = False

TIME_ZONE = env.str("TIME_ZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

COUNTRIES_FIRST = ["CH", "DE", "FR", "IT", "AT"]

# Phonenumbers

PHONENUMBER_DEFAULT_REGION = "CH"


# Authentication
OIDC_OP_USER_ENDPOINT = env.str("OIDC_OP_USER_ENDPOINT", default=None)
OIDC_OP_TOKEN_ENDPOINT = "not supported in mysagw, but a value is needed"
OIDC_VERIFY_SSL = env.bool("OIDC_VERIFY_SSL", default=True)
OIDC_ID_CLAIM = env.str("OIDC_ID_CLAIM", default="sub")
OIDC_EMAIL_CLAIM = env.str("OIDC_EMAIL_CLAIM", default="email")
OIDC_GROUPS_CLAIM = env.str("OIDC_GROUPS_CLAIM", default="mysagw_groups")
OIDC_CLIENT_ID_CLAIM = env.str("OIDC_CLIENT_ID_CLAIM", default="clientId")
OIDC_BEARER_TOKEN_REVALIDATION_TIME = env.int(
    "OIDC_BEARER_TOKEN_REVALIDATION_TIME", default=0
)
OIDC_OP_INTROSPECT_ENDPOINT = env.str("OIDC_OP_INTROSPECT_ENDPOINT", default=None)
OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID", default="test_client")
OIDC_RP_CLIENT_SECRET = env.str(
    "OIDC_RP_CLIENT_SECRET", default="fb13e564-75dd-4fc3-a993-3dad9064e71e"
)
OIDC_MONITORING_CLIENT_ID = env.str(
    "OIDC_MONITORING_CLIENT_ID", default="monitoring_client"
)
OIDC_DRF_AUTH_BACKEND = "mysagw.oidc_auth.authentication.MySAGWAuthenticationBackend"

# simple history
SIMPLE_HISTORY_HISTORY_ID_USE_UUID = True

# watchman
WATCHMAN_CHECKS = env.list(
    "WATCHMAN_CHECKS",
    default=(
        "mysagw.healthz.health_checks.check_migrations",
        "mysagw.healthz.health_checks.check_models",
        "watchman.checks.caches",
        "watchman.checks.databases",
    ),
)
WATCHMAN_ERROR_CODE = 503


# Document Merge Service
DOCUMENT_MERGE_SERVICE_URL = env.str(
    "DOCUMENT_MERGE_SERVICE_URL", default="http://dms:8000/api/v1"
)
DOCUMENT_MERGE_SERVICE_ENGINE = env.str(
    "DOCUMENT_MERGE_SERVICE_ENGINE", default="docx-template"
)

DOCUMENT_MERGE_SERVICE_LABELS_TEMPLATE_SLUG = env.str(
    "DOCUMENT_MERGE_SERVICE_LABELS_TEMPLATE_SLUG", default="identity-labels"
)
DOCUMENT_MERGE_SERVICE_ACCOUNTING_COVER_TEMPLATE_SLUG = env.str(
    "DOCUMENT_MERGE_SERVICE_ACCOUNTING_COVER_TEMPLATE_SLUG", default="accounting-cover"
)
DOCUMENT_MERGE_SERVICE_ACKNOWLEDGEMENT_TEMPLATE_SLUG = env.str(
    "DOCUMENT_MERGE_SERVICE_ACKNOWLEDGEMENT_TEMPLATE_SLUG", default="acknowledgement"
)
DOCUMENT_MERGE_SERVICE_CREDIT_APPROVAL_TEMPLATE_SLUG = env.str(
    "DOCUMENT_MERGE_SERVICE_CREDIT_APPROVAL_TEMPLATE_SLUG", default="credit-approval"
)
DOCUMENT_MERGE_SERVICE_APPLICATION_EXPORT_SLUG = env.str(
    "DOCUMENT_MERGE_SERVICE_APPLICATION_EXPORT_SLUG", default="application"
)

# Caluma
CALUMA_VERIFY_SSL = env.bool("CALUMA_VERIFY_SSL", default=True)


REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "rest_framework_json_api.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
        "mysagw.identity.filters.SAGWSearchFilter",
    ),
    "ORDERING_PARAM": "sort",
    "SEARCH_PARAM": "filter[search]",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
}

JSON_API_FORMAT_FIELD_NAMES = "dasherize"
JSON_API_FORMAT_TYPES = "dasherize"
JSON_API_PLURALIZE_TYPES = True

# mySAGW
ADMIN_GROUP = "admin"
STAFF_GROUP = "sagw"

# mailing
EMAIL_HOST = env.str("EMAIL_HOST", "mail")
EMAIL_PORT = env.int("EMAIL_PORT", 1025)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "noreply@mysagw.adfinis.com")
SERVER_EMAIL = env.str("SERVER_EMAIL", EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", False)
from_name = env.str("MAILING_FROM_NAME", "mySAGW")
from_mail = env.str("MAILING_FROM_MAIL", "noreply@mysagw.adfinis.com")
MAILING = {"from_email": from_mail, "from_name": from_name}
MAILING_SENDER = f"{from_name} <{from_mail}>"

SELF_URI = env.str("SELF_URI", "https://mysagw.adfinis.com")


def parse_admins(admins):
    """
    Parse env admins to django admins.

    Example of ADMINS environment variable:
    Test Example <test@example.com>,Test2 <test2@example.com>
    """
    result = []
    for admin in admins:
        match = re.search(r"(.+) \<(.+@.+)\>", admin)
        if not match:  # pragma: no cover
            raise environ.ImproperlyConfigured(
                'In ADMINS admin "{0}" is not in correct '
                '"Firstname Lastname <email@example.com>"'.format(admin)
            )
        result.append((match.group(1), match.group(2)))
    return result


ADMINS = parse_admins(env.list("ADMINS", default=[]))

# Logging

LOGGING = {
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
            "level": "WARNING" if DEBUG else "ERROR",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console", "mail_admins"],
            "level": "WARNING" if DEBUG else "ERROR",
            "propagate": False,
        },
        "mysagw": {
            "handlers": ["console", "mail_admins"],
            "level": "WARNING" if DEBUG else "ERROR",
            "propagate": True,
        },
    },
}
