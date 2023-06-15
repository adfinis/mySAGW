from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from mysagw.filters import CharMultiValueFilter, UUIDMultiValueFilter

from . import models


class CaseAccessFilterSet(FilterSet):
    idp_id = CharFilter(field_name="identity__idp_id")
    case_ids = UUIDMultiValueFilter(field_name="case_id")
    idp_ids = CharMultiValueFilter(field_name="identity__idp_id")

    class Meta:
        model = models.CaseAccess
        fields = ["idp_id", "case_ids", "idp_ids"]
