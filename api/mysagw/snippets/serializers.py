from rest_framework_json_api import serializers

from . import models


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Snippet
        fields = ("title", "body", "archived")
