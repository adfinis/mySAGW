import operator
import shlex
from functools import reduce

from django.db.models import Max, OuterRef, Q, Subquery, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from django_filters import BooleanFilter, UUIDFilter
from django_filters.rest_framework import FilterSet
from rest_framework.compat import distinct
from rest_framework.filters import SearchFilter

from mysagw.filters import CharMultiValueFilter
from mysagw.identity import models


class IdentityFilterSet(FilterSet):
    idp_ids = CharMultiValueFilter(field_name="idp_id")
    has_idp_id = BooleanFilter(field_name="idp_id", lookup_expr="isnull", exclude=True)
    member_of_organisations = CharMultiValueFilter(
        field_name="memberships__organisation__organisation_name",
        distinct=True,
        method="member_of_organisations_filter",
    )

    @staticmethod
    def member_of_organisations_filter(queryset, name, value):
        membership_base_query = models.Membership.objects.filter(
            models.Q(organisation__organisation_name__in=value)
            & (
                (
                    models.Q(time_slot__isnull=True)
                    | models.Q(time_slot__contains=timezone.now())
                )
                & models.Q(inactive=False)
            ),
        )

        membership_base_subquery = membership_base_query.filter(
            identity_id=OuterRef("pk"),
        )
        return queryset.filter(
            memberships__id__in=Subquery(membership_base_subquery.values("id")),
        ).distinct()

    class Meta:
        model = models.Identity
        fields = [
            "email",
            "idp_id",
            "is_organisation",
            "member_of_organisations",
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


class OrganisationAdminMembersFilterSet(FilterSet):
    organisation = UUIDFilter(
        field_name="memberships__organisation_id",
        method="organisation_filter",
        required=True,
    )

    def organisation_filter(self, queryset, name, value):
        queryset = queryset.filter(**{name: value})
        queryset = queryset.annotate(
            highest_active_role=Coalesce(
                Max(
                    "memberships__role__sort",
                    filter=Q(**{name: value})
                    & Q(memberships__inactive=False)
                    & (
                        Q(memberships__time_slot__isnull=True)
                        | Q(memberships__time_slot__contains=timezone.now())
                    ),
                ),
                Value(0),
            ),
        )
        queryset = queryset.annotate(
            highest_inactive_role=Coalesce(
                Max(
                    "memberships__role__sort",
                    filter=Q(**{name: value})
                    & ~Q(
                        Q(memberships__inactive=False)
                        & (
                            Q(memberships__time_slot__isnull=True)
                            | Q(memberships__time_slot__contains=timezone.now())
                        ),
                    ),
                ),
                Value(0),
            ),
        )

        return queryset.order_by(
            "-highest_active_role",
            "-highest_inactive_role",
            "last_name",
            "first_name",
            "email",
        )

    class Meta:
        model = models.Identity
        fields = [
            "organisation",
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

    def filter_queryset(self, request, queryset, view):  # noqa: C901
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field)) for search_field in search_fields
        ]

        base = queryset
        # we're only interested in active memberships
        membership_base_query = models.Membership.objects.filter(
            (
                (
                    models.Q(time_slot__isnull=True)
                    | models.Q(time_slot__contains=timezone.now())
                )
                & models.Q(inactive=False)
            ),
        )

        membership_base_subquery = membership_base_query.filter(
            identity_id=OuterRef("pk"),
        )

        filters = []
        excludes = []

        for search_term in search_terms:
            exclude = False
            if search_term.startswith("-"):
                exclude = True
                search_term = search_term.lstrip("-")

            queries = []
            for orm_lookup in orm_lookups:
                lookup = models.Q(**{orm_lookup: search_term})

                if orm_lookup.startswith("memberships__"):
                    membership_orm_lookup = orm_lookup.replace("memberships__", "")
                    if not membership_base_query.filter(
                        **{membership_orm_lookup: search_term},
                    ).exists():
                        # short-circuiting in order to save ~75% of processing time
                        continue

                    membership_subquery = membership_base_subquery.filter(
                        **{membership_orm_lookup: search_term},
                    )
                    # first Q object short circuits again, for a performance gain
                    lookup = models.Q(**{orm_lookup: search_term}) & models.Q(
                        memberships__id__in=Subquery(membership_subquery.values("id")),
                    )

                queries.append(lookup)

            condition = reduce(operator.or_, queries)
            if exclude:
                excludes.append(condition)
            else:
                filters.append(condition)

        needed = [set(queryset.filter(f).values_list("pk", flat=True)) for f in filters]

        if needed == [set()]:
            # if no records match our filters, we don't care about excludes
            return models.Identity.objects.none()

        excluded = [
            pk
            for f in excludes
            for pk in queryset.filter(f).values_list("pk", flat=True)
        ]

        if not needed:
            # only excludes have been provided to the filter
            queryset = queryset.exclude(pk__in=excluded)
        else:
            needed_pks = reduce(lambda a, b: a.intersection(b), needed)
            queryset = queryset.filter(pk__in=needed_pks).exclude(pk__in=excluded)

        if self.must_call_distinct(queryset, search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            queryset = distinct(queryset, base)

        return queryset
