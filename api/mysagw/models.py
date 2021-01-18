import uuid

from django.db import models
from simple_history.models import HistoricalRecords


def _history_user_getter(historical_instance):  # pragma: todo cover
    return historical_instance.history_user_id


def _history_user_setter(historical_instance, user):
    request = getattr(HistoricalRecords.thread, "request", None)
    user = None
    if request is not None:
        user = request.user.username
    historical_instance.history_user_id = user


class HistoricalModel(models.Model):
    history = HistoricalRecords(
        inherit=True,
        history_user_id_field=models.CharField(null=True, max_length=150),
        history_user_setter=_history_user_setter,
        history_user_getter=_history_user_getter,
    )

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    Models which use uuid as primary key.

    Defined as mySAGW default
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by_user = models.CharField(
        max_length=255, blank=True, null=True, db_index=True
    )
    modified_at = models.DateTimeField(auto_now=True, db_index=True)
    modified_by_user = models.CharField(
        max_length=255, blank=True, null=True, db_index=True
    )

    class Meta:
        abstract = True
