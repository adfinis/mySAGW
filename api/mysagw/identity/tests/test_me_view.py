import pytest
from django.urls import reverse
from rest_framework import status

TIMESTAMP = "2017-05-21T11:25:41.123840Z"


@pytest.mark.parametrize(
    "client", ["user"], indirect=["client"],
)
def test_me_retrieve(db, client):
    identity = client.user.identity

    url = reverse("me")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json["data"]["id"] == str(identity.pk)


@pytest.mark.parametrize(
    "client", ["user"], indirect=["client"],
)
def test_identity_update(db, client):
    identity = client.user.identity
    assert identity.first_name is None

    url = reverse("me")

    data = {
        "data": {
            "type": "identities",
            "id": str(identity.pk),
            "attributes": {"first-name": "Foo"},
        }
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK

    identity.refresh_from_db()
    assert identity.first_name == "Foo"
