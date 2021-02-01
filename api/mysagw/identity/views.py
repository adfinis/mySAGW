from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from . import models, serializers
from .permissions import IsAdmin, IsAuthenticated, IsOrgAdmin, IsStaff


class EmailViewSet(views.ModelViewSet):
    serializer_class = serializers.EmailSerializer
    queryset = models.Email.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.username
        instance.identity.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.default is True:
            raise ValidationError("Cannot delete default Email.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IdentityViewSet(views.ModelViewSet):
    serializer_class = serializers.IdentitySerializer
    queryset = models.Identity.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)


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


class InterestOptionViewSet(views.ModelViewSet):
    serializer_class = serializers.InterestOptionSerializer
    queryset = models.InterestOption.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)


class MembershipRoleViewSet(views.ModelViewSet):
    serializer_class = serializers.MembershipRoleSerializer
    queryset = models.MembershipRole.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)


class MembershipViewSet(views.ModelViewSet):
    serializer_class = serializers.MembershipSerializer
    queryset = models.Membership.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.identity.modified_by_user = self.request.user.username
        instance.identity.save()
