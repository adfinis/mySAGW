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


class UniqueBooleanFieldSerializerMixin:
    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)
        if (
            self.instance
            and self.instance.default
            and not validated_data.get("default", True)
        ):
            raise ValidationError(
                'Can\'t unset "default". Set another default instead.'
            )
        return validated_data


class EmailSerializer(SetModifyingUserOnIdentityMixin, serializers.ModelSerializer):
    included_serializers = {
        "identity": "mysagw.identity.serializers.IdentitySerializer",
    }

    class Meta:
        model = models.Email
        resource_name = "additional-emails"
        fields = (
            "email",
            "identity",
            "description",
        )


class PhoneNumberSerializer(
    SetModifyingUserOnIdentityMixin,
    UniqueBooleanFieldSerializerMixin,
    serializers.ModelSerializer,
):
    included_serializers = {
        "identity": "mysagw.identity.serializers.IdentitySerializer",
    }

    class Meta:
        model = models.PhoneNumber
        fields = (
            "phone",
            "identity",
            "description",
            "default",
        )


class IdentitySerializer(TrackingSerializer):
    included_serializers = {
        "additional_emails": "mysagw.identity.serializers.EmailSerializer",
        "phone_numbers": "mysagw.identity.serializers.PhoneNumberSerializer",
    }

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        is_organisation = validated_data.get("is_organisation")
        organisation_name = validated_data.get("organisation_name")
        no_organisation_name_msg = (
            'Can\'t set "is_organisation" without an organisation_name.'
        )

        if not self.instance:
            if is_organisation and not organisation_name:
                raise ValidationError(no_organisation_name_msg)
            elif not is_organisation and organisation_name:
                validated_data["organisation_name"] = None
            return validated_data

        if self.instance.is_organisation and not is_organisation:
            if self.instance.members.exists():
                raise ValidationError(
                    'Can\'t unset "is_organisation", because there are members.'
                )
            validated_data["organisation_name"] = None

        if not self.instance.is_organisation and is_organisation:
            if self.instance.memberships.exists():
                raise ValidationError(
                    'Can\'t set "is_organisation", because there are memberships.'
                )
            elif not organisation_name:
                raise ValidationError(no_organisation_name_msg)

        return validated_data

    class Meta:
        model = models.Identity
        fields = TrackingSerializer.Meta.fields + (
            "idp_id",
            "first_name",
            "last_name",
            "interests",
            "email",
            "additional_emails",
            "phone_numbers",
            "is_organisation",
            "organisation_name",
        )
        extra_kwargs = {
            **TrackingSerializer.Meta.extra_kwargs,
            "interests": {"required": False},
            "idp_id": {"read_only": True},
            "additional_emails": {"required": False},
            "phone_numbers": {"required": False},
        }


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Identity
        fields = (
            "first_name",
            "last_name",
            "email",
        )
        extra_kwargs = {
            "email": {"read_only": True},
        }


class MyOrgsSerializer(serializers.ModelSerializer):
    is_authorized = serializers.SerializerMethodField()

    def get_is_authorized(self, obj):
        identity = self.context["request"].user.identity
        return obj.members.filter(identity=identity, authorized=True).exists()

    class Meta:
        model = models.Identity
        fields = (
            "first_name",
            "last_name",
            "organisation_name",
            "is_authorized",
            "email",
        )
        extra_kwargs = {
            "email": {"read_only": True},
        }


class InterestCategorySerializer(serializers.ModelSerializer):
    included_serializers = {
        "interests": "mysagw.identity.serializers.InterestSerializer",
    }

    class Meta:
        model = models.InterestCategory
        fields = ("title", "description", "archived", "interests")
        extra_kwargs = {
            "interests": {"required": False},
        }


class InterestSerializer(serializers.ModelSerializer):
    included_serializers = {
        "category": InterestCategorySerializer,
    }

    class Meta:
        model = models.Interest
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
    time_slot = DateRangeField(
        child_attrs={"allow_null": True}, required=False, allow_null=True
    )

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
