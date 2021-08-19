from pathlib import Path

import pytest
from django.core.management import call_command

from caluma.caluma_form.models import Form
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import skip_work_item, start_case
from caluma.caluma_workflow.models import Workflow

from .settings import settings


@pytest.fixture
def caluma_data(db):
    call_command("loaddata", Path.cwd() / "caluma" / "data" / "form-config.json")
    call_command("loaddata", Path.cwd() / "caluma" / "data" / "workflow-config.json")


@pytest.fixture
def user():
    return BaseUser(username="name", claims={"sub": "test"}, token=b"eyToken")


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


@pytest.fixture
def identites_mock_for_mailing(requests_mock):
    data = {
        "data": [
            {
                "type": "identities",
                "id": "4d70c3f9-1e69-4e82-9010-1a28d12b1e58",
                "attributes": {
                    "email": "test@example.com",
                    "first-name": "Winston",
                    "last-name": "Smith",
                    "language": "en",
                },
                "relationships": {
                    "interests": {"meta": {"count": 0}, "data": []},
                    "additional-emails": {"meta": {"count": 0}, "data": []},
                    "phone-numbers": {"meta": {"count": 0}, "data": []},
                    "addresses": {"meta": {"count": 0}, "data": []},
                },
            }
        ]
    }

    return requests_mock.get(f"{settings.API_BASE_URI}/identities", json=data)
