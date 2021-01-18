from factory import Faker
from factory.django import DjangoModelFactory

from . import models


class IdentityFactory(DjangoModelFactory):
    idp_id = Faker("uuid4")

    class Meta:
        model = models.Identity
