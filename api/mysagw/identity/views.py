from rest_framework_json_api import views

from . import models, serializers
from .permissions import IsAdmin, IsAuthenticated, IsStaff


class IdentityViewSet(views.ModelViewSet):
    serializer_class = serializers.IdentitySerializer
    queryset = models.Identity.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)
