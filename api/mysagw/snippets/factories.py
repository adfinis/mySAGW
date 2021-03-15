from factory import Faker
from factory.django import DjangoModelFactory

from . import models


class SnippetFactory(DjangoModelFactory):
    title = Faker("word")
    body = Faker("multilang", faker_provider="text")
    archived = False

    class Meta:
        model = models.Snippet
