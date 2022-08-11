import pytest
from django.utils import timezone

from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import (
    complete_work_item,
    redo_work_item,
    skip_work_item,
    start_case,
)
from caluma.caluma_workflow.models import Case, Workflow, WorkItem

from ..settings import settings


def test_work_item_set_assigned_user(
    db, caluma_data, case_access_event_mock, document_review_case
):
    assert document_review_case.work_items.get(
        task_id="submit-document"
    ).assigned_users == ["test"]


def test_work_item_create_circulation(
    db, caluma_data, case_access_event_mock, circulation
):
    assert circulation.workflow_id == "circulation"


def test_work_item_finish_circulation(
    db, caluma_data, user, case_access_event_mock, circulation
):
    complete_work_item(circulation.work_items.get(task_id="finish-circulation"), user)

    assert (
        circulation.work_items.get(task_id="invite-to-circulation").status
        == WorkItem.STATUS_CANCELED
    )


def test_work_item_additional_data(
    db, caluma_data, user, case_access_event_mock, circulation
):
    Question.objects.filter(formquestion__form__pk="additional-data-form").update(
        is_required="false"
    )

    case = circulation.parent_work_item.case

    skip_work_item(case.work_items.get(task_id="circulation"), user)

    case.work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value="decision-and-credit-decision-additional-data",
    )

    skip_work_item(case.work_items.get(task_id="decision-and-credit"), user)

    assert (
        case.work_items.get(task_id="additional-data").status == WorkItem.STATUS_READY
    )

    complete_work_item(case.work_items.get(task_id="additional-data"), user)

    assert (
        case.work_items.get(task_id="advance-credits").status == WorkItem.STATUS_READY
    )
    assert (
        case.work_items.get(task_id="additional-data-form").status
        == WorkItem.STATUS_SUSPENDED
    )


def test_work_item_define_amount(
    db, caluma_data, user, case_access_event_mock, circulation
):
    work_items = circulation.parent_work_item.case.work_items

    skip_work_item(work_items.get(task_id="circulation"), user)
    work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value="decision-and-credit-decision-additional-data",
    )
    complete_work_item(work_items.get(task_id="decision-and-credit"), user)
    complete_work_item(work_items.get(task_id="additional-data"), user)
    work_items.get(task_id="define-amount").document.answers.create(
        question_id="define-amount-decision",
        value="define-amount-decision-reject",
    )
    skip_work_item(work_items.get(task_id="define-amount"), user)

    assert (
        work_items.get(task_id="additional-data-form").status
        == WorkItem.STATUS_SUSPENDED
    )

    complete_work_item(
        work_items.get(task_id="additional-data", status=WorkItem.STATUS_READY),
        user,
    )

    answers = work_items.get(task_id="additional-data-form").document.answers

    answers.create(
        question_id="define-amount-decision",
        value="define-amount-decision-continue",
    )
    answers.create(
        question_id="additional-data-adresse",
        value="Foo",
    )
    answers.create(
        question_id="additional-data-bank",
        value="Foo",
    )
    answers.create(
        question_id="additional-data-iban",
        value="Foo",
    )
    answers.create(
        question_id="additional-data-name",
        value="Foo",
    )

    define_amount = work_items.get(
        task_id="define-amount", status=WorkItem.STATUS_READY
    )
    define_amount.document.answers.create(
        question_id="define-amount-decision",
        value="define-amount-decision-continue",
    )
    complete_work_item(define_amount, user)

    assert work_items.get(task_id="complete-document").status == WorkItem.STATUS_READY
    assert (
        work_items.get(task_id="additional-data-form").status
        == WorkItem.STATUS_COMPLETED
    )
    assert work_items.get(task_id="advance-credits").status == WorkItem.STATUS_COMPLETED
    assert circulation.parent_work_item.case.status == Case.STATUS_RUNNING


def test_work_item_invite_to_circulation(
    db, caluma_data, user, case_access_event_mock, circulation
):
    complete_work_item(
        circulation.work_items.get(task_id="invite-to-circulation"),
        user,
        {"assign_users": ["ab", "cd"]},
    )

    decisions = circulation.work_items.filter(task_id="circulation-decision")
    assert decisions.count() == 2
    assert list(
        map(lambda v: v["assigned_users"][0], decisions.values("assigned_users"))
    ) == [
        "ab",
        "cd",
    ]


def test_case_complete_circulation(
    db, caluma_data, user, case_access_event_mock, circulation
):
    complete_work_item(circulation.work_items.get(task_id="finish-circulation"), user)

    assert circulation.parent_work_item.status == WorkItem.STATUS_COMPLETED


@pytest.mark.parametrize(
    "same_year,first", [(True, False), (False, False), (False, True)]
)
def test_case_number(
    db,
    caluma_data,
    case_access_event_mock,
    user,
    form_question_factory,
    answer_factory,
    same_year,
    first,
):
    question = Question.objects.get(pk="dossier-nr")
    form_question = form_question_factory(question=question)
    old_year = year = timezone.now().year
    if not same_year:
        old_year = old_year - 1

    if not first:
        for i in range(1, 4):
            answer_factory(question=form_question.question, value=f"{old_year}-000{i}")

    expected_no = f"{year}-0004"
    if not same_year:
        expected_no = f"{year}-0001"

    case = start_case(
        workflow=Workflow.objects.get(pk="document-review"),
        form=form_question.form,
        user=user,
    )

    assert case.document.answers.get(question=question).value == expected_no


def test_case_status(
    db,
    caluma_data,
    case_access_event_mock,
    document_review_case,
    user,
):
    case = document_review_case
    assert case.meta["status"] == "submit"

    skip_work_item(case.work_items.get(task_id="submit-document"), user)
    assert case.meta["status"] == "audit"

    case.work_items.get(task_id="review-document").document.answers.create(
        question_id="review-document-decision",
        value="review-document-decision-continue",
    )
    skip_work_item(case.work_items.get(task_id="review-document"), user)
    assert case.meta["status"] == "audit"

    skip_work_item(case.work_items.get(task_id="circulation"), user)
    assert case.meta["status"] == "audit"

    case.work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value="decision-and-credit-decision-additional-data",
    )
    skip_work_item(case.work_items.get(task_id="decision-and-credit"), user)
    assert case.meta["status"] == "submit-receipts"

    skip_work_item(case.work_items.get(task_id="additional-data"), user)
    skip_work_item(case.work_items.get(task_id="additional-data-form"), user)
    assert case.meta["status"] == "decision"

    skip_work_item(case.work_items.get(task_id="advance-credits"), user)
    assert case.meta["status"] == "decision"

    case.work_items.get(task_id="define-amount").document.answers.create(
        question_id="define-amount-decision",
        value="define-amount-decision-continue",
    )
    skip_work_item(case.work_items.get(task_id="define-amount"), user)
    assert case.meta["status"] == "decision"

    skip_work_item(case.work_items.get(task_id="complete-document"), user)
    assert case.meta["status"] == "complete"


def test_send_new_work_item_mail(
    db, user, caluma_data, case_access_event_mock, document_review_case, mailoutbox
):
    case = document_review_case

    skip_work_item(case.work_items.get(task_id="submit-document"), user)

    case.work_items.get(task_id="review-document").document.answers.create(
        question_id="review-document-decision",
        value="review-document-decision-reject",
    )

    complete_work_item(case.work_items.get(task_id="review-document"), user)
    assert len(mailoutbox) == 1
    assert mailoutbox[0].from_email == settings.MAILING_SENDER
    assert mailoutbox[0].to == ["test-send@example.com"]


def test_access_control(
    db,
    caluma_data,
    user,
    identities_mock,
    form_question_factory,
    get_token_mock,
    case_access_create_request_mock,
):
    form_question = form_question_factory()

    start_case(
        workflow=Workflow.objects.get(pk="document-review"),
        form=form_question.form,
        user=user,
    )
    assert case_access_create_request_mock.called


def test_redo_circulation(
    db,
    caluma_data,
    user,
    case_access_event_mock,
    circulation,
):
    Question.objects.filter(formquestion__form__pk="additional-data-form").update(
        is_required="false"
    )

    circ_work_item = circulation.parent_work_item

    skip_work_item(circ_work_item.case.work_items.get(task_id="circulation"), user)

    assert (
        circ_work_item.child_case.work_items.get(task_id="finish-circulation").status
        == WorkItem.STATUS_CANCELED
    )

    redo_work_item(circ_work_item.case.work_items.get(task_id="circulation"), user)

    circ_work_item.refresh_from_db()
    assert (
        circ_work_item.child_case.work_items.get(task_id="finish-circulation").status
        == WorkItem.STATUS_READY
    )


@pytest.mark.parametrize(
    "decision,expected_work_item_task",
    [
        (
            "define-amount",
            "define-amount",
        ),
        (
            "additional-data",
            "advance-credits",
        ),
    ],
)
def test_redo_define_amount(
    db,
    caluma_data,
    user,
    case_access_event_mock,
    circulation,
    decision,
    expected_work_item_task,
):
    Question.objects.filter(formquestion__form__pk="additional-data-form").update(
        is_required="false"
    )

    case = circulation.parent_work_item.case

    skip_work_item(case.work_items.get(task_id="circulation"), user)

    case.work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value=f"decision-and-credit-decision-{decision}",
    )

    complete_work_item(case.work_items.get(task_id="decision-and-credit"), user)
    if decision != "define-amount":
        complete_work_item(case.work_items.get(task_id="additional-data"), user)

    case.work_items.get(task_id="define-amount").document.answers.create(
        question_id="define-amount-decision", value="define-amount-decision-continue"
    )

    complete_work_item(case.work_items.get(task_id="define-amount"), user)

    redo_work_item(case.work_items.get(task_id="define-amount"), user)

    assert case.status == Case.STATUS_RUNNING
    assert case.work_items.filter(
        task_id=expected_work_item_task, status=WorkItem.STATUS_READY
    ).exists()
