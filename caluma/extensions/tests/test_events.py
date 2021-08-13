from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import WorkItem


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
