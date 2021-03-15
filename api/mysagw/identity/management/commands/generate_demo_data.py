import random

from django.core.management.base import BaseCommand

from mysagw import conftest  # noqa
from mysagw.identity import models
from mysagw.identity.factories import (
    EmailFactory,
    InterestCategoryFactory,
    InterestFactory,
    MembershipFactory,
    MembershipRoleFactory,
    PhoneNumberFactory,
)


class Command(BaseCommand):
    help = "Load demo data."

    def add_arguments(self, parser):
        parser.add_argument("--cleanup", default=False, action="store_true")
        parser.add_argument("--rounds", default=1, type=int)

    def cleanup(self):
        models.Email.objects.all().delete()
        models.PhoneNumber.objects.all().delete()
        models.Membership.objects.all().delete()
        models.MembershipRole.objects.all().delete()
        models.Interest.objects.all().delete()
        models.InterestCategory.objects.all().delete()
        models.Identity.objects.all().delete()

    def handle(self, *args, **options):
        if options["cleanup"]:
            self.cleanup()

        interest = InterestFactory.create_batch(
            3,
            description=None,
            category=InterestCategoryFactory(title="Universitäten", description=None),
        )

        membership_roles = MembershipRoleFactory.create_batch(5)

        for _ in range(options["rounds"]):
            m = MembershipFactory(
                organisation__idp_id=None,
                identity__idp_id=None,
                role=random.choice(membership_roles),
            )
            PhoneNumberFactory.create_batch(2, identity=m.organisation)
            PhoneNumberFactory.create_batch(2, identity=m.identity)
            EmailFactory.create_batch(2, identity=m.organisation)
            EmailFactory.create_batch(2, identity=m.identity)
            m.identity.interests.add(interest[0])
            m.identity.interests.add(interest[1])
            m.organisation.interests.add(interest[1])
            m.organisation.interests.add(interest[2])
