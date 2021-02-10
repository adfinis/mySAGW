import hashlib
import json

import pytest
from django.core.cache import cache
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from requests.exceptions import HTTPError
from rest_framework import exceptions, status
from rest_framework.exceptions import AuthenticationFailed

from mysagw.identity.models import Identity


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
    settings,
    claims,
):
    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    assert Identity.objects.count() == 0

    if not is_id_token:
        claims["client_id"] = "test_client"
        requests_mock.get(
            settings.OIDC_OP_USER_ENDPOINT, status_code=status.HTTP_401_UNAUTHORIZED
        )
        requests_mock.post(
            settings.OIDC_OP_INTROSPECT_ENDPOINT, text=json.dumps(claims)
        )

    request = rf.get("/openid", HTTP_AUTHORIZATION=authentication_header)
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
            assert Identity.objects.count() == 1
        else:
            assert result is None


@pytest.mark.parametrize(
    "identity__idp_id,identity__email,",
    [("matching_id", None), (None, "match@example.com")],
)
def test_authentication_exiting_identity(
    db,
    rf,
    requests_mock,
    settings,
    identity,
    get_claims,
):
    claims = get_claims(
        id_claim="matching_id", groups_claim=[], email_claim="match@example.com"
    )

    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(claims))

    assert Identity.objects.count() == 1

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    result = OIDCAuthentication().authenticate(request)

    user, auth = result
    assert user.is_authenticated
    assert user.identity == identity
    assert Identity.objects.count() == 1


def test_authentication_idp_502(
    db,
    rf,
    requests_mock,
    settings,
):
    requests_mock.get(
        settings.OIDC_OP_USER_ENDPOINT, status_code=status.HTTP_502_BAD_GATEWAY
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


def test_authentication_no_client(db, rf, requests_mock, settings, claims):
    requests_mock.get(
        settings.OIDC_OP_USER_ENDPOINT, status_code=status.HTTP_401_UNAUTHORIZED
    )
    requests_mock.post(settings.OIDC_OP_INTROSPECT_ENDPOINT, text=json.dumps(claims))

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    with pytest.raises(AuthenticationFailed):
        OIDCAuthentication().authenticate(request)
