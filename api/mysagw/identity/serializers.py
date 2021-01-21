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
    included_serializers = {
        "options": "mysagw.identity.serializers.InterestOptionSerializer",
    }

    class Meta:
        model = models.InterestCategory
        fields = ("title", "description", "archived", "options")
        extra_kwargs = {
            "options": {"required": False},
        }


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
