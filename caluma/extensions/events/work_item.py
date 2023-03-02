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
    post_redo_work_item,
    pre_complete_work_item,
)

from ..common import format_currency, get_users_for_case
from ..email_texts import email_cost_approval, email_general, email_payout_amount
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


def _send_new_work_item_mail(work_item):
    """
    Send the work_item emails.

    This must reside in a separate function in order to be able to patch it in the
    tests.
    """
    link = f"{settings.SELF_URI}/cases/{work_item.case.pk}"

    try:
        dossier_nr = work_item.case.document.answers.get(question_id="dossier-nr").value
    except caluma_form_models.Answer.DoesNotExist:
        dossier_nr = "Not found"

    framework_credit = None
    payout_amount = None
    selected_email_texts = email_general

    if work_item.task.slug == "additional-data":
        define_amount_work_item = (
            work_item.case.work_items.filter(task__slug="define-amount")
            .order_by("-closed_at")
            .first()
        )
        if not (
            define_amount_work_item
            and define_amount_work_item.status == "completed"
            and define_amount_work_item.document.answers.filter(
                question_id="define-amount-decision",
                value="define-amount-decision-reject",
            ).exists()
        ):
            decision_and_credit_work_item = (
                work_item.case.work_items.filter(task__slug="decision-and-credit")
                .order_by("-created_at")
                .first()
            )
            framework_credit = decision_and_credit_work_item.document.answers.get(
                question__slug="gesprochener-rahmenkredit"
            ).value
            framework_credit = format_currency(framework_credit, "CHF")
            selected_email_texts = email_cost_approval
    elif work_item.task.slug == "complete-document":
        define_amount_work_item = (
            work_item.case.work_items.filter(task__slug="define-amount")
            .order_by("-created_at")
            .first()
        )
        payout_amount_answer = define_amount_work_item.document.answers.filter(
            question__slug="define-amount-amount-float"
        ).first()
        payout_amount = format_currency(
            payout_amount_answer.value if payout_amount_answer else 0, "CHF"
        )
        selected_email_texts = email_payout_amount

    users = get_users_for_case(work_item.case)

    for user in users:
        subject = selected_email_texts.EMAIL_SUBJECTS[user["language"]]

        subject = subject.format(dossier_nr=dossier_nr)

        body = selected_email_texts.EMAIL_BODIES[user["language"]]

        body = body.format(
            first_name=user["first-name"] or "",
            last_name=user["last-name"] or "",
            link=link,
            dossier_nr=dossier_nr,
            framework_credit=framework_credit,
            payout_amount=payout_amount,
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
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id
    in [
        "revise-document",
        "additional-data",
        "complete-document",
    ]
)
def send_new_work_item_mail(sender, work_item, user, **kwargs):
    _send_new_work_item_mail(work_item)


@on(post_create_work_item, raise_exception=True)
@filter_events(
    lambda sender: sender
    in [
        "post_complete_work_item",
        "post_skip_work_item",
        "case_post_create",
        "post_redo_work_item",
    ]
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

    if work_item:
        caluma_workflow_api.complete_work_item(
            work_item=work_item,
            user=user,
        )


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


@on(post_create_work_item, raise_exception=True)
@filter_events(lambda sender, work_item: work_item.task_id == "complete-document")
@transaction.atomic
def complete_additional_data_form(sender, work_item, user, **kwargs):
    form_work_item = caluma_workflow_models.WorkItem.objects.filter(
        task_id="additional-data-form",
        case=work_item.case,
        status=caluma_workflow_models.WorkItem.STATUS_READY,
    ).first()

    if form_work_item:
        caluma_workflow_api.complete_work_item(
            work_item=form_work_item,
            user=user,
        )


@on(post_redo_work_item, raise_exception=True)
@filter_events(lambda sender, work_item: work_item.task_id == "circulation")
@transaction.atomic
def redo_circulation(sender, work_item, user, **kwargs):
    work_item.child_case = caluma_workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="circulation"),
        form=caluma_form_models.Form.objects.get(pk="circulation-form"),
        user=user,
        parent_work_item=work_item,
    )
    work_item.save()


@on(post_redo_work_item, raise_exception=True)
@filter_events(lambda sender, work_item: work_item.task_id == "define-amount")
@transaction.atomic
def redo_define_amount(sender, work_item, user, **kwargs):
    credit_decision = (
        work_item.case.work_items.filter(task_id="decision-and-credit")
        .order_by("-created_at")
        .first()
        .document.answers.get(
            question_id="decision-and-credit-decision",
        )
    )

    if "additional-data" in credit_decision.value:
        advance_credits = (
            work_item.case.work_items.filter(task__slug="advance-credits")
            .order_by("-created_at")
            .first()
        )
        data_form = (
            work_item.case.work_items.filter(task__slug="additional-data-form")
            .order_by("-created_at")
            .first()
        )

        # This can't be done over caluma_workflow_api because they are the last work items of a "branch",
        # consequently they don't have another following work item which defines redoable for them.
        advance_credits.status = caluma_workflow_models.WorkItem.STATUS_READY
        advance_credits.save()
        data_form.status = caluma_workflow_models.WorkItem.STATUS_SUSPENDED
        data_form.save()


@on(post_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id == "additional-data"
)
@transaction.atomic
def close_multiple_define_amount(sender, work_item, user, **kwargs):
    """
    Close all define-amount WorkItems.

    So the new that will open afterwards will be the only one.

    TODO: This is an ugly hack and we want to get rid of it.
    """
    define_amount = work_item.case.work_items.filter(
        task_id="define-amount", status=caluma_workflow_models.WorkItem.STATUS_REDO
    )
    define_amount.update(status=caluma_workflow_models.WorkItem.STATUS_CANCELED)
