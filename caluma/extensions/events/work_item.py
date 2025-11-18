from django.db import transaction

from caluma.caluma_core.events import filter_events, on
from caluma.caluma_form import api as caluma_form_api
from caluma.caluma_form.models import Document, Form
from caluma.caluma_workflow import (
    api as caluma_workflow_api,
)
from caluma.caluma_workflow.events import (
    post_complete_work_item,
    post_create_work_item,
    post_redo_work_item,
    post_reopen_case,
    pre_complete_work_item,
)
from caluma.caluma_workflow.models import Case, Workflow, WorkItem

from ..email.send_email import send_work_item_mail
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
        work_item.assigned_users = WorkItem.objects.get(
            task_id="submit-document",
            case=work_item.case,
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
    ],
)
def send_new_work_item_mail(sender, work_item, user, **kwargs):
    send_work_item_mail(work_item)


@on(post_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: work_item.task_id
    in ["review-document", "decision-and-credit"]
    and (
        work_item.document.answers.filter(
            question_id="decision-and-credit-decision",
            value="decision-and-credit-decision-close",
        ).exists()
        or work_item.document.answers.filter(
            question_id="review-document-decision",
            value="review-document-decision-complete",
        ).exists()
    ),
)
def send_rejection_mail(sender, work_item, user, **kwargs):
    send_work_item_mail(work_item)


@on(post_reopen_case, raise_exception=True)
@filter_events(lambda case: case.workflow.slug == "document-review")
@transaction.atomic
def set_case_status_post_reopen_case(
    sender,
    case,
    user,
    work_items,
    **kwargs,
):
    work_item = case.work_items.filter(status=WorkItem.STATUS_READY).first()
    status = settings.CASE_STATUS.get(work_item.task_id)
    if status is None:  # pragma: no cover
        # Shouldn't happen, if all tasks are correctly added to `settings.CASE_STATUS`
        return
    case.meta["status"] = status
    case.save()


@on(post_create_work_item, raise_exception=True)
@filter_events(lambda work_item: work_item.case.workflow.slug == "document-review")
@transaction.atomic
def set_case_status_post_create_work_item(
    sender,
    work_item,
    user,
    **kwargs,
):
    status = settings.CASE_STATUS.get(work_item.task_id)
    if status is None:  # pragma: no cover
        # Shouldn't happen, if all tasks are correctly added to `settings.CASE_STATUS`
        return
    work_item.case.meta["status"] = status
    work_item.case.save()


@on(post_create_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender
    in ["post_complete_work_item", "post_skip_work_item"]
    and work_item.task_id == "circulation"
    and not work_item.child_case,
)
@transaction.atomic
def create_circulation_child_case(sender, work_item, user, **kwargs):
    caluma_workflow_api.start_case(
        workflow=Workflow.objects.get(pk="circulation"),
        form=Form.objects.get(pk="circulation-form"),
        user=user,
        parent_work_item=work_item,
    )


@on(post_create_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item, context: sender == "post_complete_work_item"
    and work_item.task_id == "circulation-decision"
    and context is not None,
)
@transaction.atomic
def invite_to_circulation(sender, work_item, user, context, **kwargs):
    for index, assign_user in enumerate(context["assign_users"]):
        if index == 0:
            work_item.assigned_users = [assign_user["idpId"]]
            work_item.meta["assigneeName"] = assign_user["name"]
            work_item.meta["assigneeEmail"] = assign_user["email"]
            work_item.save()
            continue

        WorkItem.objects.create(
            name=work_item.task.name,
            description=work_item.task.description,
            task=work_item.task,
            status=WorkItem.STATUS_READY,
            assigned_users=[assign_user["idpId"]],
            meta={
                "assigneeName": assign_user["name"],
                "assigneeEmail": assign_user["email"],
            },
            case=work_item.case,
            document=Document.objects.create(
                form=work_item.document.form,
            ),
        )


@on(post_create_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id == "additional-data-form",
)
@transaction.atomic
def create_additional_data_form_document(sender, work_item, user, context, **kwargs):
    form_slug = settings.ADDITIONAL_DATA_FORM.get(
        work_item.case.document.form_id,
        "additional-data-form",
    )
    if work_item.case.document.form_id == settings.INTERNAL_APPLICATION_FORM_SLUG:
        answer = work_item.case.document.answers.filter(
            question__slug=settings.INTERNAL_APPLICATION_TYPE_QUESTION_SLUG,
        )
        if (
            answer
            and answer.first().value in settings.INTERNAL_APPLICATION_PERIODICS_CHOICES
        ):
            form_slug = settings.ADDITIONAL_DATA_FORM["periodika-antrag"]

    form = Form.objects.get(slug=form_slug)

    work_item.document = caluma_form_api.save_document(form=form, user=user)
    work_item.save()


@on(pre_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "pre_complete_work_item"
    and work_item.task_id == "finish-circulation",
)
@transaction.atomic
def finish_circulation(sender, work_item, user, **kwargs):
    caluma_workflow_api.cancel_work_item(
        work_item=WorkItem.objects.get(
            task_id="invite-to-circulation",
            case=work_item.case,
            status=WorkItem.STATUS_READY,
        ),
        user=user,
    )


@on(post_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id == "additional-data",
)
@transaction.atomic
def finish_additional_data(sender, work_item, user, **kwargs):
    form_work_item = WorkItem.objects.filter(
        task_id="additional-data-form",
        case=work_item.case,
        status=WorkItem.STATUS_READY,
    ).first()

    if form_work_item:
        caluma_workflow_api.suspend_work_item(work_item=form_work_item, user=user)


@on(post_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id == "additional-data-form",
)
@transaction.atomic
def finish_additional_data_form(sender, work_item, user, **kwargs):
    work_item = WorkItem.objects.filter(
        task_id="advance-credits",
        case=work_item.case,
        status=WorkItem.STATUS_READY,
    ).first()

    if work_item:
        caluma_workflow_api.complete_work_item(
            work_item=work_item,
            user=user,
        )


@on(post_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id == "define-amount",
)
@transaction.atomic
def finish_define_amount(sender, work_item, user, **kwargs):
    decision = work_item.document.answers.get(
        question_id="define-amount-decision",
    )

    if any(state in decision.value for state in ["zurueckgezogen", "dismissed"]):
        for sibling in work_item.case.work_items.filter(
            status=WorkItem.STATUS_READY,
        ):
            caluma_workflow_api.complete_work_item(
                work_item=sibling,
                user=user,
            )
        return

    form_work_item = WorkItem.objects.filter(
        task_id="additional-data-form",
        case=work_item.case,
        status=WorkItem.STATUS_SUSPENDED,
    ).first()

    if form_work_item:
        caluma_workflow_api.resume_work_item(work_item=form_work_item, user=user)


@on(pre_complete_work_item, raise_exception=True)
@filter_events(lambda sender, work_item: work_item.task_id == "define-amount")
@transaction.atomic
def redo_to_decision_and_credit(sender, work_item, user, **kwargs):
    # fix workflow edge case where there is no additional-data-form
    # due to skipping it from decision-and-credit
    decision_and_credit = (
        WorkItem.objects.filter(case=work_item.case, task_id="decision-and-credit")
        .order_by("-created_at")
        .first()
    )
    if (
        work_item
        and work_item.document.answers.filter(
            question_id="define-amount-decision",
            value="define-amount-decision-reject",
        ).exists()
        and decision_and_credit.status != WorkItem.STATUS_READY
        and (
            decision_and_credit.document.answers.filter(
                question_id="decision-and-credit-decision",
                value="decision-and-credit-decision-define-amount",
            ).exists()
        )
    ):
        caluma_workflow_api.redo_work_item(
            work_item=decision_and_credit,
            user=user,
        )


@on(post_create_work_item, raise_exception=True)
@filter_events(lambda sender, work_item: work_item.task_id == "complete-document")
@transaction.atomic
def complete_additional_data_form(sender, work_item, user, **kwargs):
    form_work_item = WorkItem.objects.filter(
        task_id="additional-data-form",
        case=work_item.case,
        status=WorkItem.STATUS_READY,
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
    caluma_workflow_api.reopen_case(
        work_item.child_case,
        [
            work_item.child_case.work_items.get(task_id="finish-circulation"),
            work_item.child_case.work_items.filter(task_id="invite-to-circulation")
            .order_by("-created_at")
            .first(),
        ],
        user,
    )


@on(post_redo_work_item, raise_exception=True)
@filter_events(lambda sender, work_item: work_item.task_id == "review-document")
@transaction.atomic
def redo_review_document(sender, work_item, user, **kwargs):
    circulation_wi = work_item.case.work_items.get(task_id="circulation")

    # Set status of possible old circulation case and all its workitems to `canceled`
    if old_circulation := circulation_wi.child_case:
        for wi in old_circulation.work_items.all():
            wi.status = WorkItem.STATUS_CANCELED
            wi.save()
        old_circulation.status = Case.STATUS_CANCELED
        old_circulation.save()

    circulation_wi.child_case = caluma_workflow_api.start_case(
        workflow=Workflow.objects.get(pk="circulation"),
        form=Form.objects.get(pk="circulation-form"),
        user=user,
        parent_work_item=circulation_wi,
    )
    circulation_wi.save()


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
        advance_credits.status = WorkItem.STATUS_READY
        advance_credits.save()
        data_form.status = WorkItem.STATUS_SUSPENDED
        data_form.save()


@on(post_complete_work_item, raise_exception=True)
@filter_events(
    lambda sender, work_item: sender == "post_complete_work_item"
    and work_item.task_id == "additional-data",
)
@transaction.atomic
def close_multiple_define_amount(sender, work_item, user, **kwargs):
    """
    Close all define-amount WorkItems.

    So the new that will open afterwards will be the only one.

    TODO: This is an ugly hack and we want to get rid of it.
    """
    define_amount = work_item.case.work_items.filter(
        task_id="define-amount",
        status=WorkItem.STATUS_REDO,
    )
    define_amount.update(status=WorkItem.STATUS_CANCELED)
