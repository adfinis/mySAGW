import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "search,expected",
    [
        ("0", [0]),
        ("1", [1]),
        ("schnip", [0, 1, 2, 3, 4]),
        ("inhalt", [0, 1, 2, 3, 4]),
        ("snip", [0, 1, 2, 3, 4]),
        ("bod", [0, 1, 2, 3, 4]),
        ("foobar", []),
    ],
)
def test_snippet_search(db, client, snippet_factory, search, expected):
    """
    Test snippet search filter.

    This test makes sure that search lookups are NOT restricted to the current language.
    For this to work, `settings.LOCALIZED_FIELDS_EXPERIMENTAL` is set to `False`.
    """
    snippets = [
        snippet_factory(
            title={"de": f"schnippsel{i}", "en": f"snippet{i}"},
            body={"de": f"inhalt{i}", "en": f"body{i}"},
        )
        for i in range(5)
    ]

    url = reverse("snippet-list")

    response = client.get(url, {"filter[search]": search})

    assert response.status_code == status.HTTP_200_OK

    expected_ids = sorted([str(snippets[ex].pk) for ex in expected])

    json = response.json()

    received_ids = []
    for snippet in json["data"]:
        received_ids.append(snippet["id"])
    received_ids = sorted(received_ids)

    assert expected_ids == received_ids


def test_snippet_archived_filter(db, client, snippet_factory):
    snippet_factory.create_batch(3, archived=True)
    expected_snippets = snippet_factory.create_batch(3, archived=False)

    expected_ids = sorted([str(snippet.pk) for snippet in expected_snippets])

    url = reverse("snippet-list")

    response = client.get(url, {"filter[archived]": False})

    assert response.status_code == status.HTTP_200_OK

    json = response.json()

    received_ids = []
    for snippet in json["data"]:
        received_ids.append(snippet["id"])
    received_ids = sorted(received_ids)

    assert expected_ids == received_ids
