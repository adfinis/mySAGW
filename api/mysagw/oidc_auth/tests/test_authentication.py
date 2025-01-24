import hashlib
import json
from uuid import uuid4

import pytest
from django.core.cache import cache
from django.urls import reverse
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from requests.exceptions import HTTPError
from rest_framework import exceptions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIClient
from simple_history.models import HistoricalRecords

from mysagw.identity.models import Identity


@pytest.mark.parametrize("is_client_grant_token", [True, False])
@pytest.mark.parametrize(
    "authentication_header,authenticated,error",
    [
        ("", False, False),
        ("Bearer", False, True),
        ("Bearer Too many params", False, True),
        ("Basic Auth", False, True),
        ("Bearer Token", True, False),
    ],
)
def test_authentication(
    db,
    rf,
    authentication_header,
    authenticated,
    error,
    is_client_grant_token,
    requests_mock,
    settings,
    claims,
):
    assert Identity.objects.count() == 0

    if is_client_grant_token:
        claims[settings.OIDC_CLIENT_GRANT_USERNAME_CLAIM] = (
            settings.OIDC_RP_CLIENT_USERNAME
        )

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION=authentication_header)
    HistoricalRecords.thread.request = request

    try:
        result = OIDCAuthentication().authenticate(request)
    except exceptions.AuthenticationFailed:
        assert error
    else:
        if authenticated:
            user, auth = result
            assert user.is_authenticated
            assert auth == authentication_header.split(" ")[1]
            assert (
                cache.get(f"auth.userinfo.{hashlib.sha256(b'Token').hexdigest()}")
                == claims
            )
            assert Identity.objects.count() == (0 if is_client_grant_token else 1)
        else:
            assert result is None


@pytest.mark.parametrize("email_claim", ["foo@example.com", "bar@example.com"])
@pytest.mark.parametrize("first_name_claim", ["Winston", "Hagbard"])
@pytest.mark.parametrize("last_name_claim", ["Smith", "Celine"])
@pytest.mark.parametrize("salutation_claim", ["neutral", "Mrs."])
@pytest.mark.parametrize("title_claim", [None, "Prof. Dr."])
def test_authentication_identity_create(
    db,
    rf,
    requests_mock,
    settings,
    get_claims,
    email_claim,
    first_name_claim,
    last_name_claim,
    salutation_claim,
    title_claim,
):
    idp_id = str(uuid4())
    claims = get_claims(
        id_claim=idp_id,
        email_claim=email_claim,
        first_name_claim=first_name_claim,
        last_name_claim=last_name_claim,
        salutation_claim=salutation_claim,
        title_claim=title_claim,
    )
    assert Identity.objects.count() == 0

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    HistoricalRecords.thread.request = request

    result = OIDCAuthentication().authenticate(request)
    user, auth = result
    assert user.is_authenticated
    assert cache.get(f"auth.userinfo.{hashlib.sha256(b'Token').hexdigest()}") == claims
    assert Identity.objects.count() == 1

    identity = Identity.objects.get(idp_id=idp_id)

    assert [
        identity.email,
        identity.first_name,
        identity.last_name,
        Identity.SALUTATION_LOCALIZED_MAP[identity.salutation]["en"],
        Identity.TITLE_LOCALIZED_MAP[identity.title]["en"],
    ] == [
        email_claim,
        first_name_claim,
        last_name_claim,
        "" if salutation_claim == "neutral" else salutation_claim,
        title_claim if title_claim else "",
    ]


@pytest.mark.parametrize(
    "identity__email,identity__first_name,identity__last_name,identity__salutation,identity__title",
    [
        (
            "foo@example.com",
            "Winston",
            "Smith",
            Identity.SALUTATION_NEUTRAL,
            Identity.TITLE_NONE,
        )
    ],
)
@pytest.mark.parametrize("email_claim", ["bar@example.com"])
@pytest.mark.parametrize("first_name_claim", ["Hagbard"])
@pytest.mark.parametrize("last_name_claim", ["Celine"])
@pytest.mark.parametrize("salutation_claim", ["Mrs."])
@pytest.mark.parametrize("title_claim", ["Prof. Dr."])
def test_authentication_identity_update_existing_identity(
    db,
    rf,
    requests_mock,
    settings,
    get_claims,
    identity,
    email_claim,
    first_name_claim,
    last_name_claim,
    salutation_claim,
    title_claim,
):
    claims = get_claims(
        id_claim=str(identity.idp_id),
        email_claim=email_claim,
        first_name_claim=first_name_claim,
        last_name_claim=last_name_claim,
        salutation_claim=salutation_claim,
        title_claim=title_claim,
    )
    assert Identity.objects.count() == 1

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    HistoricalRecords.thread.request = request

    result = OIDCAuthentication().authenticate(request)
    assert result[0].is_authenticated
    assert Identity.objects.count() == 1

    identity.refresh_from_db()

    # only the email should be updated
    assert identity.email == email_claim
    assert identity.first_name == "Winston"
    assert identity.last_name == "Smith"
    assert identity.salutation == Identity.SALUTATION_NEUTRAL
    assert identity.title == Identity.TITLE_NONE


def test_authentication_multiple_existing_identity(
    db,
    rf,
    requests_mock,
    settings,
    identity_factory,
    get_claims,
    caplog,
):
    identity = identity_factory(idp_id="matching_id")
    identity_factory(email="match@example.com")
    claims = get_claims(
        id_claim="matching_id",
        groups_claim=[],
        email_claim="match@example.com",
    )

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    assert Identity.objects.count() == 2

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    HistoricalRecords.thread.request = request

    result = OIDCAuthentication().authenticate(request)

    user, auth = result
    assert user.is_authenticated
    assert user.identity == identity
    assert Identity.objects.count() == 2
    assert (
        caplog.records[0].msg
        == "Found one Identity with same idp_id and one with same email. Matching on idp_id."
    )


def test_authentication_idp_502(
    db,
    rf,
    requests_mock,
    settings,
):
    requests_mock.get(
        settings.OIDC_OP_USER_ENDPOINT,
        status_code=status.HTTP_502_BAD_GATEWAY,
    )

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    with pytest.raises(HTTPError):
        OIDCAuthentication().authenticate(request)


def test_authentication_idp_missing_claim(
    db,
    rf,
    requests_mock,
    settings,
    claims,
):
    settings.OIDC_ID_CLAIM = "missing"
    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    with pytest.raises(AuthenticationFailed):
        OIDCAuthentication().authenticate(request)


@pytest.mark.parametrize(
    "identity__is_organisation,identity__organisation_name,identity__email",
    [
        (True, "org name", "email@example.com"),
    ],
)
def test_authentication_email_already_used(
    db, rf, requests_mock, settings, get_claims, identity
):
    idp_id = str(uuid4())
    claims = get_claims(
        id_claim=idp_id,
        email_claim="email@example.com",
        first_name_claim="Winston",
        last_name_claim="Smith",
        salutation_claim="neutral",
        title_claim=None,
    )
    assert Identity.objects.count() == 1

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    url = reverse("me")

    client = APIClient()
    response = client.get(url, HTTP_AUTHORIZATION="Bearer Token")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "errors": [
            {
                "detail": "Can't create Identity, because there is already an organisation with this email address.",
                "status": "400",
                "source": {"pointer": "/data"},
                "code": "invalid",
            }
        ]
    }
