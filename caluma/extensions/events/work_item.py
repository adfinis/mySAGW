from django.core.mail import send_mail
from django.db import transaction

from caluma.caluma_core.events import filter_events, on
from caluma.caluma_form import api as caluma_form_api, models as caluma_form_models
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
@filter_events(lambda sender: sender in ["post_complete_work_item", "case_post_create"])
@transaction.atomic
def set_assigned_user(sender, work_item, user, **kwargs):
    if work_item.task_id == "submit-document":
        work_item.assigned_users = [user.claims["sub"]]
    elif work_item.task_id in [
        "revise-document",
        "additional-data",
        "additional-data-form",
    ]:
        work_item.assigned_users = caluma_workflow_models.WorkItem.objects.get(
            task_id="submit-document", case=work_item.case
        ).assigned_users

    work_item.save()


@on(post_create_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id
    in [
        "revise-document",
        "additional-data",
        "complete-document",
    ]
)
def send_new_work_item_mail(sender, work_item, user, **kwargs):
    link = f"{settings.SELF_URI}/cases/{work_item.case.pk}"

    try:
        dossier_nr = work_item.case.document.answers.get(question_id="dossier-nr").value
    except caluma_form_models.Answer.DoesNotExist:
        dossier_nr = "Not found"

    users = get_users_for_case(work_item.case)

    for user in users:
        subject = email_texts.EMAIL_SUBJECTS[user["language"]]

        subject = subject.format(dossier_nr=dossier_nr)

        body = email_texts.EMAIL_BODIES[user["language"]]

        body = body.format(
            first_name=user["first-name"] or "",
            last_name=user["last-name"] or "",
            link=link,
            dossier_nr=dossier_nr,
        )

        send_mail(
            subject,
            body,
            settings.MAILING_SENDER,
            [user["email"]],
            fail_silently=True,
        )


@on(post_create_work_item, raise_exception=True)
@filter_events(
    lambda sender: sender
    in ["post_complete_work_item", "post_skip_work_item", "case_post_create"]
)
@transaction.atomic
def set_case_status(sender, work_item, user, **kwargs):
    status = settings.CASE_STATUS.get(work_item.task_id)
    if status is None:
        return
    work_item.case.meta["status"] = status
    work_item.case.save()


@on(post_create_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender
    in ["post_complete_work_item", "post_skip_work_item"]
    and work_item.task_id == "circulation"
    and not work_item.child_case
)
@transaction.atomic
def create_circulation_child_case(sender, work_item, user, **kwargs):
    caluma_workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="circulation"),
        form=caluma_form_models.Form.objects.get(pk="circulation-form"),
        user=user,
        parent_work_item=work_item,
    )


@on(post_create_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item, context: sender == "post_complete_work_item"
    and work_item.task_id == "circulation-decision"
    and context is not None
)
@transaction.atomic
def invite_to_circulation(sender, work_item, user, context, **kwargs):
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


@on(post_create_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id == "additional-data-form"
)
@transaction.atomic
def create_additional_data_form_document(sender, work_item, user, context, **kwargs):
    form_slug = settings.ADDITIONAL_DATA_FORM.get(
        work_item.case.document.form_id, "additional-data-form"
    )
    if work_item.case.document.form_id == settings.INTERNAL_APPLICATION_FORM_SLUG:
        answer = work_item.case.document.answers.filter(
            question__slug=settings.INTERNAL_APPLICATION_TYPE_QUESTION_SLUG
        )
        if (
            answer
            and answer.first().value in settings.INTERNAL_APPLICATION_PERIODICS_CHOICES
        ):
            form_slug = settings.ADDITIONAL_DATA_FORM["periodika-antrag"]

    form = caluma_form_models.Form.objects.get(slug=form_slug)

    work_item.document = caluma_form_api.save_document(form=form, user=user)
    work_item.save()


@on(pre_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "pre_complete_work_item"
    and work_item.task_id == "finish-circulation"
)
@transaction.atomic
def finish_circulation(sender, work_item, user, **kwargs):
    caluma_workflow_api.cancel_work_item(
        work_item=caluma_workflow_models.WorkItem.objects.get(
            task_id="invite-to-circulation",
            case=work_item.case,
            status=caluma_workflow_models.WorkItem.STATUS_READY,
        ),
        user=user,
    )


@on(post_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id == "additional-data"
)
@transaction.atomic
def finish_additional_data(sender, work_item, user, **kwargs):
    form_work_item = caluma_workflow_models.WorkItem.objects.filter(
        task_id="additional-data-form",
        case=work_item.case,
        status=caluma_workflow_models.WorkItem.STATUS_READY,
    ).first()

    if form_work_item:
        caluma_workflow_api.suspend_work_item(work_item=form_work_item, user=user)


@on(post_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id == "additional-data-form"
)
@transaction.atomic
def finish_additional_data_form(sender, work_item, user, **kwargs):
    work_item = caluma_workflow_models.WorkItem.objects.filter(
        task_id="advance-credits",
        case=work_item.case,
        status=caluma_workflow_models.WorkItem.STATUS_READY,
    ).first()

    caluma_workflow_api.complete_work_item(
        work_item=work_item,
        user=user,
    )

    assert work_item.case.status == caluma_workflow_models.Case.STATUS_RUNNING


@on(post_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id == "define-amount"
)
@transaction.atomic
def finish_define_amount(sender, work_item, user, **kwargs):
    decision = work_item.document.answers.get(
        question_id="define-amount-decision",
    )

    if any(state in decision.value for state in ["zurueckgezogen", "dismissed"]):
        for sibling in work_item.case.work_items.filter(
            status=caluma_workflow_models.WorkItem.STATUS_READY
        ):
            caluma_workflow_api.complete_work_item(
                work_item=sibling,
                user=user,
            )
        return

    form_work_item = caluma_workflow_models.WorkItem.objects.filter(
        task_id="additional-data-form",
        case=work_item.case,
        status=caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
    ).first()

    if form_work_item:
        caluma_workflow_api.resume_work_item(work_item=form_work_item, user=user)

        if "continue" in decision.value:
            caluma_workflow_api.complete_work_item(
                work_item=form_work_item,
                user=user,
            )
