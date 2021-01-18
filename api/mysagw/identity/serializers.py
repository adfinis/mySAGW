from rest_framework_json_api import serializers

from ..serializers import TrackingSerializer
from . import models


class IdentitySerializer(TrackingSerializer):
    class Meta:
        model = models.Identity
        fields = TrackingSerializer.Meta.fields + ("idp_id", "first_name", "last_name",)


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Identity
        fields = (
            "first_name",
            "last_name",
        )
