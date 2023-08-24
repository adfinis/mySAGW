from caluma.caluma_analytics.schema import (
    RemoveAnalyticsField,
    RemoveAnalyticsTable,
    SaveAnalyticsField,
    SaveAnalyticsTable,
)
from caluma.caluma_core.mutation import Mutation
from caluma.caluma_core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)
from caluma.caluma_form.schema import SaveDocument, SaveDocumentAnswer
from caluma.caluma_workflow.schema import (
    CancelCase,
    CompleteWorkItem,
    RedoWorkItem,
    ReopenCase,
    SaveCase,
)
from caluma.extensions.common import (
    get_cases_for_user,
    get_cases_for_user_by_circulation_invite,
)
from caluma.extensions.settings import settings


class MySAGWPermission(BasePermission):
    def _is_admin(self, info):
        groups = info.context.user.groups
        return "admin" in groups

    def _is_sagw(self, info):
        groups = info.context.user.groups
        return "sagw" in groups

    def _is_admin_or_sagw(self, info):
        return self._is_admin(info) or self._is_sagw(info)

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
    @permission_for(SaveDocumentAnswer)
    def has_permission_for_save_case_save_document(self, mutation, info, obj=None):
        return True

    @object_permission_for(SaveDocumentAnswer)
    def has_permission_for_save_document_answer(self, mutation, info, answer):
        if (
            not answer.document.family.form.is_published
            and not getattr(answer.document.family, "case", False)
            and not getattr(answer.document.family, "work_item", False)
            and self._is_own(info, answer.document.family)
        ):
            # is floating row-document
            return True

        case = self._get_case_for_doc(answer.document)

        if self._is_admin(info):
            return True
        if self._is_sagw(info):
            work_item = (
                answer.document.family.work_item
                if hasattr(answer.document.family, "work_item")
                else case.work_items.filter(status="ready")
                .exclude(task__slug__in=settings.APPLICANT_TASK_SLUGS)
                .first()
            )
            if work_item or self._can_access_case(info, case):
                return True

        if not (
            self._can_access_case(info, case)
            or self._is_own(info, answer.document.family)
        ):
            return False

        work_item = (
            answer.document.family.work_item
            if hasattr(answer.document.family, "work_item")
            else case.work_items.filter(
                task__slug__in=["submit-document", "revise-document"],
                status="ready",
            ).first()
        )

        return work_item is not None and work_item.status == "ready"

    @permission_for(CompleteWorkItem)
    @permission_for(CancelCase)
    def has_permission_for_complete_work_item(self, mutation, info):
        return True

    @object_permission_for(CompleteWorkItem)
    def has_object_permission_for_complete_work_item(self, mutation, info, work_item):
        return (
            self._is_admin_or_sagw(info)
            or (
                (
                    self._can_access_case(info, work_item.case)
                    or self._is_own(info, work_item)
                )
                and work_item.task.slug in settings.APPLICANT_TASK_SLUGS
            )
            or (
                str(work_item.case.pk)
                in get_cases_for_user_by_circulation_invite(info.context.user)
                and work_item.task.slug in settings.CIRCULATION_TASK_SLUGS
            )
        )

    @object_permission_for(CancelCase)
    def has_permission_for_cancel_case(self, mutation, info, case):
        return self._is_admin_or_sagw(info) or (
            (self._can_access_case(info, case) or self._is_own(info, case))
            and case.work_items.filter(
                status="ready",
                task__slug="submit-document",
            ).exists()
        )

    @permission_for(RedoWorkItem)
    @object_permission_for(RedoWorkItem)
    @permission_for(ReopenCase)
    @object_permission_for(ReopenCase)
    def has_permission_for_redo_workitem_reopen_case(
        self,
        mutation,
        info,
        instance=None,
    ):
        return self._is_admin_or_sagw(info)

    @permission_for(RemoveAnalyticsField)
    @object_permission_for(RemoveAnalyticsField)
    @permission_for(RemoveAnalyticsTable)
    @object_permission_for(RemoveAnalyticsTable)
    @permission_for(SaveAnalyticsField)
    @object_permission_for(SaveAnalyticsField)
    @permission_for(SaveAnalyticsTable)
    @object_permission_for(SaveAnalyticsTable)
    def has_permission_for_analytics(self, mutation, info, _=None):
        return self._is_admin_or_sagw(info)
