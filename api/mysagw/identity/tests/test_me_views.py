import pytest
from django.urls import reverse
from rest_framework import status

TIMESTAMP = "2017-05-21T11:25:41.123840Z"


@pytest.mark.parametrize(
    "client",
    ["user"],
    indirect=["client"],
)
def test_me_retrieve(db, client, interest_factory):
    identity = client.user.identity

    private_interest = interest_factory(category__public=False)
    public_interest = interest_factory(category__public=True)

    identity.interests.add(private_interest, public_interest)

    url = reverse("me")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json["data"]["id"] == str(identity.pk)
    assert len(json["data"]["relationships"]["interests"]["data"]) == 1
    assert json["data"]["relationships"]["interests"]["data"][0]["id"] == str(
        public_interest.pk,
    )


@pytest.mark.parametrize(
    "client",
    ["user"],
    indirect=["client"],
)
def test_my_orgs_list(db, client, membership_factory, identity_factory):
    identity = client.user.identity

    expected = membership_factory.create_batch(3, identity=identity, authorized=True)
    expected += membership_factory.create_batch(3, identity=identity, authorized=False)
    membership_factory.create_batch(3, identity=identity_factory(), authorized=False)

    expected_map = {str(m.organisation.pk): m.authorized for m in expected}

    url = reverse("my-orgs-list")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == len(expected_map)
    for membership in json["data"]:
        assert (
            membership["attributes"]["is-authorized"] == expected_map[membership["id"]]
        )


@pytest.mark.parametrize(
    "client",
    ["user"],
    indirect=["client"],
)
def test_me_update(db, client):
    identity = client.user.identity
    assert identity.first_name is None

    url = reverse("me")

    data = {
        "data": {
            "type": "identities",
            "id": str(identity.pk),
            "attributes": {"first-name": "Foo"},
        },
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK

    identity.refresh_from_db()
    assert identity.first_name == "Foo"


@pytest.mark.parametrize(
    "client",
    ["user"],
    indirect=["client"],
)
@pytest.mark.parametrize(
    "authorized",
    [True, False],
)
def test_my_orgs_update(db, client, authorized, membership_factory):
    identity = client.user.identity
    membership = membership_factory(identity=identity, authorized=authorized)

    url = reverse("my-orgs-detail", args=[str(membership.organisation.pk)])

    data = {
        "data": {
            "type": "identities",
            "id": str(membership.organisation.pk),
            "attributes": {"organisation-name": "Foo"},
        },
    }

    response = client.patch(url, data=data)

    if not authorized:
        assert response.status_code == status.HTTP_403_FORBIDDEN
        return

    assert response.status_code == status.HTTP_200_OK
    membership.organisation.refresh_from_db()
    assert membership.organisation.organisation_name == "Foo"


@pytest.mark.parametrize(
    "client",
    ["user"],
    indirect=["client"],
)
@pytest.mark.parametrize(
    "public,expected_status",
    [(True, status.HTTP_200_OK), (False, status.HTTP_400_BAD_REQUEST)],
)
def test_me_set_interests(db, client, interest_factory, public, expected_status):
    identity = client.user.identity
    interest = interest_factory(category__public=False)
    identity.interests.add(interest)
    assert identity.interests.count() == 1

    interests = interest_factory.create_batch(2, category__public=public)

    url = reverse("me")

    data = {
        "data": {
            "type": "identities",
            "id": str(identity.pk),
            "relationships": {
                "interests": {
                    "data": [
                        {"id": str(interests[0].pk), "type": "interests"},
                        {"id": str(interests[1].pk), "type": "interests"},
                    ],
                },
            },
        },
    }

    response = client.patch(url, data=data)

    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        identity.refresh_from_db()
        assert identity.interests.count() == 3


@pytest.mark.parametrize(
    "client",
    ["user"],
    indirect=["client"],
)
def test_my_orgs_delete_failure(db, client):
    url = reverse("my-orgs-detail", args=["foo"])

    response = client.delete(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
