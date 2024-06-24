from django_filters.rest_framework import FilterSet

from mysagw.filters import UUIDMultiValueFilter

from . import models


class CaseAccessFilterSet(FilterSet):
    case_ids = UUIDMultiValueFilter(field_name="case_id")
    identity_ids = UUIDMultiValueFilter(field_name="identity_id")

    class Meta:
        model = models.CaseAccess
        fields = ["case_ids", "identity_ids"]
