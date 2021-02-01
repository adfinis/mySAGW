from rest_framework_json_api import views

from ..identity.permissions import IsAdmin, IsAuthenticated, IsStaff
from . import models, serializers


class SnippetViewSet(views.ModelViewSet):
    serializer_class = serializers.SnippetSerializer
    queryset = models.Snippet.objects.all()
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)
