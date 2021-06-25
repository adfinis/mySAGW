from django_filters.rest_framework import FilterSet

from mysagw.identity import models


class IdentityFilterSet(FilterSet):
    class Meta:
        model = models.Identity
        fields = [
            "idp_id",
            "is_organisation",
            "memberships__organisation__organisation_name",
        ]


class EmailFilterSet(FilterSet):
    class Meta:
        model = models.Email
        fields = [
            "identity",
        ]


class PhoneNumberFilterSet(FilterSet):
    class Meta:
        model = models.PhoneNumber
        fields = [
            "identity",
        ]


class AddressFilterSet(FilterSet):
    class Meta:
        model = models.Address
        fields = [
            "identity",
        ]


class MembershipFilterSet(FilterSet):
    class Meta:
        model = models.Membership
        fields = [
            "identity",
            "authorized",
        ]
