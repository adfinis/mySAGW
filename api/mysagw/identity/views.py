from rest_framework_json_api import views

from . import models, serializers


class IdentityViewSet(views.ModelViewSet):
    serializer_class = serializers.IdentitySerializer
    queryset = models.Identity.objects
    lookup_field = "idp_id"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(pk=user.identity.pk)
