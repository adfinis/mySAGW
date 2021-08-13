import json

import django_excel
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.utils import translation
from requests import HTTPError
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from . import filters, models, serializers
from .dms_client import DMSClient
from .export import IdentityExport
from .permissions import (
    IsAdmin,
    IsAuthenticated,
    IsAuthorized,
    IsOwn,
    IsStaff,
    ReadOnly,
)


class UniqueBooleanFieldViewSetMixin:
    def perform_destroy(self, instance):
        if (
            instance.default
            and instance.__class__.objects.filter(identity=instance.identity).count()
            > 1
        ):
            raise ValidationError(
                "Can't delete the default entry. Set another entry as default first."
            )
        super().perform_destroy(instance)


class IdentityAdditionsViewSetMixin:
    """Only allow to see/create objects for own identities."""

    def perform_create(self, serializer):
        identity = serializer.validated_data["identity"]
        if (
            identity != self.request.user.identity
            and identity not in self.request.user.identity.authorized_for
            and not self.request.user.is_staff
        ):
            raise PermissionDenied(
                "You can only create records for your own identity or identities you "
                "are authorized to manage."
            )
        return super().perform_create(serializer)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_staff:
            return qs
        qs = qs.filter(
            Q(identity=self.request.user.identity)
            | Q(identity__in=self.request.user.identity.authorized_for)
        )
        return qs


class EmailViewSet(IdentityAdditionsViewSetMixin, views.ModelViewSet):
    serializer_class = serializers.EmailSerializer
    queryset = models.Email.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | IsOwn | IsAuthorized),)
    filterset_class = filters.EmailFilterSet

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.username
        instance.identity.save()


class PhoneNumberViewSet(
    IdentityAdditionsViewSetMixin, UniqueBooleanFieldViewSetMixin, views.ModelViewSet
):
    serializer_class = serializers.PhoneNumberSerializer
    queryset = models.PhoneNumber.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | IsOwn | IsAuthorized),)
    filterset_class = filters.PhoneNumberFilterSet

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.username
        instance.identity.save()


class AddressViewSet(IdentityAdditionsViewSetMixin, views.ModelViewSet):
    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | IsOwn | IsAuthorized),)
    filterset_class = filters.AddressFilterSet

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.username
        instance.identity.save()


class IdentityViewSet(views.ModelViewSet):
    serializer_class = serializers.IdentitySerializer
    queryset = models.Identity.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)
    filterset_class = filters.IdentityFilterSet
    search_fields = (
        "organisation_name",
        "first_name",
        "last_name",
        "email",
        "interests__title",
        "interests__description",
        "additional_emails__email",
        "phone_numbers__phone",
        "memberships__role__title",
        "memberships__role__description",
        "memberships__organisation__organisation_name",
        "memberships__organisation__first_name",
        "memberships__organisation__last_name",
    )

    @action(detail=False, methods=["post"])
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).prefetch_related(
            "phone_numbers", "additional_emails", "addresses"
        )

        ex = IdentityExport()
        records = ex.export(queryset)
        response = django_excel.make_response_from_records(records, "xlsx")
        return response

    @action(detail=False, methods=["post"], url_path="export-email")
    def export_email(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        records = queryset.values("email")
        response = django_excel.make_response_from_records(records, "xlsx")
        return response

    def _get_dms_error_content(self, response):
        if response.headers["Content-Type"].startswith("application/json"):
            content = response.json()
            content["source"] = "DMS"
            return json.dumps({"errors": content})
        elif response.headers["Content-Type"].startswith("text/plain"):
            return f"[DMS] {response.content.decode()}".encode("utf-8")
        return response.content

    def _merge(self, records):
        client = DMSClient()
        try:
            resp = client.merge(
                settings.DOCUMENT_MERGE_SERVICE_LABELS_TEMPLATE_SLUG,
                {"identities": records},
                None,
            )
            return resp.status_code, resp.headers["Content-Type"], resp.content
        except HTTPError as e:
            content = self._get_dms_error_content(e.response)
            return e.response.status_code, e.response.headers["Content-Type"], content

    @action(detail=False, methods=["post"], url_path="export-labels")
    def export_labels(self, request, *args, **kwargs):
        def group_records(records, group_size=3):
            grouped_records = []
            addrs = []
            ct = None
            for ct, identitiy in enumerate(records):
                addrs.append(identitiy)
                if (ct + 1) % group_size == 0:
                    grouped_records.append(list(addrs))
                    addrs = []
            if ct is not None and (ct + 1) % group_size > 0:
                grouped_records.append(list(addrs))
            return grouped_records

        queryset = self.filter_queryset(self.get_queryset()).prefetch_related(
            "phone_numbers", "additional_emails", "addresses"
        )
        ex = IdentityExport()
        records = ex.export(
            queryset,
            include_fields=[
                "first_name",
                "last_name",
                "organisation_name",
                "address_addition_1",
                "address_addition_2",
                "address_addition_3",
                "street_and_number",
                "po_box",
                "postcode",
                "town",
                "country",
            ],
            ignore_empty=True,
        )

        records = group_records(records)

        status_code, mime_type, resp_content = self._merge(records)
        return HttpResponse(resp_content, status=status_code, content_type=mime_type)


class MeViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.MeSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user.identity

    def update(self, request, *args, **kwargs):
        self.kwargs["pk"] = self.request.user.identity.pk
        return super().update(request, *args, **kwargs)


class MyOrgsViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.MyOrgsSerializer
    permission_classes = (IsAuthenticated & IsAuthorized,)

    def get_queryset(self):
        return self.request.user.identity.member_of


class InterestCategoryViewSet(views.ModelViewSet):
    serializer_class = serializers.InterestCategorySerializer
    queryset = models.InterestCategory.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)


class InterestViewSet(views.ModelViewSet):
    serializer_class = serializers.InterestSerializer
    queryset = models.Interest.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)


class MembershipRoleViewSet(views.ModelViewSet):
    serializer_class = serializers.MembershipRoleSerializer
    queryset = models.MembershipRole.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | ReadOnly),)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        lang = translation.get_language()
        return qs.order_by(f"title__{lang}")


class MembershipViewSet(views.ModelViewSet):
    serializer_class = serializers.MembershipSerializer
    queryset = models.Membership.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | (IsOwn & ReadOnly)),)
    filterset_class = filters.MembershipFilterSet

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_staff:
            return qs
        qs = qs.filter(identity=self.request.user.identity)
        return qs

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.username
        instance.identity.save()
