from caluma.caluma_core.mutation import Mutation
from caluma.caluma_core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from caluma.caluma_form.schema import SaveDocumentAnswer
from caluma.caluma_workflow.schema import SaveCase


class MySAGWPermission(BasePermission):
    def _is_admin_or_sagw(self, info):
        groups = info.context.user.groups
        return "admin" in groups or "sagw" in groups

    def _is_own(self, info, instance):
        return instance.created_by_user == info.context.user.username

    @permission_for(Mutation)
    @object_permission_for(Mutation)
    def has_permission_fallback(self, mutation, info, instance=None):
        return self._is_admin_or_sagw(info) or (
            bool(instance) and self._is_own(info, instance)
        )

    @permission_for(SaveCase)
    @object_permission_for(SaveCase)
    def has_permission_for_save_case(self, mutation, info, case=None):
        return True

    @permission_for(SaveDocumentAnswer)
    @object_permission_for(SaveDocumentAnswer)
    def has_permission_for_save_document_answer(self, mutation, info, answer=None):
        return self._is_admin_or_sagw(info) or (
            bool(answer) and self._is_own(info, answer.document)
        )
