from uuid import uuid4

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from mysagw.case import email_texts, models


@pytest.mark.parametrize(
    "filter_id,expected_count",
    [
        (None, 4),
        ("00000000-0000-0000-0000-000000000000", 2),
        ("11111111-1111-1111-1111-111111111111", 1),
    ],
)
def test_case_list(
    db, client, filter_id, expected_count, identity_factory, case_access_factory
):
    identity_0 = identity_factory(idp_id="00000000-0000-0000-0000-000000000000")
    identity_1 = identity_factory(idp_id="11111111-1111-1111-1111-111111111111")
    case_access_factory.create_batch(2, identity=identity_0, email=None)
    case_access_factory(identity=identity_1, email=None)
    case_access_factory()

    url = reverse("caseaccess-list")

    response = client.get(url, {"filter[idpId]": filter_id} if filter_id else None)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "client,has_access,identity_exists,expected_status",
    [
        ("user", False, False, status.HTTP_403_FORBIDDEN),
        ("user", True, False, status.HTTP_201_CREATED),
        ("staff", False, False, status.HTTP_403_FORBIDDEN),
        ("admin", False, False, status.HTTP_201_CREATED),
        ("admin", False, True, status.HTTP_201_CREATED),
    ],
    indirect=["client"],
)
def test_case_create(
    db,
    case_access,
    client,
    identity,
    has_access,
    identity_exists,
    expected_status,
    mailoutbox,
):
    url = reverse("caseaccess-list")

    data = {
        "data": {
            "type": "case-accesses",
            "attributes": {"email": "test@example.com", "case-id": uuid4()},
            "relationships": {
                "identity": {},
            },
        }
    }

    if has_access:
        case_access.email = None
        case_access.identity = client.user.identity
        case_access.save()
        data["data"]["attributes"]["case-id"] = case_access.case_id
        data["data"]["attributes"]["email"] = identity.email
    elif identity_exists:
        data["data"]["attributes"]["email"] = client.user.identity.email

    response = client.post(url, data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_403_FORBIDDEN:
        assert len(mailoutbox) == 0
        return

    assert models.CaseAccess.objects.count() == 2
    result = response.json()
    case_access = models.CaseAccess.objects.get(pk=result["data"]["id"])
    if identity_exists:
        assert case_access.email is None
        assert case_access.identity == client.user.identity
    elif has_access:
        assert case_access.email is None
        assert case_access.identity == identity
    else:
        assert case_access.email == "test@example.com"
        assert case_access.identity is None
        assert len(mailoutbox) == 1
        expected_body = email_texts.EMAIL_BODY_INVITE_REGISTER.format(
            link=settings.SELF_URI,
        )
        assert mailoutbox[0].body == expected_body

    if identity_exists or has_access:
        assert len(mailoutbox) == 1
        expected_body = email_texts.EMAIL_INVITE_BODIES[
            case_access.identity.language
        ].format(
            first_name=case_access.identity.first_name or "",
            last_name=case_access.identity.last_name or "",
            link=f"{settings.SELF_URI}/cases/{case_access.case_id}",
        )
        assert mailoutbox[0].body == expected_body


def test_case_create_already_exists(db, case_access_factory, client):
    case_access = case_access_factory(
        email=None, identity=client.user.identity, case_id=uuid4()
    )

    data = {
        "data": {
            "type": "case-accesses",
            "attributes": {
                "email": client.user.identity.email,
                "case-id": str(case_access.case_id),
            },
            "relationships": {
                "identity": {},
            },
        }
    }

    url = reverse("caseaccess-list")

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["errors"][0]["detail"] == "Case already exists!"


@pytest.mark.parametrize(
    "client,has_access,expected_status",
    [
        ("user", False, status.HTTP_404_NOT_FOUND),
        ("user", True, status.HTTP_204_NO_CONTENT),
        ("staff", False, status.HTTP_404_NOT_FOUND),
        ("admin", False, status.HTTP_204_NO_CONTENT),
    ],
    indirect=["client"],
)
def test_case_delete(db, client, has_access, expected_status, case_access_factory):
    case_access = case_access_factory()

    if has_access:
        case_access_factory(identity=client.user.identity, case_id=case_access.case_id)

    url = reverse("caseaccess-detail", args=[case_access.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(models.CaseAccess.DoesNotExist):
            case_access.refresh_from_db()
