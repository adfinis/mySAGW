import uuid

from django.db import models


class UUIDModel(models.Model):
    """
    Models which use uuid as primary key.

    Defined as mySAGW default
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Identity(UUIDModel):
    idp_id = models.CharField(max_length=255, unique=True, null=True, blank=False)
