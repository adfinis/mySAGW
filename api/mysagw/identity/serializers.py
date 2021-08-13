from django.conf import settings
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


class AddressSerializer(SetModifyingUserOnIdentityMixin, serializers.ModelSerializer):
    included_serializers = {
        "identity": "mysagw.identity.serializers.IdentitySerializer",
    }

    class Meta:
        model = models.Address
        fields = (
            "identity",
            "address_addition_1",
            "address_addition_2",
            "address_addition_3",
            "street_and_number",
            "po_box",
            "postcode",
            "town",
            "country",
            "description",
            "default",
        )


class IdentitySerializer(TrackingSerializer):
    has_memberships = serializers.SerializerMethodField()
    has_members = serializers.SerializerMethodField()

    included_serializers = {
        "additional_emails": "mysagw.identity.serializers.EmailSerializer",
        "phone_numbers": "mysagw.identity.serializers.PhoneNumberSerializer",
        "addresses": "mysagw.identity.serializers.AddressSerializer",
    }

    def get_has_memberships(self, obj):
        return obj.memberships.exists()

    def get_has_members(self, obj):
        return obj.members.exists()

    def _ensure_no_empty_identity(self, validated_data):
        any_needed = ["email", "first_name", "last_name"]
        if validated_data.get(
            "is_organisation", getattr(self.instance, "is_organisation", None)
        ):
            any_needed.append("organisation_name")

        values = [
            validated_data.get(attr, getattr(self.instance, attr, None))
            for attr in any_needed
        ]

        if not any(values):
            raise ValidationError(
                "Identities need at least an email, first_name, last_name or "
                "organisation_name."
            )

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        is_organisation = validated_data.get("is_organisation")
        organisation_name = validated_data.get("organisation_name")
        no_organisation_name_msg = (
            'Can\'t set "is_organisation" without an organisation_name.'
        )

        self._ensure_no_empty_identity(validated_data)

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
            "salutation",
            "language",
            "interests",
            "email",
            "additional_emails",
            "phone_numbers",
            "addresses",
            "is_organisation",
            "organisation_name",
            "has_memberships",
            "has_members",
        )
        extra_kwargs = {
            **TrackingSerializer.Meta.extra_kwargs,
            "interests": {"required": False},
            "idp_id": {"read_only": True},
            "additional_emails": {"required": False},
            "phone_numbers": {"required": False},
            "addresses": {"required": False},
        }


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Identity
        fields = (
            "idp_id",
            "first_name",
            "last_name",
            "salutation",
            "language",
            "email",
        )
        extra_kwargs = {
            "idp_id": {"read_only": True},
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
            "idp_id",
            "first_name",
            "last_name",
            "salutation",
            "language",
            "is_organisation",
            "organisation_name",
            "is_authorized",
            "email",
        )
        extra_kwargs = {
            "idp_id": {"read_only": True},
            "is_organisation": {"read_only": True},
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

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)
        if not validated_data.get("title", {}).get(settings.LANGUAGE_CODE):
            raise ValidationError(
                f'Title must be set for language: "{settings.LANGUAGE_CODE}"'
            )
        return validated_data


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
        "organisation": IdentitySerializer,
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
