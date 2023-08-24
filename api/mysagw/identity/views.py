import django_excel
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.utils import translation
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from ..dms_client import DMSClient, get_dms_error_response
from ..oidc_auth.permissions import IsAdmin, IsAuthenticated, IsStaff
from ..permissions import ReadOnly
from . import filters, models, serializers
from .export import IdentityExport, MembershipExport
from .permissions import IsAuthorized, IsOwn


class UniqueBooleanFieldViewSetMixin:
    def perform_destroy(self, instance):
        if (
            instance.default
            and instance.__class__.objects.filter(identity=instance.identity).count()
            > 1
        ):
            msg = "Can't delete the default entry. Set another entry as default first."
            raise ValidationError(
                msg,
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
            msg = "You can only create records for your own identity or identities you are authorized to manage."
            raise PermissionDenied(
                msg,
            )
        return super().perform_create(serializer)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_staff:
            return qs
        return qs.filter(
            Q(identity=self.request.user.identity)
            | Q(identity__in=self.request.user.identity.authorized_for),
        )


class EmailViewSet(IdentityAdditionsViewSetMixin, views.ModelViewSet):
    serializer_class = serializers.EmailSerializer
    queryset = models.Email.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | IsOwn | IsAuthorized),)
    filterset_class = filters.EmailFilterSet

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.id
        instance.identity.save()


class PhoneNumberViewSet(
    IdentityAdditionsViewSetMixin,
    UniqueBooleanFieldViewSetMixin,
    views.ModelViewSet,
):
    serializer_class = serializers.PhoneNumberSerializer
    queryset = models.PhoneNumber.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | IsOwn | IsAuthorized),)
    filterset_class = filters.PhoneNumberFilterSet

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.id
        instance.identity.save()


class AddressViewSet(IdentityAdditionsViewSetMixin, views.ModelViewSet):
    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | IsOwn | IsAuthorized),)
    filterset_class = filters.AddressFilterSet

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.id
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
        "additional_emails__email",
        "phone_numbers__phone",
        "memberships__role__title",
        "memberships__role__description",
        "memberships__organisation__organisation_name",
        "memberships__organisation__first_name",
        "memberships__organisation__last_name",
        "addresses__address_addition_1",
        "addresses__address_addition_2",
        "addresses__address_addition_3",
        "addresses__street_and_number",
        "addresses__postcode",
        "addresses__town",
    )

    @action(detail=False, methods=["post"])
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).prefetch_related(
            "phone_numbers",
            "additional_emails",
            "addresses",
        )

        ex = IdentityExport()
        records = ex.export(queryset)
        return django_excel.make_response_from_records(records, "xlsx")

    @action(detail=False, methods=["post"], url_path="export-memberships")
    def export_memberships(self, request, *args, **kwargs):
        identity_queryset = self.filter_queryset(self.get_queryset())

        queryset = (
            models.Membership.objects.filter(organisation__in=identity_queryset)
            .select_related("identity", "role")
            .prefetch_related("identity__additional_emails", "identity__addresses")
        )

        ex = MembershipExport()
        records = ex.export(queryset)
        return django_excel.make_response_from_records(records, "xlsx")

    @action(detail=False, methods=["post"], url_path="export-email")
    def export_email(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        records = queryset.values("email")
        return django_excel.make_response_from_records(records, "xlsx")

    @action(detail=False, methods=["post"], url_path="export-labels")
    def export_labels(self, request, *args, **kwargs):
        def group_records(records, group_size=2):
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
            if len(grouped_records[-1]) < group_size:
                # make sure the last row has also a length of `group_size`
                placeholders = [
                    {} for _ in range(group_size - len(grouped_records[-1]))
                ]
                grouped_records[-1] = [
                    *grouped_records[-1],
                    *placeholders,
                ]
            return grouped_records

        queryset = self.filter_queryset(self.get_queryset()).prefetch_related(
            "phone_numbers",
            "additional_emails",
            "addresses",
        )
        ex = IdentityExport()
        records = ex.export(
            queryset,
            include_fields=[
                "localized_title",
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

        dms_client = DMSClient()
        dms_response = dms_client.get_merged_document(
            {"identities": records},
            settings.DOCUMENT_MERGE_SERVICE_LABELS_TEMPLATE_SLUG,
        )

        if dms_response.status_code != status.HTTP_200_OK:
            return get_dms_error_response(dms_response)
        return HttpResponse(
            dms_response.content,
            status=status.HTTP_200_OK,
            content_type=dms_response.headers["Content-Type"],
        )


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


class PublicIdentitiesViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = serializers.PublicIdentitySerializer
    queryset = models.Identity.objects.all()
    filterset_class = filters.IdentityFilterSet
    search_fields = (
        "first_name",
        "last_name",
    )


class InterestCategoryViewSet(views.ModelViewSet):
    serializer_class = serializers.InterestCategorySerializer
    queryset = models.InterestCategory.objects.all()
    filterset_class = filters.InterestCategoryFilterSet
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | ReadOnly),)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_staff:
            return qs
        return qs.filter(public=True)


class InterestViewSet(views.ModelViewSet):
    serializer_class = serializers.InterestSerializer
    queryset = models.Interest.objects.all()
    filterset_class = filters.InterestFilterSet
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | ReadOnly),)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_staff:
            return qs
        return qs.filter(category__public=True)


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
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)
    filterset_class = filters.MembershipFilterSet

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.id
        instance.identity.save()


class MyMembershipViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.MyMembershipsSerializer
    permission_classes = (IsAuthenticated & (IsOwn & ReadOnly),)

    def get_queryset(self):
        return self.request.user.identity.memberships.all()


class OrganisationAdminMembersViewSet(
    ListModelMixin,
    GenericViewSet,
):
    queryset = models.Identity.objects.all()
    serializer_class = serializers.OrganisationAdminMembersSerializer
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)
    filterset_class = filters.OrganisationAdminMembersFilterSet
