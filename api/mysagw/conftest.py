import importlib
import inspect

import pytest
from django.core.cache import cache
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .oidc_auth.models import OIDCUser


def register_module(module):
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            # name needs to be compatible with
            # `rest_framework.routers.SimpleRouter` naming for easier testing
            base_name = obj._meta.model._meta.object_name.lower()
            register(obj, base_name)


register_module(importlib.import_module(".identity.factories", "mysagw"))


@pytest.fixture
def admin_groups():
    return ["admin"]


# @pytest.fixture
# def user(settings, admin_groups):
#     return OIDCUser("sometoken", {"sub": "user", settings.OIDC_GROUPS_CLAIM: ["group"]})


@pytest.fixture
def admin_user(settings, admin_groups):
    return OIDCUser(
        "sometoken", {"sub": "admin", settings.OIDC_GROUPS_CLAIM: admin_groups}
    )


# @pytest.fixture
# def client(db):
#     client = APIClient()
#     return client


@pytest.fixture
def admin_client(db, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture(scope="function", autouse=True)
def _autoclear_cache():
    cache.clear()
