from django.db import models

from mysagw.identity.models import Identity
from mysagw.models import HistoricalModel, UUIDModel


class CaseAccess(UUIDModel, HistoricalModel):
    case_id = models.UUIDField()
    identity = models.ForeignKey(
        Identity,
        related_name="cases",
        on_delete=models.CASCADE,
        null=True,
    )
    email = models.EmailField(null=True)

    class Meta:
        unique_together = [["case_id", "email"], ["case_id", "identity"]]
