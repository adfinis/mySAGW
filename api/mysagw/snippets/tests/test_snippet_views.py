import pytest
from django.urls import reverse
from rest_framework import status

from .. import models


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_snippet_detail(db, client, expected_status, snippet):

    url = reverse("snippet-detail", args=[snippet.pk])

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["id"] == str(snippet.pk)


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_snippet_list(db, client, expected_status, snippet_factory):
    snippet_factory.create_batch(3)

    url = reverse("snippet-list")

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert len(json["data"]) == models.Snippet.objects.count() == 3


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_snippet_update(db, client, expected_status, snippet_factory):
    snippet = snippet_factory(title={"de": "Bar"})
    url = reverse("snippet-detail", args=[snippet.pk])

    data = {
        "data": {
            "type": "snippets",
            "id": str(snippet.pk),
            "attributes": {"title": "Foo"},
        }
    }

    response = client.patch(url, data=data)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    json = response.json()
    assert json["data"]["attributes"]["title"] == "Foo"
    snippet.refresh_from_db()
    assert snippet.title == "Foo"


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_204_NO_CONTENT),
        ("admin", status.HTTP_204_NO_CONTENT),
    ],
    indirect=["client"],
)
def test_snippet_delete(db, client, expected_status, snippet_factory):
    snippet = snippet_factory()
    url = reverse("snippet-detail", args=[snippet.pk])

    response = client.delete(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(models.Snippet.DoesNotExist):
            snippet.refresh_from_db()
        return
    snippet.refresh_from_db()
