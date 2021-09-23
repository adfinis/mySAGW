from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from mysagw.case import filters, models, serializers
from mysagw.case.permissions import HasCaseAccess
from mysagw.oidc_auth.permissions import IsAdmin, IsAuthenticated


class CaseAccessViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.CaseAccessSerializer
    queryset = models.CaseAccess.objects.all()
    filterset_class = filters.CaseAccessFilterSet
    permission_classes = (IsAuthenticated & (IsAdmin | HasCaseAccess),)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_admin:
            return qs
        return qs.filter(
            case_id__in=qs.filter(identity=self.request.user.identity).values("case_id")
        )
