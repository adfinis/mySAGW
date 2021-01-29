import importlib
import inspect

import pytest
from django.core.cache import cache
from factory import Faker
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .faker import MultilangProvider
from .oidc_auth.models import OIDCUser

Faker.add_provider(MultilangProvider)


def register_module(module):
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            register(obj)


register_module(importlib.import_module(".identity.factories", "mysagw"))


@pytest.fixture
def admin_user(settings):
    return OIDCUser(
        "sometoken", {"sub": "admin", settings.OIDC_GROUPS_CLAIM: ["admin"]}
    )


@pytest.fixture
def staff_user(settings):
    return OIDCUser(
        "sometoken",
        {"sub": "staff_user", settings.OIDC_GROUPS_CLAIM: [settings.STAFF_GROUP]},
    )


@pytest.fixture
def user(settings):
    return OIDCUser("sometoken", {"sub": "user", settings.OIDC_GROUPS_CLAIM: []})


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
