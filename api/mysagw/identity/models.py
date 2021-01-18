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


class Identity(UUIDModel, HistoricalModel, TrackingModel):
    idp_id = models.CharField(max_length=255, unique=True, null=True, blank=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    interests = models.ManyToManyField(
        InterestOption, related_name="identities", blank=True
    )
