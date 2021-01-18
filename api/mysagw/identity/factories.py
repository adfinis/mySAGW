from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from . import models


class IdentityFactory(DjangoModelFactory):
    idp_id = Faker("uuid4")

    class Meta:
        model = models.Identity


class InterestCategoryFactory(DjangoModelFactory):
    title = Faker("name")
    description = Faker("text")
    archived = False

    class Meta:
        model = models.InterestCategory


class InterestOptionFactory(DjangoModelFactory):
    title = Faker("name")
    description = Faker("text")
    archived = False
    category = SubFactory(InterestCategoryFactory)

    class Meta:
        model = models.InterestOption
