from pathlib import Path

import pytest
from django.core.management import call_command

from caluma.caluma_form.models import Form
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import skip_work_item, start_case
from caluma.caluma_workflow.models import Workflow


@pytest.fixture
def caluma_data(db):
    call_command("loaddata", Path.cwd() / "caluma" / "data" / "form-config.json")
    call_command("loaddata", Path.cwd() / "caluma" / "data" / "workflow-config.json")


@pytest.fixture
def user(db):
    return BaseUser(username="name", claims={"sub": "test"})


@pytest.fixture
def document_review_case(db, user):
    return start_case(
        workflow=Workflow.objects.get(pk="document-review"),
        form=Form.objects.get(pk="circulation-form"),
        user=user,
    )


@pytest.fixture
def circulation(db, document_review_case, user):
    case = document_review_case
    skip_work_item(case.work_items.get(task_id="submit-document"), user)

    case.work_items.get(task_id="review-document").document.answers.create(
        question_id="review-document-decision",
        value="review-document-decision-continue",
    )

    skip_work_item(case.work_items.get(task_id="review-document"), user)

    return case.work_items.get(task_id="circulation").child_case
