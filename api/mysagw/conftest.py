import io
import re
from functools import partial
from pathlib import Path

import pytest
from django.core.cache import cache
from factory import Faker
from pytest_factoryboy import register
from rest_framework import status
from rest_framework.test import APIClient

from .case import factories as case_factories
from .faker import MultilangProvider, SwissPhoneNumberProvider
from .identity import factories as identity_factories
from .oidc_auth.models import OIDCUser
from .snippets import factories as snippets_factories
from .utils import build_url

Faker.add_provider(MultilangProvider)
Faker.add_provider(SwissPhoneNumberProvider)


TEST_FILES_DIR = Path(__file__).parent.resolve() / "test_files"


register(identity_factories.IdentityFactory)
register(identity_factories.EmailFactory)
register(identity_factories.PhoneNumberFactory)
register(identity_factories.AddressFactory)
register(identity_factories.InterestCategoryFactory)
register(identity_factories.InterestFactory)
register(identity_factories.MembershipRoleFactory)
register(identity_factories.MembershipFactory)
register(snippets_factories.SnippetFactory)
register(case_factories.CaseAccessFactory)


def _get_claims(
    settings,
    id_claim="00000000-0000-0000-0000-000000000000",
    groups_claim=None,
    email_claim="test@example.com",
    first_name_claim=None,
    last_name_claim=None,
    salutation_claim="neutral",
    title_claim=None,
):
    groups_claim = groups_claim if groups_claim else []
    claims = {
        settings.OIDC_ID_CLAIM: id_claim,
        settings.OIDC_GROUPS_CLAIM: groups_claim,
        settings.OIDC_EMAIL_CLAIM: email_claim,
        settings.OIDC_FIRST_NAME_CLAIM: first_name_claim,
        settings.OIDC_LAST_NAME_CLAIM: last_name_claim,
    }
    if title_claim is not None:
        claims[settings.OIDC_TITLE_CLAIM] = title_claim
    if salutation_claim is not None:
        claims[settings.OIDC_SALUTATION_CLAIM] = salutation_claim
    return claims


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
        get_claims(
            id_claim="admin",
            groups_claim=[settings.ADMIN_GROUP],
            email_claim="admin@example.com",
        ),
    )


@pytest.fixture
def staff_user(settings, get_claims):
    return OIDCUser(
        "sometoken",
        get_claims(
            id_claim="staff_user",
            groups_claim=[settings.STAFF_GROUP],
            email_claim="staff@example.com",
        ),
    )


@pytest.fixture
def user(get_claims):
    return OIDCUser(
        "sometoken",
        get_claims(id_claim="user", groups_claim=[], email_claim="user@example.com"),
    )


@pytest.fixture(params=["admin"])
def client(db, user, staff_user, admin_user, request):
    usermap = {"user": user, "staff": staff_user, "admin": admin_user}
    client = APIClient()
    user = usermap[request.param]
    client.force_authenticate(user=user)
    client.user = user
    return client


@pytest.fixture(autouse=True)
def _autoclear_cache():
    cache.clear()


@pytest.fixture(params=["success"])
def _dms_mock(requests_mock, settings, request):
    matcher = re.compile(
        build_url(
            settings.DOCUMENT_MERGE_SERVICE_URL,
            "template",
            ".*",
            "merge",
            trailing=True,
        ),
    )

    response_map = {
        "success": {
            "status_code": status.HTTP_200_OK,
            "headers": {
                "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            },
            "body": io.BytesIO(b"I'm the merged document"),
        },
        "json_error": {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "headers": {"Content-Type": "application/json"},
            "json": {"error": "something went wrong"},
        },
        "text_error": {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "headers": {"Content-Type": "text/plain"},
            "text": "something went wrong",
        },
        "unknown_error": {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "headers": {"Content-Type": "unknown"},
            "text": "something went wrong",
        },
    }

    requests_mock.post(matcher, **response_map[request.param])


@pytest.fixture
def _caluma_files_mock(requests_mock):
    for file, content_type in [
        ("small.png", "image/png"),
        ("big.png", "image/png"),
        ("long.png", "image/png"),
        ("wide.png", "image/png"),
        ("test.pdf", "application/pdf"),
        ("test_encrypted.pdf", "application/pdf"),
    ]:
        with (TEST_FILES_DIR / file).open("rb") as f:
            data = f.read()

        requests_mock.get(
            f"https://mysagw.local/caluma-media/download-url-{file}",
            status_code=status.HTTP_200_OK,
            content=data,
            headers={"CONTENT-TYPE": content_type},
        )


@pytest.fixture
def graphql_mock(requests_mock):
    def mockit(id_data, data):
        def json_callback(request, context):
            if request.json()["query"].startswith("query DocumentId"):
                return id_data
            return data

        requests_mock.post(
            "http://testserver/graphql",
            status_code=200,
            json=json_callback,
        )

    return mockit
