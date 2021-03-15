from django.db import models
from localized_fields.fields import LocalizedTextField

from mysagw.models import HistoricalModel, UUIDModel


class Snippet(UUIDModel, HistoricalModel):
    title = models.CharField(max_length=255)
    body = LocalizedTextField(blank=False, null=False, required=False)
    archived = models.BooleanField(default=False)
