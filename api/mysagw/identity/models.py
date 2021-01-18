from django.db import models

from mysagw.models import HistoricalModel, TrackingModel, UUIDModel


class Identity(UUIDModel, HistoricalModel, TrackingModel):
    idp_id = models.CharField(max_length=255, unique=True, null=True, blank=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
