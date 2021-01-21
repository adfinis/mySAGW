from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from . import models


class IdentityFactory(DjangoModelFactory):
    idp_id = Faker("uuid4")
    is_organisation = False

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


class MembershipRoleFactory(DjangoModelFactory):
    title = Faker("name")
    description = Faker("text")
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
