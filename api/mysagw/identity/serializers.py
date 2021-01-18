from rest_framework_json_api import serializers

from ..serializers import TrackingSerializer
from . import models


class IdentitySerializer(TrackingSerializer):
    class Meta:
        model = models.Identity
        fields = TrackingSerializer.Meta.fields + (
            "idp_id",
            "first_name",
            "last_name",
            "interests",
        )
        extra_kwargs = {
            **TrackingSerializer.Meta.extra_kwargs,
            "interests": {"required": False},
        }


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Identity
        fields = (
            "first_name",
            "last_name",
        )


class InterestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InterestCategory
        fields = (
            "title",
            "description",
            "archived",
        )


class InterestOptionSerializer(serializers.ModelSerializer):
    included_serializers = {
        "category": InterestCategorySerializer,
    }

    class Meta:
        model = models.InterestOption
        fields = (
            "title",
            "description",
            "category",
            "archived",
        )
