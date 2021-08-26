from caluma.caluma_core.mutation import Mutation
from caluma.caluma_core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from caluma.caluma_form.models import Document
from caluma.caluma_form.schema import SaveDocumentAnswer
from caluma.caluma_workflow.schema import CompleteWorkItem, SaveCase, StartCase


class MySAGWPermission(BasePermission):
    def _is_admin_or_sagw(self, info):
        groups = info.context.user.groups
        return "admin" in groups or "sagw" in groups

    def _is_own(self, info, instance):
        return instance.created_by_user == info.context.user.username

    def _is_assigned(self, info, instance):
        return info.context.user.username in instance.assigned_users

    @permission_for(Mutation)
    @object_permission_for(Mutation)
    def has_permission_fallback(self, mutation, info, instance=None):
        return self._is_admin_or_sagw(info) or (
            bool(instance) and self._is_own(info, instance)
        )

    @permission_for(SaveCase)
    @object_permission_for(SaveCase)
    @permission_for(StartCase)
    @object_permission_for(StartCase)
    def has_permission_for_save_case(self, mutation, info, case=None):
        return True

    @permission_for(SaveDocumentAnswer)
    @object_permission_for(SaveDocumentAnswer)
    def has_permission_for_save_document_answer(self, mutation, info, answer=None):
        document = Document.objects.get(
            pk=mutation.get_params(info)["input"]["document"]
        )
        return (
            self._is_admin_or_sagw(info)
            or self._is_own(info, document)
            or (self._is_assigned(info, document.work_item))
            or (
                hasattr(document.case, "parent_work_item")
                and self._is_assigned(info, document.case.parent_work_item)
            )
        )

    @permission_for(CompleteWorkItem)
    def has_permission_for_complete_work_item(self, mutation, info):
        return True

    @object_permission_for(CompleteWorkItem)
    def has_object_permission_for_complete_work_item(self, mutation, info, work_item):
        return self._is_admin_or_sagw(info) or self._is_assigned(info, work_item)
