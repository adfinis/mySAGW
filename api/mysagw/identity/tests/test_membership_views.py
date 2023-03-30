import datetime

import pytest
from django.conf import settings
from django.urls import reverse
from psycopg2.extras import DateRange
from rest_framework import status
from syrupy import filters

from mysagw.identity import models


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_200_OK),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_membership_role_detail(db, membership_role, client, expected_status):
    url = reverse("membershiprole-detail", args=[membership_role.pk])

    response = client.get(url)

    assert response.status_code == expected_status

    json = response.json()
    assert json["data"]["id"] == str(membership_role.pk)


@pytest.mark.parametrize(
    "client,own,expected_status",
    [
        ("user", False, status.HTTP_403_FORBIDDEN),
        ("user", True, status.HTTP_403_FORBIDDEN),
        ("staff", False, status.HTTP_200_OK),
        ("admin", False, status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_membership_detail(db, membership, client, own, expected_status):
    if own:
        membership.identity = client.user.identity
        membership.save()

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
        ("user", status.HTTP_200_OK),
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

    json = response.json()
    assert len(json["data"]) == models.MembershipRole.objects.count() == 3


@pytest.mark.parametrize("lang", ["de", "fr"])
def test_membership_role_list_ordering(db, client, lang, membership_role_factory):
    role1 = membership_role_factory(title={"de": "aaa", "fr": "bbb"})
    role2 = membership_role_factory(title={"de": "bbb", "fr": "aaa"})

    expected = [str(role1.pk), str(role2.pk)]
    if lang == "fr":
        expected = [str(role2.pk), str(role1.pk)]

    url = reverse("membershiprole-list")

    response = client.get(url, HTTP_ACCEPT_LANGUAGE=lang)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    assert len(json["data"]) == 2
    assert json["data"][0]["id"] == expected[0]
    assert json["data"][1]["id"] == expected[1]


@pytest.mark.parametrize(
    "client,expected_count,expected_status",
    [
        ("user", 0, status.HTTP_403_FORBIDDEN),
        ("staff", 3, status.HTTP_200_OK),
        ("admin", 3, status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_membership_list(
    db, client, expected_count, expected_status, membership_factory
):
    membership_factory.create_batch(2)
    membership_factory(identity=client.user.identity)

    url = reverse("membership-list")

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        json = response.json()
        assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "client,expected_count",
    [
        ("user", 1),
        ("staff", 1),
        ("admin", 1),
    ],
    indirect=["client"],
)
def test_my_membership_list(db, client, expected_count, membership_factory):
    membership_factory.create_batch(2)
    membership_factory(identity=client.user.identity)

    url = reverse("my-memberships-list")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == expected_count


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
    "title",
    [
        {"de": ""},
        {"de": None},
        {"en": "Foo"},
        {},
    ],
)
def test_membership_role_empty_failure(db, client, title):
    url = reverse("membershiprole-list")
    data = {"data": {"type": "membership-roles", "attributes": {"title": title}}}

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.json()["errors"][0]["detail"]
        == f'Title must be set for language: "{settings.LANGUAGE_CODE}"'
    )


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
    assert identity.modified_by_user != client.user.id
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
    assert membership.identity.modified_by_user == client.user.id


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_403_FORBIDDEN),
        ("admin", status.HTTP_403_FORBIDDEN),
    ],
    indirect=["client"],
)
def test_my_membership_create(
    db,
    client,
    expected_status,
    identity_factory,
):
    identity = identity_factory(is_organisation=False)
    assert identity.modified_by_user != client.user.id
    organisation = identity_factory(is_organisation=True)

    url = reverse("my-memberships-list")

    data = {
        "data": {
            "type": "memberships",
            "attributes": {
                "time-slot": {"lower": None, "upper": None},
                "next-election": None,
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


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_403_FORBIDDEN),
        ("admin", status.HTTP_403_FORBIDDEN),
    ],
    indirect=["client"],
)
def test_my_membership_update(db, client, expected_status, membership_factory):
    membership = membership_factory()

    url = reverse("my-memberships-detail", args=[membership.pk])

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
    assert membership.identity.modified_by_user != client.user.id
    url = reverse("membership-detail", args=[membership.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(models.Membership.DoesNotExist):
            membership.refresh_from_db()
        membership.identity.refresh_from_db()
        assert membership.identity.modified_by_user == client.user.id


@pytest.mark.parametrize(
    "client",
    ["user"],
    indirect=["client"],
)
def test_my_memberships_delete_failure(db, client):
    url = reverse("my-memberships-detail", args=["foo"])

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_organisation_members(
    db, client, membership_role_factory, membership_factory, identity_factory, snapshot
):
    first_role = membership_role_factory.create(sort=1)
    second_role = membership_role_factory.create(sort=2)
    third_role = membership_role_factory.create(sort=3)
    organisation = identity_factory(is_organisation=True)
    user1 = identity_factory(first_name="User", last_name="1")
    user2 = identity_factory(first_name="User", last_name="2")
    user3 = identity_factory(first_name="User", last_name="3")
    user4 = identity_factory(first_name="User", last_name="4")
    user5 = identity_factory(first_name="User", last_name="5")

    # User1, 2 memberships, 1 inactive
    # second role is highest
    # should be second in list - same highest role as user 3, but last_name comes first
    # in alphabet
    membership_factory.create(
        role=first_role, identity=user1, organisation=organisation
    )
    membership_factory.create(
        role=second_role, identity=user1, organisation=organisation
    )
    membership_factory.create(
        role=third_role,
        identity=user1,
        organisation=organisation,
        time_slot=DateRange(datetime.date(2020, 1, 1), datetime.date(2020, 12, 31)),
    )

    # User2, 3 memberships, 1 inactive
    # third role is highest
    # should be first in list
    membership_factory.create(
        role=second_role, identity=user2, organisation=organisation, inactive=True
    )
    membership_factory.create(
        role=second_role, identity=user2, organisation=organisation
    )
    membership_factory.create(
        role=third_role, identity=user2, organisation=organisation
    )

    # User3, 2 memberships, 1 inactive
    # second role highest
    # should be third in list - same highest role as user 1, but last_name comes after
    # in alphabet
    membership_factory.create(
        role=second_role, identity=user3, organisation=organisation
    )
    membership_factory.create(
        role=third_role, identity=user3, organisation=organisation, inactive=True
    )

    # User4, 1 membership, 1 inactive
    # should be fifth in list
    membership_factory.create(
        role=second_role, identity=user4, organisation=organisation, inactive=True
    )

    # User5, 1 membership, 1 inactive
    # should be fourth in list
    membership_factory.create(
        role=third_role, identity=user5, organisation=organisation, inactive=True
    )

    url = reverse("org-memberships-list")

    response = client.get(url, {"filter[organisation]": str(organisation.pk)})

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 5
    assert json["data"][0]["attributes"]["last-name"] == "2"
    assert json["data"][1]["attributes"]["last-name"] == "1"
    assert json["data"][2]["attributes"]["last-name"] == "3"
    assert json["data"][3]["attributes"]["last-name"] == "5"
    assert json["data"][4]["attributes"]["last-name"] == "4"
    assert json == snapshot(exclude=filters.props("id"))
