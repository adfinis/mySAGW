from rest_framework_json_api import serializers


class TrackingSerializer(serializers.ModelSerializer):
    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        user = self.context["request"].user
        if self.instance is None:
            validated_data["created_by_user"] = user.id
        validated_data["modified_by_user"] = user.id

        return validated_data

    class Meta:
        fields = (
            "created_at",
            "created_by_user",
            "modified_at",
            "modified_by_user",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
            "created_by_user": {"read_only": True},
            "modified_at": {"read_only": True},
            "modified_by_user": {"read_only": True},
        }
