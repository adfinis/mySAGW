from django.db import transaction

from caluma.caluma_core.events import on
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import (
    api as caluma_workflow_api,
    models as caluma_workflow_models,
)
from caluma.caluma_workflow.events import post_create_work_item


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def set_assigned_user(sender, work_item, user, **kwargs):
    if work_item.task_id in ["submit-document", "revise-document", "additional-data"]:
        work_item.assigned_users = [user.claims["sub"]]
        work_item.save()


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def create_circulation_child_case(sender, work_item, user, **kwargs):
    if work_item.task_id == "circulation":
        case = caluma_workflow_api.start_case(
            workflow=caluma_workflow_models.Workflow.objects.get(pk="circulation"),
            form=caluma_form_models.Form.objects.get(pk="circulation-form"),
            user=user,
            parent_work_item=work_item,
        )

        work_item = case.work_items.all().first()
        work_item.assigned_users = [user.claims["sub"]]
        work_item.save()
