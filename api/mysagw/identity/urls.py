from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"identities", views.IdentityViewSet)

urlpatterns = [
    url(
        r"^me",
        views.MeViewSet.as_view({"get": "retrieve", "patch": "update"}),
        name="me",
    )
]

urlpatterns.extend(r.urls)
