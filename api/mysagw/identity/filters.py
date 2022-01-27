import operator
import shlex
from functools import reduce

from django.utils import timezone
from django_filters import BooleanFilter, CharFilter
from django_filters.rest_framework import FilterSet
from rest_framework.compat import distinct
from rest_framework.filters import SearchFilter

from mysagw.filters import CharMultiValueFilter
from mysagw.identity import models


class IdentityFilterSet(FilterSet):
    idp_ids = CharMultiValueFilter(field_name="idp_id")
    has_idp_id = BooleanFilter(field_name="idp_id", lookup_expr="isnull", exclude=True)
    memberships__organisation__organisation_name = CharFilter(distinct=True)

    class Meta:
        model = models.Identity
        fields = [
            "email",
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
            "organisation",
            "authorized",
        ]


class InterestFilterSet(FilterSet):
    public = BooleanFilter(field_name="category__public")

    class Meta:
        model = models.Interest
        fields = [
            "public",
        ]


class InterestCategoryFilterSet(FilterSet):
    class Meta:
        model = models.InterestCategory
        fields = [
            "public",
        ]


class SAGWSearchFilter(SearchFilter):
    @staticmethod
    def _split(value):
        lex = shlex.shlex(value, posix=True)
        lex.whitespace_split = True
        lex.commenters = ""
        lex.quotes = '"'
        return [i.strip() for i in lex if i.strip()]

    def get_search_terms(self, request):
        params = request.query_params.get(self.search_param, "")
        params = params.replace("\x00", "")  # strip null characters
        params = params.replace(",", " ")
        try:
            return self._split(params)
        except ValueError as e:
            if e.args[0] == "No closing quotation":
                return self._split(f'{params}"')

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field)) for search_field in search_fields
        ]

        base = queryset

        for search_term in search_terms:
            method = queryset.filter
            if search_term.startswith("-"):
                method = queryset.exclude
                search_term = search_term.lstrip("-")

            queries = []
            for orm_lookup in orm_lookups:
                lookup = models.Q(**{orm_lookup: search_term})
                if orm_lookup.startswith("memberships_"):
                    lookup = models.Q(**{orm_lookup: search_term}) & (
                        (
                            models.Q(memberships__time_slot__isnull=True)
                            | models.Q(memberships__time_slot__contains=timezone.now())
                        )
                        & models.Q(memberships__inactive=False)
                    )
                queries.append(lookup)

            condition = reduce(operator.or_, queries)
            queryset = method(condition)

        if self.must_call_distinct(queryset, search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            queryset = distinct(queryset, base)

        return queryset
