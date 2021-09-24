import datetime
from pathlib import Path

import pytest
from django.core.management import call_command

from caluma.caluma_form.models import Answer, Form
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import skip_work_item, start_case
from caluma.caluma_workflow.models import Workflow

from . import api_client
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
    case = start_case(
        workflow=Workflow.objects.get(pk="document-review"),
        form=Form.objects.get(pk="circulation-form"),
        user=user,
    )

    Answer.objects.create(
        question_id="circulation-decision",
        document=case.document,
        value="circulation-decision-approved",
    )

    return case


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
def identities_mock(requests_mock):
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


@pytest.fixture
def get_token_mock(mocker):
    data = {
        "access_token": "eyToken",
        "expires_in": 300,
        "refresh_expires_in": 0,
        "token_type": "Bearer",
        "not-before-policy": 0,
        "scope": ["profile", "email"],
        "expires_at": 1632468505.0576448,
        "expires_at_dt": datetime.datetime(2021, 9, 24, 7, 28, 25),
    }

    return mocker.patch.object(
        api_client.OAuth2Session,
        "fetch_token",
        return_value=data,
    )


@pytest.fixture
def case_access_create_request_mock(requests_mock):
    data = {
        "data": {
            "type": "case-accesses",
            "id": "ee6f5d24-b351-4b44-9d55-7dbd2c19d16a",
            "attributes": {
                "case-id": "97d001cf-8d07-4733-aa17-542ed83e8582",
                "email": None,
            },
            "relationships": {
                "identity": {
                    "data": {
                        "type": "identities",
                        "id": "d7b118a7-ce53-48b7-9b05-be148f154f14",
                    }
                }
            },
        }
    }

    return requests_mock.post(f"{settings.API_BASE_URI}/case/accesses", json=data)


@pytest.fixture
def case_access_event_mock(
    identities_mock, get_token_mock, case_access_create_request_mock
):
    pass
