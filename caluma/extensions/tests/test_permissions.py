from collections import namedtuple

import pytest

from caluma.caluma_core.mutation import Mutation
from caluma.caluma_form.schema import SaveDocumentAnswer
from caluma.caluma_workflow.schema import SaveCase
from caluma.extensions.permissions import MySAGWPermission

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
    "groups,created_by_user,assigned_users,has_perm,has_obj_perm",
    [
        (["admin"], "bar", ["admin"], True, True),
        (["sagw"], "bar", ["admin"], True, True),
        (["foo"], "bar", [], False, False),
        (["foo"], "baz", [], False, True),
    ],
)
def test_permission_for_save_document_answer(
    db,
    admin_info,
    answer,
    work_item,
    groups,
    created_by_user,
    assigned_users,
    has_perm,
    has_obj_perm,
):
    admin_info.context.user.groups = groups
    admin_info.context.user.username = "baz"

    answer.document.created_by_user = created_by_user
    answer.document.save()

    answer.document.case.parent_work_item = work_item
    answer.document.case.save()

    work_item.assigned_users = assigned_users
    work_item.save()

    perm = MySAGWPermission()

    mutation = SaveDocumentAnswer
    assert perm.has_permission(mutation, admin_info) is has_perm
    assert perm.has_object_permission(mutation, admin_info, answer) is has_obj_perm


@pytest.mark.parametrize(
    "groups,created_by_user,has_perm,has_obj_perm",
    [
        (["admin"], "bar", True, True),
        (["sagw"], "bar", True, True),
        (["foo"], "bar", True, True),
        (["foo"], "baz", True, True),
    ],
)
def test_permission_for_save_case(
    db, admin_info, answer, groups, created_by_user, has_perm, has_obj_perm
):
    admin_info.context.user.groups = groups
    admin_info.context.user.username = "baz"

    answer.document.created_by_user = created_by_user
    answer.document.save()

    perm = MySAGWPermission()

    mutation = SaveCase
    assert perm.has_permission(mutation, admin_info) is has_perm
    assert perm.has_object_permission(mutation, admin_info, answer) is has_obj_perm
