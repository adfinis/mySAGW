from django.contrib.postgres.fields import DateRangeField
from django.db import models
from localized_fields.fields import LocalizedCharField, LocalizedTextField

from mysagw.models import HistoricalModel, TrackingModel, UUIDModel


class InterestCategory(UUIDModel, HistoricalModel):
    title = LocalizedCharField()
    description = LocalizedTextField(blank=True, null=True, required=False)
    archived = models.BooleanField(default=False)


class InterestOption(UUIDModel, HistoricalModel):
    title = LocalizedCharField()
    description = LocalizedTextField(blank=True, null=True, required=False)
    category = models.ForeignKey(
        InterestCategory, related_name="options", on_delete=models.PROTECT
    )
    archived = models.BooleanField(default=False)


class MembershipRole(UUIDModel, HistoricalModel):
    title = LocalizedCharField()
    description = LocalizedTextField(blank=True, null=True, required=False)
    archived = models.BooleanField(default=False)


class Membership(UUIDModel, HistoricalModel):
    identity = models.ForeignKey(
        "Identity", on_delete=models.CASCADE, related_name="members",
    )
    organisation = models.ForeignKey(
        "Identity", on_delete=models.CASCADE, related_name="memberships",
    )
    role = models.ForeignKey(
        MembershipRole,
        related_name="memberships",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    authorized = models.BooleanField(default=False)
    time_slot = DateRangeField(null=True, blank=True)
    next_election = models.DateField(null=True, blank=True)
    comment = LocalizedTextField(blank=True, null=True, required=False)
    inactive = models.BooleanField(default=False)


class Identity(UUIDModel, HistoricalModel, TrackingModel):
    idp_id = models.CharField(max_length=255, unique=True, null=True, blank=False)
    organisation_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    interests = models.ManyToManyField(
        InterestOption, related_name="identities", blank=True
    )
    is_organisation = models.BooleanField(default=False)

    def _get_memberships(self, only_authorized=False):
        memberships = Membership.objects.filter(identity=self)
        if only_authorized:
            memberships = memberships.filter(authorized=True)
        return self.__class__.objects.filter(
            pk__in=memberships.values_list("organisation", flat=True).distinct()
        )

    @property
    def authorized_for(self):
        return self._get_memberships(only_authorized=True)

    @property
    def member_of(self):
        return self._get_memberships(only_authorized=False)
