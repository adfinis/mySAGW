import pytest
from django.urls import reverse
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
def test_address_detail(db, address, client, expected_status):
    url = reverse("address-detail", args=[address.pk])

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["id"] == str(address.pk)


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_address_list(db, client, expected_status, address_factory):
    address_factory.create_batch(3)

    url = reverse("address-list")

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert len(json["data"]) == models.Address.objects.count() == 3


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_201_CREATED),
        ("admin", status.HTTP_201_CREATED),
    ],
    indirect=["client"],
)
def test_address_create(db, identity, client, expected_status):
    assert identity.modified_by_user != client.user.username

    url = reverse("address-list")

    data = {
        "data": {
            "type": "addresses",
            "attributes": {
                "street_and_number": "Hauptstrasse 23",
                "postcode": "3000",
                "town": "Bern",
                "default": False,
            },
            "relationships": {
                "identity": {"data": {"id": str(identity.pk), "type": "identities"}},
            },
        }
    }

    response = client.post(url, data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_403_FORBIDDEN:
        return

    assert models.Address.objects.count() == 1
    address = models.Address.objects.first()
    assert address.postcode == "3000"
    # As it's the only address for this identity, `default` will be set to `True`
    # regardless of the POST data
    assert address.default is True

    identity.refresh_from_db()
    assert identity.modified_by_user == client.user.username


def test_address_create_new_default(db, address_factory, client):
    address = address_factory()
    other_address = address_factory()

    url = f"{reverse('address-list')}?include=identity&include=identity.addresses"

    data = {
        "data": {
            "type": "addresses",
            "attributes": {
                "street_and_number": "Hauptstrasse 23",
                "postcode": "3000",
                "town": "Bern",
                "default": True,
            },
            "relationships": {
                "identity": {
                    "data": {"id": str(address.identity.pk), "type": "identities"}
                },
            },
        }
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED

    assert models.Address.objects.count() == 3
    new = models.Address.objects.get(pk=response.json()["data"]["id"])
    assert new != address
    assert new.postcode == "3000"
    address.refresh_from_db()
    other_address.refresh_from_db()
    assert new.default is True
    assert address.default is False
    assert other_address.default is True

    # assert includes
    json = response.json()
    assert len(json["included"]) == 2
    incl_address, incl_identity = json["included"]
    assert incl_address["type"] == "addresses"
    assert incl_address["attributes"]["default"] is False
    assert incl_identity["type"] == "identities"
    assert incl_identity["id"] == str(address.identity.pk)


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_address_update(db, client, expected_status, address_factory):
    address = address_factory(description="Bar")
    assert address.identity.modified_by_user != client.user.username

    url = reverse("address-detail", args=[address.pk])

    data = {
        "data": {
            "type": "addresses",
            "id": str(address.pk),
            "attributes": {"description": {"de": "Foo"}},
        }
    }

    response = client.patch(url, data=data)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["attributes"]["description"] == {
        "de": "Foo",
        "en": "",
        "fr": "",
    }

    address.refresh_from_db()
    address.identity.refresh_from_db()

    assert dict(address.description) == {"de": "Foo", "en": "", "fr": ""}
    assert address.identity.modified_by_user == client.user.username


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_204_NO_CONTENT),
        ("admin", status.HTTP_204_NO_CONTENT),
    ],
    indirect=["client"],
)
def test_address_delete(db, client, expected_status, address_factory):
    main_address = address_factory()
    other_address = address_factory(identity=main_address.identity, default=False)
    assert other_address.identity.modified_by_user != client.user.username

    url = reverse("address-detail", args=[other_address.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(models.Address.DoesNotExist):
            other_address.refresh_from_db()

        other_address.identity.refresh_from_db()
        assert other_address.identity.modified_by_user == client.user.username


def test_country_options(client):
    url = reverse("address-list")
    response = client.options(url)
    json = response.json()
    assert json["data"]["actions"]["POST"]["country"]["choices"][0] == {
        "value": "AF",
        "display_name": "Afghanistan",
    }
