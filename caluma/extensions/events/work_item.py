from django.db import transaction

from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_create_work_item


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def set_assigned_user(sender, work_item, user, **kwargs):
    if work_item.task_id in ["submit-document", "revise-document", "additional-data"]:
        work_item.assigned_users = [user.claims["sub"]]
        work_item.save()
