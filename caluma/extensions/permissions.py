from caluma.caluma_core.mutation import Mutation
from caluma.caluma_core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from caluma.caluma_form.models import Document
from caluma.caluma_form.schema import SaveDocument, SaveDocumentAnswer
from caluma.caluma_workflow.schema import CompleteWorkItem, SaveCase
from caluma.extensions.common import get_cases_for_user
from caluma.extensions.settings import settings


class MySAGWPermission(BasePermission):
    def _is_admin_or_sagw(self, info):
        groups = info.context.user.groups
        return "admin" in groups or "sagw" in groups

    def _can_access_case(self, info, case):
        case_ids = get_cases_for_user(info.context.user)
        return str(case.pk) in case_ids

    def _is_own(self, info, instance):
        return instance.created_by_user == info.context.user.username

    @permission_for(Mutation)
    @object_permission_for(Mutation)
    def has_permission_fallback(self, mutation, info, instance=None):
        return self._is_admin_or_sagw(info) or (
            bool(instance) and self._is_own(info, instance)
        )

    def _get_case_for_doc(self, document):
        """
        Get case from document.

        Check for case at these locations in this order:
        1. case on the document
        2. case on the document.work_item
        3. case on the document.family
        4. case on the document.family.work_item
        """

        def case_lookup(obj, *lookups):
            for lookup in lookups:
                obj = getattr(obj, lookup, None)
            return obj

        case_lookups = [
            (document, "case"),
            (document, "work_item", "case"),
            (document.family, "case"),
            (document.family, "work_item", "case"),
        ]

        for lookup_path in case_lookups:
            case = case_lookup(*lookup_path)
            if case:
                return case.family

    @permission_for(SaveCase)
    @object_permission_for(SaveCase)
    @permission_for(SaveDocument)
    @object_permission_for(SaveDocument)
    def has_permission_for_save_case_save_document(self, mutation, info, obj=None):
        return True

    @permission_for(SaveDocumentAnswer)
    @object_permission_for(SaveDocumentAnswer)
    def has_permission_for_save_document_answer(self, mutation, info, answer=None):
        document = Document.objects.get(
            pk=mutation.get_params(info)["input"]["document"]
        )
        case = self._get_case_for_doc(document)
        work_item_query = case.work_items.filter(
            status="ready", task__slug__in=settings.APPLICANT_TASK_SLUGS
        )

        return self._is_admin_or_sagw(info) or (
            (self._can_access_case(info, case) or self._is_own(info, document))
            and (
                work_item_query.exists()
                or (
                    hasattr(document, "work_item")
                    and document.work_item.task.slug == "additional-data-form"
                    and work_item_query.filter(task__slug="additonal-data").exists()
                )
            )
        )

    @permission_for(CompleteWorkItem)
    def has_permission_for_complete_work_item(self, mutation, info):
        return True

    @object_permission_for(CompleteWorkItem)
    def has_object_permission_for_complete_work_item(self, mutation, info, work_item):
        return self._is_admin_or_sagw(info) or (
            (
                self._can_access_case(info, work_item.case)
                or self._is_own(info, work_item)
            )
            and work_item.task.slug in settings.APPLICANT_TASK_SLUGS
        )
