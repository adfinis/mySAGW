import datetime

import pytest
from django.urls import reverse
from psycopg2.extras import DateRange
from rest_framework import status

from mysagw.identity import models


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_membership_role_detail(db, membership_role, client, expected_status):
    url = reverse("membershiprole-detail", args=[membership_role.pk])

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["id"] == str(membership_role.pk)


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_membership_detail(db, membership, client, expected_status):
    url = reverse("membership-detail", args=[membership.pk])

    response = client.get(url, {"include": "role"})

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["id"] == str(membership.pk)
    assert json["included"][0]["id"] == str(membership.role.pk)


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_membership_role_list(db, client, expected_status, membership_role_factory):
    membership_role_factory.create_batch(3)

    url = reverse("membershiprole-list")

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert len(json["data"]) == models.MembershipRole.objects.count() == 3


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_membership_list(db, client, expected_status, membership_factory):
    membership_factory.create_batch(3)

    url = reverse("membership-list")

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert len(json["data"]) == models.Membership.objects.count() == 3


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_201_CREATED),
        ("admin", status.HTTP_201_CREATED),
    ],
    indirect=["client"],
)
def test_membership_role_create(db, client, expected_status):
    url = reverse("membershiprole-list")

    data = {
        "data": {"type": "membership-roles", "attributes": {"title": {"de": "Foo"}}}
    }

    response = client.post(url, data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_403_FORBIDDEN:
        return

    assert models.MembershipRole.objects.count() == 1
    assert dict(models.MembershipRole.objects.first().title) == {
        "de": "Foo",
        "en": "",
        "fr": "",
    }


@pytest.mark.parametrize(
    "client,identity_is_organisation,organisation_is_organisation,set_lower,set_upper,expected_status",
    [
        ("user", False, True, True, True, status.HTTP_403_FORBIDDEN),
        ("staff", False, True, True, True, status.HTTP_201_CREATED),
        ("admin", False, True, True, True, status.HTTP_201_CREATED),
        ("admin", False, True, False, True, status.HTTP_201_CREATED),
        ("admin", False, True, True, False, status.HTTP_201_CREATED),
        ("admin", False, True, False, False, status.HTTP_201_CREATED),
        ("admin", True, True, True, True, status.HTTP_400_BAD_REQUEST),
        ("admin", False, False, True, True, status.HTTP_400_BAD_REQUEST),
    ],
    indirect=["client"],
)
def test_membership_create(
    db,
    client,
    set_lower,
    set_upper,
    expected_status,
    identity_factory,
    identity_is_organisation,
    organisation_is_organisation,
):
    identity = identity_factory(is_organisation=identity_is_organisation)
    assert identity.modified_by_user != client.user.username
    organisation = identity_factory(is_organisation=organisation_is_organisation)

    url = reverse("membership-list")

    start = datetime.date(2020, 1, 1) if set_lower else None
    end = datetime.date(2020, 12, 31) if set_upper else None
    bounds = "[)" if set_lower else "()"
    next_election = datetime.date(2020, 11, 23)

    data = {
        "data": {
            "type": "memberships",
            "attributes": {
                "time-slot": {"lower": start, "upper": end},
                "next-election": next_election,
            },
            "relationships": {
                "identity": {"data": {"id": str(identity.pk), "type": "identities"}},
                "organisation": {
                    "data": {"id": str(organisation.pk), "type": "identities"}
                },
            },
        }
    }

    response = client.post(url, data=data)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_201_CREATED:
        return

    assert models.Membership.objects.count() == 1
    membership = models.Membership.objects.first()
    assert membership.identity == identity
    assert membership.organisation == organisation
    assert membership.time_slot == DateRange(start, end, bounds)
    assert membership.next_election == next_election
    assert membership.identity.modified_by_user == client.user.username


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_membership_role_update(db, client, expected_status, membership_role_factory):
    membershiprole = membership_role_factory(title="Bar")
    url = reverse("membershiprole-detail", args=[membershiprole.pk])

    data = {
        "data": {
            "type": "membership-roles",
            "id": str(membershiprole.pk),
            "attributes": {"title": {"de": "Foo"}},
        }
    }

    response = client.patch(url, data=data)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["attributes"]["title"] == {"de": "Foo", "en": "", "fr": ""}
    membershiprole.refresh_from_db()
    assert dict(membershiprole.title) == {"de": "Foo", "en": "", "fr": ""}


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_membership_update(db, client, expected_status, membership_factory):
    membership = membership_factory()

    url = reverse("membership-detail", args=[membership.pk])

    data = {
        "data": {
            "type": "memberships",
            "id": str(membership.pk),
            "attributes": {"comment": "Foo"},
            "relationships": {"role": {}},
        },
    }

    response = client.patch(url, data=data)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    membership.refresh_from_db()
    assert membership.role is None
    assert membership.comment == "Foo"


@pytest.mark.parametrize("field", ["identity", "organisation"])
def test_membership_update_failure(db, client, field, membership, identity_factory):
    identity = identity_factory(is_organisation=field == "organisation")

    url = reverse("membership-detail", args=[membership.pk])

    data = {
        "data": {
            "type": "memberships",
            "id": str(membership.pk),
            "relationships": {
                field: {"data": {"type": "identities", "id": str(identity.pk)}},
            },
        }
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.json()["errors"][0]["detail"] == f'Field "{field}" can\'t be modified.'
    )


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_204_NO_CONTENT),
        ("admin", status.HTTP_204_NO_CONTENT),
    ],
    indirect=["client"],
)
def test_membership_role_delete(db, client, expected_status, membership_role_factory):
    membershiprole = membership_role_factory()
    url = reverse("membershiprole-detail", args=[membershiprole.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(models.MembershipRole.DoesNotExist):
            membershiprole.refresh_from_db()


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_204_NO_CONTENT),
        ("admin", status.HTTP_204_NO_CONTENT),
    ],
    indirect=["client"],
)
def test_membership_delete(db, client, expected_status, membership_factory):
    membership = membership_factory()
    assert membership.identity.modified_by_user != client.user.username
    url = reverse("membership-detail", args=[membership.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(models.Membership.DoesNotExist):
            membership.refresh_from_db()
        membership.identity.refresh_from_db()
        assert membership.identity.modified_by_user == client.user.username
