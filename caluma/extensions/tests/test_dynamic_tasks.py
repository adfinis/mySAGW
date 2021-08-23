import pytest

from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import Case


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
    document_review_case,
    identites_mock_for_mailing,
    decision,
    expected_case_status,
    expected_work_item,
):
    case = document_review_case

    skip_work_item(case.work_items.get(task_id="submit-document"), user)

    case.work_items.get(task_id="review-document").document.answers.create(
        question_id="review-document-decision",
        value=f"review-document-decision-{decision}",
    )

    skip_work_item(case.work_items.get(task_id="review-document"), user)

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
        ("complete", Case.STATUS_RUNNING, "complete-document"),
    ],
)
def test_dynamic_task_after_decision_and_credit(
    db,
    caluma_data,
    user,
    circulation,
    identites_mock_for_mailing,
    decision,
    expected_case_status,
    expected_work_item,
):
    case = circulation.parent_work_item.case

    skip_work_item(case.work_items.get(task_id="circulation"), user)

    case.work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value=f"decision-and-credit-decision-{decision}",
    )

    skip_work_item(case.work_items.get(task_id="decision-and-credit"), user)

    case.refresh_from_db()

    assert case.status == expected_case_status

    if case.status == Case.STATUS_RUNNING:
        assert case.work_items.filter(task_id=expected_work_item).exists()


@pytest.mark.parametrize(
    "decision,expected_work_item",
    [
        (False, "complete-document"),
        (True, "additional-data"),
    ],
)
def test_dynamic_task_after_define_amount(
    db,
    caluma_data,
    user,
    circulation,
    identites_mock_for_mailing,
    decision,
    expected_work_item,
):
    case = circulation.parent_work_item.case

    skip_work_item(case.work_items.get(task_id="circulation"), user)

    case.work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value="decision-and-credit-decision-define-amount",
    )

    if decision:
        case.work_items.get(task_id="decision-and-credit").document.answers.create(
            question_id="decision-and-credit-advance-credit",
            value="decision-and-credit-advance-credit-approved",
        )

    skip_work_item(case.work_items.get(task_id="decision-and-credit"), user)
    skip_work_item(case.work_items.get(task_id="define-amount"), user)

    case.refresh_from_db()

    assert case.status == Case.STATUS_RUNNING
    assert case.work_items.filter(task_id=expected_work_item).exists()
