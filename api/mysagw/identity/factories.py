from factory import Faker, Maybe, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from . import models


class IdentityFactory(DjangoModelFactory):
    idp_id = Faker("uuid4")
    email = Faker("email")
    is_organisation = False
    organisation_name = Maybe("is_organisation", Faker("company"), None)
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    class Meta:
        model = models.Identity


class EmailFactory(DjangoModelFactory):
    identity = SubFactory(IdentityFactory)
    email = Faker("email")
    description = fuzzy.FuzzyChoice(["work", "private", "assistant"])

    class Meta:
        model = models.Email


class PhoneNumberFactory(DjangoModelFactory):
    identity = SubFactory(IdentityFactory)
    phone = Faker("phone_number")
    description = fuzzy.FuzzyChoice(["work", "private", "home", "office", "mobile"])
    default = True

    class Meta:
        model = models.PhoneNumber


class AddressFactory(DjangoModelFactory):
    identity = SubFactory(IdentityFactory)
    street_and_number = Faker("street_address")
    postcode = Faker("postcode")
    town = Faker("city")
    country = Faker("country_code")
    description = fuzzy.FuzzyChoice(["work", "private", "home", "office"])
    default = True

    class Meta:
        model = models.Address


class InterestCategoryFactory(DjangoModelFactory):
    title = Faker("word")
    description = Faker("sentence")
    archived = False

    class Meta:
        model = models.InterestCategory


class InterestFactory(DjangoModelFactory):
    title = Faker("job")
    description = Faker("sentence")
    archived = False
    category = SubFactory(InterestCategoryFactory)

    class Meta:
        model = models.Interest


class MembershipRoleFactory(DjangoModelFactory):
    title = Faker("multilang", faker_provider="job")
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
