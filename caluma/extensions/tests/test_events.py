import pytest
from django.utils import timezone

from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import complete_work_item, start_case
from caluma.caluma_workflow.models import Workflow, WorkItem


def test_work_item_set_assigned_user(db, caluma_data, document_review_case):
    assert document_review_case.work_items.get(
        task_id="submit-document"
    ).assigned_users == ["test"]


def test_work_item_create_circulation(db, caluma_data, circulation):
    assert circulation.workflow_id == "circulation"


def test_work_item_finish_circulation(db, caluma_data, user, circulation):
    complete_work_item(circulation.work_items.get(task_id="finish-circulation"), user)

    assert (
        circulation.work_items.get(task_id="invite-to-circulation").status
        == WorkItem.STATUS_CANCELED
    )


def test_work_item_invite_to_circulation(db, caluma_data, user, circulation):
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


def test_case_complete_circulation(db, caluma_data, user, circulation):
    complete_work_item(circulation.work_items.get(task_id="finish-circulation"), user)

    assert circulation.parent_work_item.status == WorkItem.STATUS_COMPLETED


@pytest.mark.parametrize(
    "same_year,first", [(True, False), (False, False), (False, True)]
)
def test_case_number(
    db, caluma_data, user, form_question_factory, answer_factory, same_year, first
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
