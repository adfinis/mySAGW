from drf_extra_fields.fields import DateRangeField
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from ..serializers import TrackingSerializer
from . import models


class SetModifyingUserOnIdentityMixin:
    def set_modifying_user_on_identity(self, instance):
        instance.identity.modified_by_user = self.context["request"].user.username
        instance.identity.save()

    def create(self, validated_data):
        instance = super().create(validated_data)
        self.set_modifying_user_on_identity(instance)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self.set_modifying_user_on_identity(instance)
        return instance


class EmailSerializer(SetModifyingUserOnIdentityMixin, serializers.ModelSerializer):
    included_serializers = {
        "identity": "mysagw.identity.serializers.IdentitySerializer",
    }

    class Meta:
        model = models.Email
        fields = (
            "email",
            "identity",
            "description",
            "default",
        )


class IdentitySerializer(TrackingSerializer):
    included_serializers = {
        "emails": "mysagw.identity.serializers.EmailSerializer",
    }

    class Meta:
        model = models.Identity
        fields = TrackingSerializer.Meta.fields + (
            "idp_id",
            "first_name",
            "last_name",
            "interests",
            "emails",
        )
        extra_kwargs = {
            **TrackingSerializer.Meta.extra_kwargs,
            "interests": {"required": False},
            "emails": {"required": False},
        }


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Identity
        fields = (
            "first_name",
            "last_name",
        )


class MyOrgsSerializer(serializers.ModelSerializer):
    is_authorized = serializers.SerializerMethodField()

    def get_is_authorized(self, obj):
        identity = self.context["request"].user.identity
        return obj.memberships.filter(identity=identity, authorized=True).exists()

    class Meta:
        model = models.Identity
        fields = (
            "first_name",
            "last_name",
            "organisation_name",
            "is_authorized",
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


class MembershipRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MembershipRole
        fields = (
            "title",
            "description",
            "archived",
        )


class MembershipSerializer(
    SetModifyingUserOnIdentityMixin, serializers.ModelSerializer
):
    identity = serializers.ResourceRelatedField(
        queryset=models.Identity.objects.filter(is_organisation=False)
    )
    organisation = serializers.ResourceRelatedField(
        queryset=models.Identity.objects.filter(is_organisation=True)
    )
    time_slot = DateRangeField()

    included_serializers = {
        "role": MembershipRoleSerializer,
    }

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)
        if not self.instance:
            return validated_data
        for field in ["identity", "organisation"]:
            if validated_data.get(field) and validated_data[field] != getattr(
                self.instance, field
            ):
                raise ValidationError(f'Field "{field}" can\'t be modified.')
        return validated_data

    class Meta:
        model = models.Membership
        fields = (
            "identity",
            "organisation",
            "role",
            "authorized",
            "time_slot",
            "next_election",
            "comment",
            "inactive",
        )
