from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import DateRangeField
from rest_framework.exceptions import ValidationError
from rest_framework.relations import MANY_RELATION_KWARGS
from rest_framework_json_api import serializers

from ..serializers import TrackingSerializer
from . import models


class SetModifyingUserOnIdentityMixin:
    def set_modifying_user_on_identity(self, instance):
        instance.identity.modified_by_user = self.context["request"].user.id
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
            msg = 'Can\'t unset "default". Set another default instead.'
            raise ValidationError(
                msg,
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
    phone_pretty = serializers.SerializerMethodField()

    included_serializers = {
        "identity": "mysagw.identity.serializers.IdentitySerializer",
    }

    def get_phone_pretty(self, obj):
        return obj.phone.as_international

    class Meta:
        model = models.PhoneNumber
        fields = (
            "phone",
            "phone_pretty",
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
            "is_organisation",
            getattr(self.instance, "is_organisation", None),
        ):
            any_needed.append("organisation_name")

        values = [
            validated_data.get(attr, getattr(self.instance, attr, None))
            for attr in any_needed
        ]

        if not any(values):
            msg = "Identities need at least an email, first_name, last_name or organisation_name."
            raise ValidationError(
                msg,
            )

    def _handle_organisation_validations(self, validated_data):
        is_organisation = validated_data.get("is_organisation")
        organisation_name = validated_data.get("organisation_name")
        no_organisation_name_msg = (
            'Can\'t set "is_organisation" without an organisation_name.'
        )

        if not self.instance:
            if is_organisation and not organisation_name:
                raise ValidationError(no_organisation_name_msg)
            if not is_organisation and organisation_name:
                validated_data["organisation_name"] = None
            return validated_data

        if self.instance.is_organisation and not is_organisation:
            if self.instance.members.exists():
                msg = 'Can\'t unset "is_organisation", because there are members.'
                raise ValidationError(
                    msg,
                )
            validated_data["organisation_name"] = None

        if not self.instance.is_organisation and is_organisation:
            if self.instance.memberships.exists():
                msg = 'Can\'t set "is_organisation", because there are memberships.'
                raise ValidationError(
                    msg,
                )
            if not organisation_name:
                raise ValidationError(no_organisation_name_msg)

        if not self.instance.is_organisation and (
            validated_data.get("is_expert_association")
            or validated_data.get("is_advisory_board")
        ):
            msg = 'Can\'t set "is_expert_association" or "is_advisory_board", because it isn\'t a organisation.'
            raise ValidationError(msg)

        return validated_data

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        self._ensure_no_empty_identity(validated_data)

        # if email was removed, we unset the email in order to satisfy the unique
        # constraint
        if validated_data.get("email") == "":
            validated_data["email"] = None

        if (
            validated_data.get("email")
            and self.context["request"].method == "POST"
            and models.Identity.objects.filter(
                email__iexact=validated_data["email"],
            ).exists()
        ):
            msg = _("%(model_name)s with this %(field_label)s already exists.") % {
                "model_name": "identity",
                "field_label": "email",
            }
            raise ValidationError(code="unique", detail={"email": msg})

        return self._handle_organisation_validations(validated_data)

    class Meta:
        model = models.Identity
        fields = (
            *TrackingSerializer.Meta.fields,
            "idp_id",
            "first_name",
            "last_name",
            "salutation",
            "title",
            "language",
            "interests",
            "email",
            "additional_emails",
            "phone_numbers",
            "addresses",
            "is_organisation",
            "organisation_name",
            "is_expert_association",
            "is_advisory_board",
            "comment",
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


class InterestsManyRelatedField(serializers.ManyRelatedField):
    # overridden for usage in `me` and `my-orgs` views. Non-admin users only have access
    # to public interests
    def get_attribute(self, instance):
        queryset = super().get_attribute(instance)
        return queryset.filter(category__public=True)


class InterestsResourceRelatedField(serializers.ResourceRelatedField):
    # overridden for using a custom `ManyRelatedField`
    @classmethod
    def many_init(cls, *args, **kwargs):
        list_kwargs = {
            key: item for key, item in kwargs.items() if key in MANY_RELATION_KWARGS
        }
        list_kwargs["child_relation"] = cls(*args, **kwargs)
        return InterestsManyRelatedField(**list_kwargs)


class MeSerializer(serializers.ModelSerializer):
    interests = InterestsResourceRelatedField(
        many=True,
        queryset=models.Interest.objects.filter(category__public=True),
        required=False,
    )

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)
        if "interests" not in validated_data:
            return validated_data

        # normal users have no access to their non-public interests. Here we make sure
        # they are not lost on update
        validated_data["interests"] += [
            interest
            for interest in self.instance.interests.iterator()
            if interest.category.public is False
        ]

        return validated_data

    class Meta:
        model = models.Identity
        fields = (
            "idp_id",
            "first_name",
            "last_name",
            "salutation",
            "language",
            "email",
            "interests",
        )
        extra_kwargs = {
            "idp_id": {"read_only": True},
            "email": {"read_only": True},
        }


class MyOrgsSerializer(MeSerializer):
    is_authorized = serializers.SerializerMethodField()

    def get_is_authorized(self, obj):
        identity = self.context["request"].user.identity
        return obj in identity.authorized_for

    class Meta:
        model = models.Identity
        fields = (
            "idp_id",
            "first_name",
            "last_name",
            "salutation",
            "title",
            "language",
            "is_organisation",
            "organisation_name",
            "is_expert_association",
            "is_advisory_board",
            "is_authorized",
            "email",
            "interests",
        )
        extra_kwargs = {
            "idp_id": {"read_only": True},
            "email": {"read_only": True},
            "organisation_name": {"read_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "salutation": {"read_only": True},
            "title": {"read_only": True},
            "language": {"read_only": True},
            "is_organisation": {"read_only": True},
            "is_expert_association": {"read_only": True},
            "is_advisory_board": {"read_only": True},
        }


class PublicIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Identity
        fields = (
            "idp_id",
            "email",
            "organisation_name",
            "first_name",
            "last_name",
            "salutation",
            "language",
            "is_organisation",
        )
        extra_kwargs = {
            "idp_id": {"read_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "email": {"read_only": True},
        }


class InterestCategorySerializer(serializers.ModelSerializer):
    included_serializers = {
        "interests": "mysagw.identity.serializers.InterestSerializer",
    }

    class Meta:
        model = models.InterestCategory
        fields = ("title", "description", "archived", "interests", "public")
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
            "sort",
        )

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)
        if not validated_data.get("title", {}).get(settings.LANGUAGE_CODE):
            msg = f'Title must be set for language: "{settings.LANGUAGE_CODE}"'
            raise ValidationError(
                msg,
            )
        return validated_data


class MembershipSerializer(
    SetModifyingUserOnIdentityMixin,
    serializers.ModelSerializer,
):
    identity = serializers.ResourceRelatedField(
        queryset=models.Identity.objects.filter(is_organisation=False),
    )
    organisation = serializers.ResourceRelatedField(
        queryset=models.Identity.objects.filter(is_organisation=True),
    )
    time_slot = DateRangeField(
        child_attrs={"allow_null": True},
        required=False,
        allow_null=True,
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
                self.instance,
                field,
            ):
                msg = f'Field "{field}" can\'t be modified.'
                raise ValidationError(msg)
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


class MyMembershipsSerializer(MembershipSerializer):
    included_serializers = {
        "role": MembershipRoleSerializer,
        "organisation": MyOrgsSerializer,
    }


class OrganisationAdminMembersSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        memberships = obj.memberships.filter(
            organisation_id=self.context["request"].GET["filter[organisation]"],
        )
        active_memberships = memberships.filter(
            Q(inactive=False),
            Q(time_slot__isnull=True) | Q(time_slot__contains=timezone.now()),
        )
        inactive_memberships = memberships.exclude(
            pk__in=active_memberships.values_list("pk", flat=True),
        )

        result_memberships = []
        date_range_field = DateRangeField(
            child_attrs={"allow_null": True},
            required=False,
            allow_null=True,
        )
        for membership_qs in [active_memberships, inactive_memberships]:
            for m in membership_qs.order_by("-role__sort"):
                time_slot = None
                if m.time_slot:
                    time_slot = date_range_field.to_representation(m.time_slot)
                result_memberships.append(
                    {
                        "role": m.role.title if m.role else None,
                        "inactive": m.inactive,
                        "authorized": m.authorized,
                        "time_slot": time_slot,
                    },
                )

        return result_memberships

    class Meta:
        model = models.Identity
        # TODO: implement new resource type in frontend
        # resource_name = "OrganisationAdminMembersIdentity"
        fields = (
            "first_name",
            "last_name",
            "email",
            "roles",
        )
