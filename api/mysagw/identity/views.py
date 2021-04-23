import django_excel
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from . import filters, models, serializers
from .export import IdentityExport
from .permissions import (
    IsAdmin,
    IsAuthenticated,
    IsOrgAdmin,
    IsOwnOrAuthorized,
    IsStaff,
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
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | IsOwnOrAuthorized),)
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
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | IsOwnOrAuthorized),)
    filterset_class = filters.PhoneNumberFilterSet

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.username
        instance.identity.save()


class AddressViewSet(IdentityAdditionsViewSetMixin, views.ModelViewSet):
    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | IsOwnOrAuthorized),)
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
    permission_classes = (IsAuthenticated & IsOrgAdmin,)

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
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)


class MembershipViewSet(views.ModelViewSet):
    serializer_class = serializers.MembershipSerializer
    queryset = models.Membership.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)
    filterset_class = filters.MembershipFilterSet

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.username
        instance.identity.save()
