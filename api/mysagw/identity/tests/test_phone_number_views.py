import pytest
from django.urls import reverse
from rest_framework import status

from mysagw.identity import models


@pytest.mark.parametrize(
    "client,own,expected_status",
    [
        ("user", False, status.HTTP_404_NOT_FOUND),
        ("user", True, status.HTTP_200_OK),
        ("staff", False, status.HTTP_200_OK),
        ("admin", False, status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_phone_number_detail(db, phone_number, client, own, expected_status):
    if own:
        phone_number.identity = client.user.identity
        phone_number.save()

    url = reverse("phonenumber-detail", args=[phone_number.pk])

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["id"] == str(phone_number.pk)


@pytest.mark.parametrize(
    "client,expected_count",
    [
        ("user", 1),
        ("staff", 3),
        ("admin", 3),
    ],
    indirect=["client"],
)
def test_phone_number_list(db, client, expected_count, phone_number_factory):
    phone_number_factory.create_batch(2)
    phone_number_factory(identity=client.user.identity)

    url = reverse("phonenumber-list")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "client,own,expected_status",
    [
        ("user", False, status.HTTP_403_FORBIDDEN),
        ("user", True, status.HTTP_201_CREATED),
        ("staff", False, status.HTTP_201_CREATED),
        ("admin", False, status.HTTP_201_CREATED),
    ],
    indirect=["client"],
)
def test_phone_number_create(db, identity, client, own, expected_status):
    if own:
        client.user.identity = identity
    assert identity.modified_by_user != client.user.id

    url = reverse("phonenumber-list")

    data = {
        "data": {
            "type": "phone-numbers",
            "attributes": {"phone": "+41791234567", "default": False},
            "relationships": {
                "identity": {"data": {"id": str(identity.pk), "type": "identities"}},
            },
        }
    }

    response = client.post(url, data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_403_FORBIDDEN:
        return

    assert models.PhoneNumber.objects.count() == 1
    phone_number = models.PhoneNumber.objects.first()
    assert phone_number.phone == "+41791234567"
    # As it's the only phone number for this identity, `default` will be set to `True`
    # regardless of the POST data
    assert phone_number.default is True

    identity.refresh_from_db()
    assert identity.modified_by_user == client.user.id


def test_phone_number_create_new_default(db, phone_number_factory, client):
    phone_number = phone_number_factory()
    other_phone_number = phone_number_factory()

    url = (
        f"{reverse('phonenumber-list')}?include=identity&include=identity.phone-numbers"
    )

    data = {
        "data": {
            "type": "phone-numbers",
            "attributes": {"phone": "+41791234567", "default": True},
            "relationships": {
                "identity": {
                    "data": {"id": str(phone_number.identity.pk), "type": "identities"}
                },
            },
        }
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED

    assert models.PhoneNumber.objects.count() == 3
    new = models.PhoneNumber.objects.get(pk=response.json()["data"]["id"])
    assert new != phone_number
    assert new.phone == "+41791234567"
    phone_number.refresh_from_db()
    other_phone_number.refresh_from_db()
    assert new.default is True
    assert phone_number.default is False
    assert other_phone_number.default is True

    # assert includes
    json = response.json()
    assert len(json["included"]) == 2
    incl_identity, incl_phone = json["included"]
    assert incl_phone["type"] == "phone-numbers"
    assert incl_phone["attributes"]["default"] is False
    assert incl_identity["type"] == "identities"
    assert incl_identity["id"] == str(phone_number.identity.pk)


@pytest.mark.parametrize(
    "client,own,expected_status",
    [
        ("user", False, status.HTTP_404_NOT_FOUND),
        ("user", True, status.HTTP_200_OK),
        ("staff", False, status.HTTP_200_OK),
        ("admin", False, status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_phone_number_update(db, client, own, expected_status, phone_number):
    assert phone_number.identity.modified_by_user != client.user.id

    phone_number.description = "Bar"
    if own:
        phone_number.identity = client.user.identity
    phone_number.save()

    url = reverse("phonenumber-detail", args=[phone_number.pk])

    data = {
        "data": {
            "type": "phone-numbers",
            "id": str(phone_number.pk),
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

    phone_number.refresh_from_db()
    phone_number.identity.refresh_from_db()

    assert dict(phone_number.description) == {"de": "Foo", "en": "", "fr": ""}
    assert phone_number.identity.modified_by_user == client.user.id


def test_phone_number_update_unset_default(db, client, phone_number):
    assert phone_number.default

    url = reverse("phonenumber-detail", args=[phone_number.pk])

    data = {
        "data": {
            "type": "phone-numbers",
            "id": str(phone_number.pk),
            "attributes": {"default": False},
        }
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.json()["errors"][0]["detail"]
        == 'Can\'t unset "default". Set another default instead.'
    )


@pytest.mark.parametrize(
    "client,own,expected_status",
    [
        ("user", False, status.HTTP_404_NOT_FOUND),
        ("user", True, status.HTTP_204_NO_CONTENT),
        ("staff", False, status.HTTP_204_NO_CONTENT),
        ("admin", False, status.HTTP_204_NO_CONTENT),
    ],
    indirect=["client"],
)
def test_phone_number_delete(db, client, own, expected_status, phone_number_factory):
    main_phone_number = phone_number_factory()
    other_phone_number = phone_number_factory(
        identity=main_phone_number.identity, default=False
    )
    assert other_phone_number.identity.modified_by_user != client.user.id

    if own:
        client.user.identity = other_phone_number.identity

    url = reverse("phonenumber-detail", args=[other_phone_number.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(models.PhoneNumber.DoesNotExist):
            other_phone_number.refresh_from_db()

        other_phone_number.identity.refresh_from_db()
        assert other_phone_number.identity.modified_by_user == client.user.id


@pytest.mark.parametrize("has_other", [True, False])
def test_phone_number_delete_default(db, client, phone_number_factory, has_other):
    main_phone_number = phone_number_factory()
    if has_other:
        phone_number_factory(identity=main_phone_number.identity, default=False)

    url = reverse("phonenumber-detail", args=[main_phone_number.pk])

    response = client.delete(url)

    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
        if has_other
        else status.HTTP_204_NO_CONTENT
    )

    if response.status_code == status.HTTP_204_NO_CONTENT:
        with pytest.raises(models.PhoneNumber.DoesNotExist):
            main_phone_number.refresh_from_db()
    else:
        assert (
            response.json()["errors"][0]["detail"]
            == "Can't delete the default entry. Set another entry as default first."
        )
