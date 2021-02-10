from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from . import models


class IdentityFactory(DjangoModelFactory):
    idp_id = Faker("uuid4")
    email = Faker("email")
    is_organisation = False

    class Meta:
        model = models.Identity


class EmailFactory(DjangoModelFactory):
    identity = SubFactory(IdentityFactory)
    email = Faker("email")
    description = Faker("text")

    class Meta:
        model = models.Email


class PhoneNumberFactory(DjangoModelFactory):
    identity = SubFactory(IdentityFactory)
    phone = Faker("phone_number")
    description = Faker("text")
    default = True

    class Meta:
        model = models.PhoneNumber


class InterestCategoryFactory(DjangoModelFactory):
    title = Faker("multilang", faker_provider="name")
    description = Faker("multilang", faker_provider="text")
    archived = False

    class Meta:
        model = models.InterestCategory


class InterestFactory(DjangoModelFactory):
    title = Faker("multilang", faker_provider="name")
    description = Faker("multilang", faker_provider="text")
    archived = False
    category = SubFactory(InterestCategoryFactory)

    class Meta:
        model = models.Interest


class MembershipRoleFactory(DjangoModelFactory):
    title = Faker("multilang", faker_provider="name")
    description = Faker("multilang", faker_provider="text")
    archived = False

    class Meta:
        model = models.MembershipRole


class MembershipFactory(DjangoModelFactory):
    identity = SubFactory(IdentityFactory)
    organisation = SubFactory(IdentityFactory, is_organisation=True)
    role = SubFactory(MembershipRoleFactory)
    authorized = False
    inactive = False

    class Meta:
        model = models.Membership
