import hashlib
import json

import pytest
from django.core.cache import cache
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from requests.exceptions import HTTPError
from rest_framework import exceptions, status
from rest_framework.exceptions import AuthenticationFailed
from simple_history.models import HistoricalRecords

from mysagw.identity.models import Identity
from mysagw.oidc_auth.authentication import MySAGWAuthenticationBackend


@pytest.mark.parametrize("is_id_token", [True, False])
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
    is_id_token,
    requests_mock,
    mocker,
    settings,
    claims,
):
    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    assert Identity.objects.count() == 0

    mocker.patch.object(
        MySAGWAuthenticationBackend,
        "_client_id_from_token",
        return_value="some_client" if is_id_token else settings.OIDC_RP_CLIENT_ID,
    )

    if not is_id_token:
        claims[settings.OIDC_CLIENT_ID_CLAIM] = settings.OIDC_RP_CLIENT_ID
        requests_mock.post(
            settings.OIDC_OP_INTROSPECT_ENDPOINT, text=json.dumps(claims)
        )

    request = rf.get("/openid", HTTP_AUTHORIZATION=authentication_header)
    HistoricalRecords.thread.request = request

    try:
        result = OIDCAuthentication().authenticate(request)
    except exceptions.AuthenticationFailed:
        assert error
    else:
        if authenticated:
            key = "userinfo" if is_id_token else "introspection"
            user, auth = result
            assert user.is_authenticated
            assert auth == authentication_header.split(" ")[1]
            assert (
                cache.get(f"auth.{key}.{hashlib.sha256(b'Token').hexdigest()}")
                == claims
            )
            assert Identity.objects.count() == (1 if is_id_token else 0)
        else:
            assert result is None


@pytest.mark.parametrize(
    "identity__idp_id,identity__email,",
    [("matching_id", None), (None, "match@example.com"), (None, "MATCH@example.com")],
)
def test_authentication_existing_identity(
    db,
    rf,
    requests_mock,
    mocker,
    settings,
    identity,
    get_claims,
):
    claims = get_claims(
        id_claim="matching_id", groups_claim=[], email_claim="match@example.com"
    )

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    mocker.patch.object(
        MySAGWAuthenticationBackend,
        "_client_id_from_token",
        return_value="some_client",
    )

    assert Identity.objects.count() == 1

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    HistoricalRecords.thread.request = request

    result = OIDCAuthentication().authenticate(request)

    user, auth = result
    assert user.is_authenticated
    assert user.identity == identity
    assert Identity.objects.count() == 1


def test_authentication_multiple_existing_identity(
    db,
    rf,
    requests_mock,
    mocker,
    settings,
    identity_factory,
    get_claims,
    caplog,
):
    identity = identity_factory(idp_id="matching_id")
    identity_factory(email="match@example.com")
    claims = get_claims(
        id_claim="matching_id", groups_claim=[], email_claim="match@example.com"
    )

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    mocker.patch.object(
        MySAGWAuthenticationBackend,
        "_client_id_from_token",
        return_value="some_client",
    )

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
    mocker,
    settings,
):
    requests_mock.get(
        settings.OIDC_OP_USER_ENDPOINT, status_code=status.HTTP_502_BAD_GATEWAY
    )

    mocker.patch.object(
        MySAGWAuthenticationBackend,
        "_client_id_from_token",
        return_value="some_client",
    )

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    with pytest.raises(HTTPError):
        OIDCAuthentication().authenticate(request)


def test_authentication_idp_missing_claim(
    db,
    rf,
    requests_mock,
    mocker,
    settings,
    claims,
):
    settings.OIDC_ID_CLAIM = "missing"
    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    mocker.patch.object(
        MySAGWAuthenticationBackend,
        "_client_id_from_token",
        return_value="some_client",
    )

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    with pytest.raises(AuthenticationFailed):
        OIDCAuthentication().authenticate(request)


def test_authentication_no_client(db, rf, requests_mock, mocker, settings, claims):
    requests_mock.post(settings.OIDC_OP_INTROSPECT_ENDPOINT, text=json.dumps(claims))

    mocker.patch.object(
        MySAGWAuthenticationBackend,
        "_client_id_from_token",
        return_value=settings.OIDC_RP_CLIENT_ID,
    )

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    with pytest.raises(AuthenticationFailed):
        OIDCAuthentication().authenticate(request)


@pytest.mark.parametrize(
    "token,claim",
    [
        ("e30.ewogICJjbGllbnRJZCI6ICJmb28iCn0", "foo"),
        ("e30.ewogICJub3RjbGllbnRJZCI6ICJiYXIiCn0", None),
        ("undefined", None),
        ("e30.undefined", None),
    ],
)
def test_client_id_from_token(token, claim):
    assert MySAGWAuthenticationBackend._client_id_from_token(token) == claim
