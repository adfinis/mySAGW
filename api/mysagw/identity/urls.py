from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"emails", views.EmailViewSet)
r.register(r"identities", views.IdentityViewSet)
r.register(r"interest-categories", views.InterestCategoryViewSet)
r.register(r"interests", views.InterestViewSet)
r.register(r"membership-roles", views.MembershipRoleViewSet)
r.register(r"memberships", views.MembershipViewSet)
r.register(r"my-orgs", views.MyOrgsViewSet, basename="my-orgs")

urlpatterns = [
    url(
        r"^me/?$",
        views.MeViewSet.as_view({"get": "retrieve", "patch": "update"}),
        name="me",
    )
]

urlpatterns.extend(r.urls)
