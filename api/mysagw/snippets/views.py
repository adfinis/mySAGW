from rest_framework_json_api import views

from ..oidc_auth.permissions import IsAdmin, IsAuthenticated, IsStaff
from . import models, serializers
from .filters import SnippetFilterSet


class SnippetViewSet(views.ModelViewSet):
    serializer_class = serializers.SnippetSerializer
    queryset = models.Snippet.objects.all()
    filterset_class = SnippetFilterSet
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)
    search_fields = ("title", "body")
