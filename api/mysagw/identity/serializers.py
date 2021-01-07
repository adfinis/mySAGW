from rest_framework_json_api import serializers

from . import models


class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Identity
        fields = "__all__"
