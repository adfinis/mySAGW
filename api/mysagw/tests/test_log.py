import logging.config

from django.test import Client
from django.urls import path
from django.views.debug import get_default_exception_reporter_filter
from rest_framework import status


class _TestException(Exception):
    pass


def exception_view(request):
    raise _TestException


urlpatterns = [path("exception-test/", exception_view)]


def test_error_email(mailoutbox, settings, snapshot):
    settings.ROOT_URLCONF = __name__
    settings.DEBUG = False
    settings.ADMINS = [("Admin Test", "admin@example.com")]
    settings.DEFAULT_EXCEPTION_REPORTER_FILTER = (
        "mysagw.log.CensoredExceptionReporterFilter"
    )
    settings.LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(settings.LOGGING)

    # Make sure lru cache of the function that uses the above setting is empty
    get_default_exception_reporter_filter.cache_clear()
    assert get_default_exception_reporter_filter.cache_info().hits == 0

    client = Client()
    client.raise_request_exception = False

    response = client.post(
        "/exception-test/",
        data={"foo": "bar"},
        HTTP_USER_AGENT="pytest",
        HTTP_AUTHORIZATION="Bearer sometoken",
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert len(mailoutbox) == 1

    # Only check everything after "Request information" as the header data and
    # traceback would cause this snapshot to be failing all the time
    assert snapshot == mailoutbox[0].body.split("Request information:", 1)[-1].strip()
