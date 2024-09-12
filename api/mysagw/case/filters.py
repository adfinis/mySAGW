from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from mysagw.filters import UUIDMultiValueFilter

from . import models


class CaseAccessFilterSet(FilterSet):
    idp_id = CharFilter(field_name="identity__idp_id")
    case_ids = UUIDMultiValueFilter(field_name="case_id")
    identity_ids = UUIDMultiValueFilter(field_name="identity_id")

    class Meta:
        model = models.CaseAccess
        fields = ["case_ids", "identity_ids"]
