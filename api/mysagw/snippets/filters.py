from django_filters import BooleanFilter, FilterSet

from . import models


class SnippetFilterSet(FilterSet):
    archived = BooleanFilter()

    class Meta:
        model = models.Snippet
        fields = ["archived"]
