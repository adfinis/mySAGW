from django.db import transaction

from caluma.caluma_core.events import on
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import (
    api as caluma_workflow_api,
    models as caluma_workflow_models,
)
from caluma.caluma_workflow.events import post_create_work_item, pre_complete_work_item


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def set_assigned_user(sender, work_item, user, **kwargs):
    if work_item.task_id == "submit-document":
        work_item.assigned_users = [user.claims["sub"]]
    elif work_item.task_id in ["revise-document", "additional-data"]:
        work_item.assigned_users = caluma_workflow_models.WorkItem.objects.get(
            task_id="submit-document", case=work_item.case
        ).assigned_users

    work_item.save()


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def create_circulation_child_case(sender, work_item, user, **kwargs):
    if work_item.task_id == "circulation":
        caluma_workflow_api.start_case(
            workflow=caluma_workflow_models.Workflow.objects.get(pk="circulation"),
            form=caluma_form_models.Form.objects.get(pk="circulation-form"),
            user=user,
            parent_work_item=work_item,
        )


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def invite_to_circulation(sender, work_item, user, context, **kwargs):
    if work_item.task_id != "circulation-decision" or context is None:
        return

    for index, assign_user in enumerate(context["assign_users"]):
        if index == 0:
            work_item.assigned_users = [assign_user]
            work_item.save()
            continue

        caluma_workflow_models.WorkItem.objects.create(
            name=work_item.task.name,
            description=work_item.task.description,
            task=work_item.task,
            status=caluma_workflow_models.WorkItem.STATUS_READY,
            assigned_users=[assign_user],
            case=work_item.case,
            document=caluma_form_models.Document.objects.create(
                form=work_item.document.form
            ),
        )


@on(pre_complete_work_item, raise_exception=True)
@transaction.atomic
def finish_circulation(sender, work_item, user, **kwargs):
    if work_item.task_id == "finish-circulation":
        caluma_workflow_api.cancel_work_item(
            work_item=caluma_workflow_models.WorkItem.objects.get(
                task_id="invite-to-circulation",
                case=work_item.case,
                status=caluma_workflow_models.WorkItem.STATUS_READY,
            ),
            user=user,
        )
