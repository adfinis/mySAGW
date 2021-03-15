from django.contrib.postgres.fields import DateRangeField
from django.db import models
from localized_fields.fields import LocalizedCharField, LocalizedTextField
from phonenumber_field.modelfields import PhoneNumberField

from mysagw.models import HistoricalModel, TrackingModel, UniqueBooleanField, UUIDModel


class InterestCategory(UUIDModel, HistoricalModel):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    archived = models.BooleanField(default=False)


class Interest(UUIDModel, HistoricalModel):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        InterestCategory, related_name="interests", on_delete=models.PROTECT
    )
    archived = models.BooleanField(default=False)


class MembershipRole(UUIDModel, HistoricalModel):
    title = LocalizedCharField()
    description = LocalizedTextField(blank=True, null=True, required=False)
    archived = models.BooleanField(default=False)


class Membership(UUIDModel, HistoricalModel):
    identity = models.ForeignKey(
        "Identity",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    organisation = models.ForeignKey(
        "Identity",
        on_delete=models.CASCADE,
        related_name="members",
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
    comment = models.TextField(blank=True, null=True)
    inactive = models.BooleanField(default=False)


class Identity(UUIDModel, HistoricalModel, TrackingModel):
    idp_id = models.CharField(max_length=255, unique=True, null=True, blank=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    organisation_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    interests = models.ManyToManyField(Interest, related_name="identities", blank=True)
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

    class Meta:
        ordering = ("last_name", "first_name", "email")


class Email(UUIDModel, HistoricalModel):
    identity = models.ForeignKey(
        Identity, related_name="additional_emails", on_delete=models.CASCADE
    )
    email = models.EmailField()
    description = LocalizedCharField(blank=True, null=True, required=False)

    class Meta:
        unique_together = [["identity", "email"]]


class PhoneNumber(UUIDModel, HistoricalModel):
    identity = models.ForeignKey(
        Identity, related_name="phone_numbers", on_delete=models.CASCADE
    )
    phone = PhoneNumberField()
    description = LocalizedCharField(blank=True, null=True, required=False)
    default = UniqueBooleanField(default=False, together=["identity"])

    class Meta:
        unique_together = [["identity", "phone"]]
        ordering = ("-default",)
