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

    data = {"data": {"type": "identities", "attributes": {"idp_id": "foo"}}}

    response = client.post(url, data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_403_FORBIDDEN:
        return

    identity = Identity.objects.get(idp_id="foo")
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


def test_identity_set_interests(db, client, identity_factory, interest_option_factory):
    identity = identity_factory()
    assert identity.interests.count() == 0

    interests = interest_option_factory.create_batch(2)

    url = reverse("identity-detail", args=[identity.pk])

    data = {
        "data": {
            "type": "identities",
            "id": str(identity.pk),
            "attributes": {"first-name": "Foo"},
            "relationships": {
                "interests": {
                    "data": [
                        {"id": str(interests[0].pk), "type": "interest-options"},
                        {"id": str(interests[1].pk), "type": "interest-options"},
                    ]
                }
            },
        }
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    identity.refresh_from_db()
    assert identity.interests.count() == 2
