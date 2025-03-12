import pytest
from django.urls import reverse
from rest_framework import status
from watchman import settings as watchman_settings


@pytest.mark.parametrize(
    "client,expected_status",
    [
        ("user", status.HTTP_403_FORBIDDEN),
        ("staff", status.HTTP_200_OK),
        ("admin", status.HTTP_200_OK),
    ],
    indirect=["client"],
)
def test_healthz_permissions(db, snapshot, identity, client, expected_status):
    url = reverse("healthz")

    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    snapshot.assert_match(response.json())


@pytest.mark.usefixtures("_roll_back_migrations")
def test_db_migrations_not_applied(
    capsys,
    client,
    snapshot,
    identity,
):
    """
    Test /healthz/ endpoint response when migrations haven't been applied.

    Undo applied migrations for app 'contenttypes'.
    Affects database migrations health check, which should detect unapplied
    migrations and fail.
    """
    # get /healthz/ response and compare to previous snapshot
    response = client.get(reverse("healthz"))
    snapshot.assert_match(response.json())

    # assert database migrations check fails
    assert response.json()["database migrations"] == [{"default": {"ok": False}}]
    assert response.status_code == watchman_settings.WATCHMAN_ERROR_CODE
