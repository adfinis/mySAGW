from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from ..identity.models import Identity
from . import models


class CaseAccessSerializer(serializers.ModelSerializer):
    included_serializers = {
        "identity": "mysagw.identity.serializers.IdentitySerializer",
    }

    class Meta:
        model = models.CaseAccess
        fields = (
            "case_id",
            "identity",
            "email",
        )
        extra_kwargs = {
            "identity": {"required": False, "read_only": True},
        }

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        try:
            validated_data["identity"] = Identity.objects.get(
                email__iexact=validated_data["email"]
            )
            validated_data.pop("email")
        except Identity.DoesNotExist:
            pass

        if models.CaseAccess.objects.filter(
            email__iexact=validated_data.get("email"),
            case_id=validated_data["case_id"],
            identity=validated_data.get("identity"),
        ).exists():
            raise ValidationError("Case already exists!")

        return validated_data
