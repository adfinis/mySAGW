from factory import Faker
from factory.django import DjangoModelFactory

from . import models


class CaseAccessFactory(DjangoModelFactory):
    case_id = Faker("uuid4")
    identity = None
    email = Faker("email")

    class Meta:
        model = models.CaseAccess
