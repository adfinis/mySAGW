from factory import Faker
from factory.django import DjangoModelFactory

from . import models


class IdentityFactory(DjangoModelFactory):
    idp_id = Faker("uuid")

    class Meta:
        model = models.Identity
