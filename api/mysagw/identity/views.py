from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from . import models, serializers
from .permissions import IsAdmin, IsAuthenticated, IsStaff


class IdentityViewSet(views.ModelViewSet):
    serializer_class = serializers.IdentitySerializer
    queryset = models.Identity.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)


class MeViewSet(
    RetrieveModelMixin, UpdateModelMixin, GenericViewSet,
):
    serializer_class = serializers.MeSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user.identity

    def update(self, request, *args, **kwargs):
        self.kwargs["pk"] = self.request.user.identity.pk
        return super().update(request, *args, **kwargs)
