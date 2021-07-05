from caluma.caluma_form.models import Form
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import skip_work_item, start_case
from caluma.caluma_workflow.models import Workflow


def test_work_item_set_assigned_user(db, caluma_data):
    case = start_case(
        workflow=Workflow.objects.get(pk="document-review"),
        form=Form.objects.get(pk="circulation-form"),
        user=BaseUser(username="name", claims={"sub": "test"}),
    )

    assert case.work_items.get(task_id="submit-document").assigned_users == ["test"]


def test_work_item_create_circulation(db, caluma_data):
    user = BaseUser(username="name", claims={"sub": "test"})
    case = start_case(
        workflow=Workflow.objects.get(pk="document-review"),
        form=Form.objects.get(pk="circulation-form"),
        user=user,
    )

    skip_work_item(case.work_items.get(task_id="submit-document"), user)

    case.work_items.get(task_id="review-document").document.answers.create(
        question_id="review-document-decision",
        value="review-document-decision-continue",
    )

    skip_work_item(case.work_items.get(task_id="review-document"), user)

    assert (
        case.work_items.get(task_id="circulation").child_case.workflow_id
        == "circulation"
    )
