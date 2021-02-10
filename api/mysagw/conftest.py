import importlib
import inspect
from functools import partial

import pytest
from django.core.cache import cache
from factory import Faker
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .faker import MultilangProvider, SwissPhoneNumberProvider
from .oidc_auth.models import OIDCUser

Faker.add_provider(MultilangProvider)
Faker.add_provider(SwissPhoneNumberProvider)


def register_module(module):
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            register(obj)


register_module(importlib.import_module(".identity.factories", "mysagw"))
register_module(importlib.import_module(".snippets.factories", "mysagw"))


def _get_claims(
    settings,
    id_claim="00000000-0000-0000-0000-000000000000",
    groups_claim=None,
    email_claim="test@example.com",
):
    groups_claim = groups_claim if groups_claim else []
    return {
        settings.OIDC_ID_CLAIM: id_claim,
        settings.OIDC_GROUPS_CLAIM: groups_claim,
        settings.OIDC_EMAIL_CLAIM: email_claim,
    }


@pytest.fixture
def get_claims(settings):
    return partial(_get_claims, settings)


@pytest.fixture
def claims(settings):
    return _get_claims(settings)


@pytest.fixture
def admin_user(settings, get_claims):
    return OIDCUser(
        "sometoken",
        get_claims("admin", [settings.ADMIN_GROUP], "admin@example.com"),
    )


@pytest.fixture
def staff_user(settings, get_claims):
    return OIDCUser(
        "sometoken",
        get_claims("staff_user", [settings.STAFF_GROUP], "staff@example.com"),
    )


@pytest.fixture
def user(get_claims):
    return OIDCUser(
        "sometoken",
        get_claims("user", [], "user@example.com"),
    )


@pytest.fixture(params=["admin"])
def client(db, user, staff_user, admin_user, request):
    usermap = {"user": user, "staff": staff_user, "admin": admin_user}
    client = APIClient()
    user = usermap[request.param]
    client.force_authenticate(user=user)
    client.user = user
    return client


@pytest.fixture(scope="function", autouse=True)
def _autoclear_cache():
    cache.clear()
