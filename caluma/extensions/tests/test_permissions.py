from collections import namedtuple
from uuid import uuid4

import pytest

from caluma.caluma_core.mutation import Mutation
from caluma.caluma_form.schema import SaveDocumentAnswer
from caluma.caluma_workflow.models import Task, Workflow
from caluma.caluma_workflow.schema import CancelCase, CompleteWorkItem, SaveCase
from caluma.extensions.permissions import MySAGWPermission
from caluma.extensions.settings import settings

_Fallbackobj = namedtuple("Fallbackobj", ["created_by_user"])


@pytest.mark.parametrize(
    "groups,created_by_user,has_perm,has_obj_perm",
    [
        (["admin"], "bar", True, True),
        (["sagw"], "bar", True, True),
        (["foo"], "bar", False, False),
        (["foo"], "baz", False, True),
    ],
)
def test_permissions_fallback(
    mocker, admin_info, groups, created_by_user, has_perm, has_obj_perm
):
    admin_info.context.user.groups = groups
    admin_info.context.user.username = "baz"

    fallback_obj = _Fallbackobj(created_by_user=created_by_user)

    perm = MySAGWPermission()

    mutation = mocker.Mock()
    mutation.__name__ = "SomeMutation"
    mutation.mro.return_value = [Mutation]
    assert perm.has_permission(mutation, admin_info) is has_perm
    assert (
        perm.has_object_permission(mutation, admin_info, fallback_obj) is has_obj_perm
    )


@pytest.mark.parametrize(
    "groups,task_slug,has_perm,has_obj_perm",
    [
        (["admin"], "bar", True, True),
        (["sagw"], "bar", True, True),
        (["foo"], "bar", True, False),
        (["foo"], settings.APPLICANT_TASK_SLUGS[0], True, True),
    ],
)
def test_permission_for_save_document_answer(
    db,
    admin_info,
    answer,
    work_item_factory,
    groups,
    task_slug,
    has_perm,
    has_obj_perm,
    mocker,
    case_access_request_mock,
):
    work_item = work_item_factory(
        task__slug=task_slug, case__pk="994b72cc-6556-46e5-baf9-228457fa309f"
    )

    admin_info.context.user.groups = groups

    work_item.case.document = answer.document
    work_item.case.save()

    mocker.patch.object(
        Mutation,
        "get_params",
        return_value={"input": {"document": str(answer.document.pk)}},
    )

    perm = MySAGWPermission()

    mutation = SaveDocumentAnswer
    assert perm.has_permission(mutation, admin_info) is has_perm
    assert perm.has_object_permission(mutation, admin_info, answer) is has_obj_perm


def test_permission_for_save_document_answer_floating_row_document(
    db,
    admin_info,
    answer,
    document,
    mocker,
    case_access_request_mock,
):
    admin_info.context.user.groups = ["test"]
    document.created_by_user = admin_info.context.user.username = "test"
    document.save()

    mocker.patch.object(
        Mutation,
        "get_params",
        return_value={"input": {"document": str(document.pk)}},
    )

    perm = MySAGWPermission()

    mutation = SaveDocumentAnswer
    assert perm.has_permission(mutation, admin_info) is True
    assert perm.has_object_permission(mutation, admin_info, answer) is True


@pytest.mark.parametrize(
    "groups,created_by_user,has_perm,has_obj_perm",
    [
        (["admin"], "bar", True, True),
        (["sagw"], "bar", True, True),
        (["foo"], "bar", True, True),
        (["foo"], "baz", True, True),
    ],
)
def test_permission_for_save_case_and_start_case(
    db, admin_info, answer, groups, created_by_user, has_perm, has_obj_perm
):
    admin_info.context.user.groups = groups
    admin_info.context.user.username = "baz"

    answer.document.created_by_user = created_by_user
    answer.document.save()

    perm = MySAGWPermission()

    assert perm.has_permission(SaveCase, admin_info) is has_perm
    assert perm.has_object_permission(SaveCase, admin_info, answer) is has_obj_perm


@pytest.mark.parametrize(
    "groups,task_slug,has_perm,has_obj_perm",
    [
        (["admin"], "bar", True, True),
        (["sagw"], "bar", True, True),
        (["foo"], "bar", True, False),
        (["foo"], settings.APPLICANT_TASK_SLUGS[0], True, True),
    ],
)
def test_permission_for_complete_work_item(
    db,
    admin_info,
    work_item_factory,
    groups,
    task_slug,
    has_perm,
    has_obj_perm,
    case_access_request_mock,
):
    work_item = work_item_factory(
        task__slug=task_slug, case__pk="994b72cc-6556-46e5-baf9-228457fa309f"
    )

    admin_info.context.user.groups = groups

    perm = MySAGWPermission()

    mutation = CompleteWorkItem
    assert perm.has_permission(mutation, admin_info) is has_perm
    assert perm.has_object_permission(mutation, admin_info, work_item) is has_obj_perm


@pytest.mark.parametrize(
    "groups,task_slug,has_case_access,has_perm,has_obj_perm",
    [
        (["admin"], "bar", True, True, False),
        (["admin"], settings.APPLICANT_TASK_SLUGS[0], True, True, True),
        (["sagw"], "bar", True, True, False),
        (["sagw"], settings.APPLICANT_TASK_SLUGS[0], True, True, True),
        (["foo"], "bar", True, True, False),
        (["foo"], settings.APPLICANT_TASK_SLUGS[0], True, True, True),
        (["foo"], settings.APPLICANT_TASK_SLUGS[0], False, True, False),
    ],
)
def test_permission_for_cancel_case(
    db,
    admin_info,
    work_item_factory,
    groups,
    task_slug,
    has_case_access,
    has_perm,
    has_obj_perm,
    caluma_data,
    case_access_create_request_mock,
    identities_mock,
    get_token_mock,
    case_access_request_mock,
):
    case_pk = (
        "994b72cc-6556-46e5-baf9-228457fa309f" if has_case_access else str(uuid4())
    )
    task = Task.objects.filter(pk=task_slug).first()
    work_item = work_item_factory(
        case__pk=case_pk,
        case__workflow=Workflow.objects.get(pk="document-review"),
    )
    if task:
        work_item.task = task
        work_item.save()

    admin_info.context.user.groups = groups

    perm = MySAGWPermission()

    mutation = CancelCase
    assert perm.has_permission(mutation, admin_info) is has_perm
    assert (
        perm.has_object_permission(mutation, admin_info, work_item.case) is has_obj_perm
    )
