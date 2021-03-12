import json

import pyexcel
import pytest
from django.urls import reverse
from rest_framework import status

from mysagw.identity.models import Identity

TIMESTAMP = "2017-05-21T11:25:41.123840Z"


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_identity_detail(db, client, expected_status):
    identity = client.user.identity

    url = reverse("identity-detail", args=[identity.pk])

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["id"] == str(identity.pk)


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_identity_list(db, client, expected_status):
    url = reverse("identity-list")

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert len(json["data"]) == Identity.objects.count() == 3


@pytest.mark.freeze_time(TIMESTAMP)
@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_201_CREATED),
        ("admin", status.HTTP_201_CREATED),
    ],
    indirect=["client"],
)
def test_identity_create(db, client, expected_status):
    url = reverse("identity-list")

    data = {"data": {"type": "identities", "attributes": {"first_name": "foo"}}}

    response = client.post(url, data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_403_FORBIDDEN:
        return

    identity = Identity.objects.get(first_name="foo")
    assert identity.created_by_user == identity.modified_by_user == client.user.username
    json = response.json()
    assert (
        json["data"]["attributes"]["created-at"]
        == json["data"]["attributes"]["modified-at"]
        == TIMESTAMP
    )


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_identity_update(db, client, expected_status, identity_factory):
    identity = identity_factory()
    url = reverse("identity-detail", args=[identity.pk])

    data = {
        "data": {
            "type": "identities",
            "id": str(identity.pk),
            "attributes": {"first-name": "Foo"},
        }
    }

    response = client.patch(url, data=data)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    identity.refresh_from_db()
    assert identity.modified_by_user == client.user.username


@pytest.mark.parametrize(
    "is_organisation,field,error_msg_vars",
    [
        (True, "identity", ["set", "memberships"]),
        (False, "organisation", ["unset", "members"]),
    ],
)
def test_identity_update_is_organisation_membership_failure(
    db, client, membership_factory, is_organisation, field, error_msg_vars
):
    membership = membership_factory(organisation__is_organisation=True)
    instance = getattr(membership, field)

    url = reverse("identity-detail", args=[instance.pk])

    data = {
        "data": {
            "type": "identities",
            "id": str(instance.pk),
            "attributes": {"is-organisation": is_organisation},
        }
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert (
        response.json()["errors"][0]["detail"]
        == f'Can\'t {error_msg_vars[0]} "is_organisation", because there are {error_msg_vars[1]}.'
    )


@pytest.mark.parametrize(
    "identity__organisation_name,identity__is_organisation,expected_status",
    [
        ("AllSafe", True, [status.HTTP_200_OK, status.HTTP_201_CREATED]),
        (None, False, [status.HTTP_400_BAD_REQUEST]),
    ],
)
@pytest.mark.parametrize("update", [True, False])
def test_identity_update_is_organisation_organisation_name_failure(
    db, client, identity, expected_status, update
):
    is_organisation = not identity.is_organisation

    data = {
        "data": {
            "type": "identities",
            "attributes": {
                "is-organisation": is_organisation,
                "organisation-name": identity.organisation_name,
            },
        }
    }

    url = reverse("identity-list")
    method = client.post
    if update:
        data["data"]["id"] = str(identity.pk)
        url = reverse("identity-detail", args=[identity.pk])
        method = client.patch

    response = method(url, data=data)

    assert response.status_code in expected_status

    result = response.json()

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        assert (
            result["errors"][0]["detail"]
            == 'Can\'t set "is_organisation" without an organisation_name.'
        )
        return

    new_identity = Identity.objects.get(pk=result["data"]["id"])
    assert new_identity.organisation_name is None


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_204_NO_CONTENT),
        ("admin", status.HTTP_204_NO_CONTENT),
    ],
    indirect=["client"],
)
def test_identity_delete(db, client, expected_status, identity_factory):
    identity = identity_factory()
    url = reverse("identity-detail", args=[identity.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(Identity.DoesNotExist):
            identity.refresh_from_db()


def test_identity_set_interests(db, client, identity_factory, interest_factory):
    identity = identity_factory()
    assert identity.interests.count() == 0

    interests = interest_factory.create_batch(2)

    url = reverse("identity-detail", args=[identity.pk])

    data = {
        "data": {
            "type": "identities",
            "id": str(identity.pk),
            "attributes": {"first-name": "Foo"},
            "relationships": {
                "interests": {
                    "data": [
                        {"id": str(interests[0].pk), "type": "interests"},
                        {"id": str(interests[1].pk), "type": "interests"},
                    ]
                }
            },
        }
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    identity.refresh_from_db()
    assert identity.interests.count() == 2


@pytest.mark.parametrize(
    "search,expected",
    [
        ("Winst", [0]),
        ("agw@", [0]),
        ("Präsi", [1]),
        ("SAGW", [0, 1, 2, 3]),
        ("@sag", [0, 3]),
        ("123456", [4]),
        ("pHil", [5]),
    ],
)
def test_identity_search(
    db,
    client,
    identity_factory,
    membership_role_factory,
    membership_factory,
    email_factory,
    phone_number_factory,
    interest_factory,
    search,
    expected,
):
    identities = [identity_factory(first_name="Winston", email="sagw@sagw.ch")]

    membership_role = membership_role_factory(title={"de": "PräsidentIn"})
    membership = membership_factory(
        role=membership_role,
        organisation__organisation_name="SAGW",
        organisation__is_organisation=True,
    )
    identities.append(membership.identity)
    identities.append(membership.organisation)

    email = email_factory(email="test@sagw.ch")
    identities.append(email.identity)

    phone = phone_number_factory(phone="+41771234567")
    identities.append(phone.identity)

    interest_identity = identity_factory()
    interest = interest_factory(title={"en": "philosophy"})
    interest_identity.interests.add(interest)
    identities.append(interest_identity)

    url = reverse("identity-list")

    response = client.get(url, {"filter[search]": search})

    assert response.status_code == status.HTTP_200_OK

    expected_ids = sorted([str(identities[ex].pk) for ex in expected])

    json = response.json()

    received_ids = []
    for snippet in json["data"]:
        received_ids.append(snippet["id"])
    received_ids = sorted(received_ids)

    assert expected_ids == received_ids


@pytest.mark.parametrize("is_organisation", [True, False, None])
def test_identity_organisation_filters(db, client, identity_factory, is_organisation):
    identities = list(Identity.objects.all())  # created by the `client` fixture
    assert len(identities) == 3

    organisations = identity_factory.create_batch(3, is_organisation=True)

    expected = identities + organisations
    if is_organisation is True:
        expected = organisations
    elif is_organisation is False:
        expected = identities

    expected_ids = sorted([str(ex.pk) for ex in expected])

    url = reverse("identity-list")

    filters = {}
    if is_organisation in [True, False]:
        filters = {"filter[is-organisation]": is_organisation}

    response = client.get(url, filters)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    received_ids = []
    for identity in json["data"]:
        received_ids.append(identity["id"])
    received_ids = sorted(received_ids)

    assert expected_ids == received_ids


def test_identity_export(
    db, client, identity_factory, phone_number_factory, email_factory
):
    identities = identity_factory.create_batch(10)
    identity_factory()  # create another one to make sure the filtering actually works
    for i in identities:
        phone_number_factory.create_batch(3, identity=i)
        email_factory.create_batch(3, identity=i)
    url = reverse("identity-export")

    data = {"export": [str(i.pk) for i in identities]}

    response = client.post(url, data=json.dumps(data), content_type="application/json")

    assert response.status_code == status.HTTP_200_OK

    sheet = pyexcel.get_sheet(file_type="xlsx", file_content=response.content)
    assert len(sheet.array) == len(identities) + 1
    assert sheet.array[0][0] == "additional_emails"
    assert sheet.array[0][1] == "email"
    assert sheet.array[0][2] == "first_name"
    assert sheet.array[1][0].split() == [
        e.email for e in identities[0].additional_emails.all()
    ]
    assert sheet.array[1][1] == identities[0].email
    assert sheet.array[1][2] == identities[0].first_name
    assert sheet.array[1][4] == identities[0].last_name
    assert sheet.array[1][6].split() == [
        str(p.phone) for p in identities[0].phone_numbers.all()
    ]


@pytest.mark.parametrize(
    "data",
    [
        None,
        "string",
        {},
        {"some-key": [False]},
        {"export": None},
        {"export": [None]},
        {"export": "string"},
        {"export": ["18606ef7-038a-4f14-a5ac-bfa3420de2de"]},
    ],
)
def test_identity_export_failure(db, client, data):
    url = reverse("identity-export")
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["errors"][0]["detail"] == "No identity IDs provided."
