from django.db import models
from localized_fields.fields import LocalizedCharField, LocalizedTextField

from mysagw.models import HistoricalModel, UUIDModel


class Snippet(UUIDModel, HistoricalModel):
    title = LocalizedCharField(blank=False, null=False, required=False)
    body = LocalizedTextField(blank=False, null=False, required=False)
    archived = models.BooleanField(default=False)
