from django.db.models.signals import post_save
from django.dispatch import receiver

from mysagw.case.models import CaseAccess
from mysagw.identity.models import Identity


@receiver(post_save, sender=Identity)
def assign_cases(sender, instance, created, **kwargs):
    if not created:
        return
    CaseAccess.objects.filter(email=instance.email).update(
        email=None, identity=instance
    )
