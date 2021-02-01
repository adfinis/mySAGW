import uuid

from django.db import models
from simple_history.models import HistoricalRecords


class UniqueBooleanField(models.BooleanField):
    """
    BooleanField that guarantees for one True record and sets others to `False`.

    By default only one record is allowed to be `True`. This can be further configured
    by providing a list of field names as `together` param.

    Example:
        ```
        >>> class Email(models.Model):
        ...     user = models.ForeignKey(User)
        ...     email = models.EmailField()
        ...     default = UniqueBooleanField(together=["user"])
        ```

        This will enforce three things:
         1. only allow for one entry where `default == True` per user
         2. if only one record exists for a given user, it we set `default = True`,
            regardless of the input
         3. The same happens, if records exists, but none of them have `default = True`
    """

    def __init__(self, *args, together=None, **kwargs):
        self.together = together if together else []
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        model = model_instance.__class__
        together = model.objects.filter(
            **{t: getattr(model_instance, t, None) for t in self.together},
        )

        if getattr(model_instance, self.attname) is True:
            # If True then set all others as False
            together.filter(**{self.attname: True}).update(**{self.attname: False})

        elif not together.filter(**{self.attname: True}).exists():
            # We're the only one, thus setting to True
            setattr(model_instance, self.attname, True)

        return super().pre_save(model_instance, add)


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
