from django.core.mail import send_mail
from django.db import transaction

from caluma.caluma_core.events import on
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import (
    api as caluma_workflow_api,
    models as caluma_workflow_models,
)
from caluma.caluma_workflow.events import (
    post_complete_work_item,
    post_create_work_item,
    pre_complete_work_item,
)

from .. import email_texts
from ..common import get_users_for_case
from ..settings import settings


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
def send_new_work_item_mail(sender, work_item, user, **kwargs):
    if work_item.task_id not in [
        "revise-document",
        "additional-data",
        "complete-document",
    ]:
        return

    link = (
        f"{settings.SELF_URI}/cases/{work_item.case.pk}/work-items/{work_item.pk}/form"
    )

    if work_item.task_id == "complete-document":
        link = f"{settings.SELF_URI}/cases/{work_item.case.pk}"

    users = get_users_for_case(work_item.case)

    for user in users:
        subject = email_texts.EMAIL_SUBJECTS[user["language"]]
        body = email_texts.EMAIL_BODIES[user["language"]]

        body = body.format(
            first_name=user["first-name"] or "",
            last_name=user["last-name"] or "",
            link=link,
        )

        send_mail(
            subject,
            body,
            settings.MAILING_SENDER,
            [user["email"]],
            fail_silently=True,
        )


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def set_case_status(sender, work_item, user, **kwargs):
    status = settings.CASE_STATUS.get(work_item.task_id)
    if status is None:
        return
    work_item.case.meta["status"] = status
    work_item.case.save()


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


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def finish_additional_data(sender, work_item, user, **kwargs):
    if work_item.task_id == "additional-data":
        open_work_item = caluma_workflow_models.WorkItem.objects.filter(
            task_id="advance-credits",
            case=work_item.case,
            status=caluma_workflow_models.WorkItem.STATUS_READY,
        )

        if open_work_item.exists():
            caluma_workflow_api.complete_work_item(
                work_item=open_work_item.first(),
                user=user,
            )

        form_work_item = caluma_workflow_models.WorkItem.objects.filter(
            task_id="additional-data-form",
            case=work_item.case,
            status=caluma_workflow_models.WorkItem.STATUS_READY,
        )

        if form_work_item.exists():
            caluma_workflow_api.suspend_work_item(
                work_item=form_work_item.first(), user=user
            )


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def finish_define_amount(sender, work_item, user, **kwargs):
    if work_item.task_id == "define-amount":
        decision = work_item.document.answers.get(
            question_id="define-amount-decision",
        )
        form_work_item = caluma_workflow_models.WorkItem.objects.filter(
            task_id="additional-data-form",
            case=work_item.case,
        ).first()

        caluma_workflow_api.resume_work_item(work_item=form_work_item, user=user)

        if "continue" in decision.value:
            caluma_workflow_api.complete_work_item(
                work_item=form_work_item,
                user=user,
            )
