import pytest
from django.core.exceptions import ValidationError

from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import (
    complete_work_item,
    redo_work_item,
    skip_work_item,
)
from caluma.caluma_workflow.models import Case, WorkItem


@pytest.mark.parametrize(
    "decision,expected_case_status,expected_work_item",
    [
        ("complete", Case.STATUS_COMPLETED, ""),
        ("continue", Case.STATUS_RUNNING, "circulation"),
        ("reject", Case.STATUS_RUNNING, "revise-document"),
    ],
)
def test_dynamic_task_after_review_document(
    db,
    caluma_data,
    user,
    case_access_event_mock,
    document_review_case,
    decision,
    expected_case_status,
    expected_work_item,
):
    case = document_review_case

    complete_work_item(case.work_items.get(task_id="submit-document"), user)

    case.work_items.get(task_id="review-document").document.answers.create(
        question_id="review-document-decision",
        value=f"review-document-decision-{decision}",
    )

    complete_work_item(case.work_items.get(task_id="review-document"), user)

    case.refresh_from_db()

    assert case.status == expected_case_status

    if case.status == Case.STATUS_RUNNING:
        assert case.work_items.filter(task_id=expected_work_item).exists()


@pytest.mark.parametrize(
    "decision,expected_case_status,expected_work_item",
    [
        ("close", Case.STATUS_COMPLETED, ""),
        ("additional-data", Case.STATUS_RUNNING, "additional-data"),
        ("define-amount", Case.STATUS_RUNNING, "define-amount"),
        ("complete", Case.STATUS_COMPLETED, ""),
    ],
)
def test_dynamic_task_after_decision_and_credit(
    db,
    caluma_data,
    user,
    case_access_event_mock,
    circulation,
    decision,
    expected_case_status,
    expected_work_item,
    send_mail_mock,
):
    case = circulation.parent_work_item.case

    skip_work_item(case.work_items.get(task_id="circulation"), user)

    case.work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value=f"decision-and-credit-decision-{decision}",
    )

    complete_work_item(case.work_items.get(task_id="decision-and-credit"), user)

    case.refresh_from_db()

    assert case.status == expected_case_status

    if case.status == Case.STATUS_RUNNING:
        assert case.work_items.filter(task_id=expected_work_item).exists()


def test_workflow_edge_cases(
    db,
    caluma_data,
    user,
    case_access_event_mock,
    circulation,
    send_mail_mock,
):
    case = circulation.parent_work_item.case

    skip_work_item(case.work_items.get(task_id="circulation"), user)

    decision_and_credit = case.work_items.get(task_id="decision-and-credit")
    decision_and_credit.document.answers.create(
        question_id="decision-and-credit-decision",
        value="decision-and-credit-decision-additional-data",
    )

    complete_work_item(decision_and_credit, user)

    case.refresh_from_db()

    assert case.work_items.filter(task_id="additional-data").exists()

    for i in range(2):
        print(i)
        complete_work_item(
            case.work_items.get(
                task_id="additional-data", status=WorkItem.STATUS_READY
            ),
            user,
        )
        define_amount = case.work_items.get(
            task_id="define-amount", status=WorkItem.STATUS_READY
        )
        define_amount.document.answers.create(
            question_id="define-amount-decision",
            value="define-amount-decision-reject",
        )
        complete_work_item(define_amount, user)

    redo_work_item(decision_and_credit, user)

    assert case.work_items.filter(task_id="additional-data").count() == 3

    complete_work_item(decision_and_credit, user)

    assert (
        case.work_items.filter(
            task_id="additional-data", status=WorkItem.STATUS_READY
        ).count()
        == 1
    )

    redo_work_item(decision_and_credit, user)
    answer = decision_and_credit.document.answers.get(
        question_id="decision-and-credit-decision",
    )
    answer.value = "decision-and-credit-decision-define-amount"
    answer.save()

    complete_work_item(decision_and_credit, user)

    define_amount = case.work_items.filter(
        task_id="define-amount", status=WorkItem.STATUS_READY
    )
    assert define_amount.count() == 1
    define_amount.first().document.answers.get(
        question_id="define-amount-decision",
    ).value = "define-amount-decision-reject"
    complete_work_item(define_amount.first(), user)

    assert (
        case.work_items.filter(
            task_id="additional-data", status=WorkItem.STATUS_READY
        ).count()
        == 1
    )


@pytest.mark.parametrize(
    "decision,expected_work_item_task,expected_work_item_form,internal_periodics",
    [
        ("continue", "complete-document", None, False),
        ("reject", "additional-data-form", "additional-data-form", False),
        ("dismissed", None, None, False),
        ("reject", "additional-data-form", "periodika-abrechnung", True),
    ],
)
def test_dynamic_task_after_define_amount(
    db,
    caluma_data,
    user,
    case_access_event_mock,
    circulation,
    answer_factory,
    form_factory,
    decision,
    expected_work_item_form,
    expected_work_item_task,
    internal_periodics,
    send_mail_mock,
):
    Question.objects.filter(formquestion__form__pk="additional-data-form").update(
        is_required="false"
    )

    case = circulation.parent_work_item.case

    if internal_periodics:
        form_factory(slug="periodika-abrechnung")
        case.document.form.slug = "intern"
        case.document.form.save()
        case.document.form_id = "intern"
        case.document.save()
        answer_factory(
            value="intern-gesuchsart-intern-abrechnung-periodika",
            question__slug="intern-gesuchsart",
            document=case.document,
        )

    skip_work_item(case.work_items.get(task_id="circulation"), user)

    case.work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value="decision-and-credit-decision-additional-data",
    )

    complete_work_item(case.work_items.get(task_id="decision-and-credit"), user)
    complete_work_item(case.work_items.get(task_id="additional-data"), user)

    case.work_items.get(task_id="define-amount").document.answers.create(
        question_id="define-amount-decision",
        value=f"define-amount-decision-{decision}",
    )
    complete_work_item(case.work_items.get(task_id="define-amount"), user)

    if expected_work_item_task:
        assert case.status == Case.STATUS_RUNNING
        assert case.work_items.filter(task_id=expected_work_item_task).exists()
        if expected_work_item_form:
            assert (
                case.work_items.filter(task_id=expected_work_item_task)
                .first()
                .document.form.slug
                == expected_work_item_form
            )
    else:
        assert case.status == Case.STATUS_COMPLETED


@pytest.mark.parametrize(
    "decision,expected_work_item_task",
    [
        (
            "define-amount",
            "decision-and-credit",
        ),
        (
            "additional-data",
            None,
        ),
    ],
)
def test_dynamic_task_redo_define_amount(
    db,
    caluma_data,
    user,
    case_access_event_mock,
    circulation,
    answer_factory,
    form_factory,
    decision,
    expected_work_item_task,
    send_mail_mock,
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

    if expected_work_item_task:
        redo_work_item(case.work_items.get(task_id="decision-and-credit"), user)

        assert case.status == Case.STATUS_RUNNING
        assert case.work_items.filter(
            task_id=expected_work_item_task, status=WorkItem.STATUS_READY
        ).exists()
    else:
        with pytest.raises(ValidationError):
            redo_work_item(case.work_items.get(task_id="decision-and-credit"), user)
