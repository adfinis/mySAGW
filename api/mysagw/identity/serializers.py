from ..serializers import TrackingSerializer
from . import models


class IdentitySerializer(TrackingSerializer):
    class Meta:
        model = models.Identity
        fields = TrackingSerializer.Meta.fields + ("idp_id", "first_name", "last_name",)
