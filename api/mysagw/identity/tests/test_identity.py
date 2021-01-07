from django.urls import reverse
from rest_framework import status


def test_identity_detail(db, admin_user, admin_client):
    url = reverse("identity-detail", args=[admin_user.username])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json["data"]["id"] == str(admin_user.identity.pk)
    assert "password" not in json["data"]["attributes"]
