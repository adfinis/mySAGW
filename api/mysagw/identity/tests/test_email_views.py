import pytest
from django.urls import reverse
from rest_framework import status

from mysagw.identity import models


@pytest.mark.parametrize(
    "client,own,expected_status",
    [
        ("user", False, status.HTTP_404_NOT_FOUND),
        ("user", True, status.HTTP_200_OK),
        ("staff", True, status.HTTP_200_OK),
        ("admin", True, status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_email_detail(db, email, client, own, expected_status):
    if own:
        email.identity = client.user.identity
        email.save()

    url = reverse("email-detail", args=[email.pk])

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["id"] == str(email.pk)


@pytest.mark.parametrize(
    "client,expected_count",
    [
        ("user", 1),
        ("staff", 3),
        ("admin", 3),
    ],
    indirect=["client"],
)
def test_email_list(db, client, expected_count, email_factory):
    email_factory.create_batch(2)
    email_factory(identity=client.user.identity)

    url = reverse("email-list")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == expected_count


def test_email_identity_filters(db, client, email_factory):
    email_factory.create_batch(3)
    expected = email_factory.create_batch(3, identity=client.user.identity)
    expected_ids = sorted([str(ex.pk) for ex in expected])

    url = reverse("email-list")

    response = client.get(url, {"filter[identity]": client.user.identity.pk})

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    received_ids = []
    for email in json["data"]:
        received_ids.append(email["id"])
    received_ids = sorted(received_ids)

    assert expected_ids == received_ids


@pytest.mark.parametrize(
    "client,own,expected_status",
    [
        ("user", False, status.HTTP_403_FORBIDDEN),
        ("user", True, status.HTTP_201_CREATED),
        ("staff", True, status.HTTP_201_CREATED),
        ("admin", True, status.HTTP_201_CREATED),
    ],
    indirect=["client"],
)
def test_email_create(db, identity, client, own, expected_status):
    if own:
        client.user.identity = identity
    assert identity.modified_by_user != client.user.username

    url = reverse("email-list")

    data = {
        "data": {
            "type": "additional-emails",
            "attributes": {"email": "test@example.com"},
            "relationships": {
                "identity": {"data": {"id": str(identity.pk), "type": "identities"}},
            },
        }
    }

    response = client.post(url, data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_403_FORBIDDEN:
        return

    assert models.Email.objects.count() == 1
    email = models.Email.objects.first()
    assert email.email == "test@example.com"
    identity.refresh_from_db()
    assert identity.modified_by_user == client.user.username


def test_email_create_with_includes(db, email_factory, client):
    email = email_factory()

    url = f"{reverse('email-list')}?include=identity&include=identity.additional_emails"

    data = {
        "data": {
            "type": "additional-emails",
            "attributes": {"email": "test@example.com"},
            "relationships": {
                "identity": {
                    "data": {"id": str(email.identity.pk), "type": "identities"}
                },
            },
        }
    }

    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED

    assert models.Email.objects.count() == 2
    new = models.Email.objects.get(pk=response.json()["data"]["id"])
    assert new != email
    assert new.email == "test@example.com"
    email.refresh_from_db()

    # assert includes
    json = response.json()
    assert len(json["included"]) == 2
    identity = json["included"][1]
    assert identity["type"] == "identities"
    assert identity["id"] == str(email.identity.pk)


@pytest.mark.parametrize(
    "client,own,expected_status",
    [
        ("user", False, status.HTTP_404_NOT_FOUND),
        ("user", True, status.HTTP_200_OK),
        ("staff", True, status.HTTP_200_OK),
        ("admin", True, status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_email_update(db, client, own, expected_status, email):
    assert email.identity.modified_by_user != client.user.username

    email.description = "Bar"
    if own:
        email.identity = client.user.identity
    email.save()

    url = reverse("email-detail", args=[email.pk])

    data = {
        "data": {
            "type": "additional-emails",
            "id": str(email.pk),
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

    email.refresh_from_db()
    email.identity.refresh_from_db()

    assert email.description.de == "Foo"
    assert email.identity.modified_by_user == client.user.username


@pytest.mark.parametrize(
    "client,own,expected_status",
    [
        ("user", False, status.HTTP_404_NOT_FOUND),
        ("user", True, status.HTTP_204_NO_CONTENT),
        ("staff", True, status.HTTP_204_NO_CONTENT),
        ("admin", True, status.HTTP_204_NO_CONTENT),
    ],
    indirect=["client"],
)
def test_email_delete(db, client, own, expected_status, email_factory):
    main_email = email_factory()
    other_email = email_factory(identity=main_email.identity)
    assert other_email.identity.modified_by_user != client.user.username

    if own:
        client.user.identity = other_email.identity

    url = reverse("email-detail", args=[other_email.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(models.Email.DoesNotExist):
            other_email.refresh_from_db()

        other_email.identity.refresh_from_db()
        assert other_email.identity.modified_by_user == client.user.username
