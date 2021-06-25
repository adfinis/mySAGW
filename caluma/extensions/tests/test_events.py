from caluma.caluma_form.models import Form
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import start_case
from caluma.caluma_workflow.models import Workflow


def test_work_item(db, caluma_data):
    case = start_case(
        workflow=Workflow.objects.get(pk="document-review"),
        form=Form.objects.get(pk="circulation-form"),
        user=BaseUser(username="name", claims={"sub": "test"}),
    )

    assert case.work_items.get(task_id="submit-document").assigned_users == ["test"]
