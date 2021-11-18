from django_filters import UUIDFilter
from django_filters.rest_framework import FilterSet

from . import models


class CaseAccessFilterSet(FilterSet):
    idp_id = UUIDFilter(field_name="identity__idp_id")

    class Meta:
        model = models.CaseAccess
        fields = ["case_id", "identity", "idp_id"]
