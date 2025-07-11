from django.db.models import F, Q

from caluma.caluma_analytics.schema import (
    AnalyticsCell,
    AnalyticsField,
    AnalyticsOutput,
    AnalyticsRow,
    AnalyticsTable,
    AnalyticsTableContent,
    AvailableField,
)
from caluma.caluma_core.types import Node
from caluma.caluma_core.visibilities import BaseVisibility, Union, filter_queryset_for
from caluma.caluma_form import models as form_models
from caluma.caluma_form.schema import Answer, Document, Form, Option, Question
from caluma.caluma_workflow.schema import Case, Flow, Task, Workflow, WorkItem
from caluma.extensions.common import (
    get_cases_for_user,
    get_cases_for_user_by_access,
    get_cases_for_user_by_circulation_invite,
)
from caluma.extensions.settings import settings


class StaffVisibility(BaseVisibility):
    @filter_queryset_for(Node)
    def filter_queryset_for_all(self, node, queryset, info):
        user = info.context.user
        if "sagw" in user.groups or "admin" in user.groups:
            return queryset

        return queryset.none()


class CreateOrAssignVisibility(BaseVisibility):
    def _is_admin_or_sagw(self, info):
        groups = info.context.user.groups
        return "admin" in groups or "sagw" in groups

    @filter_queryset_for(Node)
    def filter_queryset_for_all(self, node, queryset, info):  # pragma: no cover
        user = info.context.user
        return queryset.filter(created_by_user=user.username)

    @filter_queryset_for(Answer)
    def filter_queryset_for_answer(self, node, queryset, info):
        if self._is_admin_or_sagw(info):
            return queryset

        case_ids_circulation = get_cases_for_user_by_circulation_invite(
            info.context.user,
        )
        return queryset.filter(
            Q(
                document__family__in=self.filter_queryset_for_document(
                    None, form_models.Document.objects, info, []
                ),
            )
            | (
                Q(
                    question__slug__in=[
                        question
                        for sublist in settings.REVISION_QUESTIONS.values()
                        for question in sublist
                    ],
                )
                & (
                    Q(
                        document__family__in=self.filter_queryset_for_document(
                            None,
                            form_models.Document.objects,
                            info,
                            list(settings.REVISION_QUESTIONS.keys()),
                        ),
                    )
                    | (
                        Q(document__family__case__family_id__in=case_ids_circulation)
                        | Q(
                            document__work_item__case__family_id__in=case_ids_circulation,
                        )
                    )
                )
            ),
        )

    @filter_queryset_for(Document)
    def filter_queryset_for_document(
        self,
        node,
        queryset,
        info,
        tasks=settings.APPLICANT_VISIBLE_TASKS,
    ):
        if self._is_admin_or_sagw(info):
            return queryset

        user = info.context.user
        case_ids_access = get_cases_for_user_by_access(user)
        case_ids_circulation = get_cases_for_user_by_circulation_invite(user)
        case_ids_circulation = list(
            filter(lambda i: i not in case_ids_access, case_ids_circulation),
        )

        work_item_case_access = Q(family__work_item__task__slug__in=tasks) | (
            Q(family__work_item__isnull=True)
            & Q(family__case__workflow__pk="document-review")
        )

        access_to_case_by_access = (
            Q(family__case__family_id__in=case_ids_access)
            | Q(family__work_item__case__family_id__in=case_ids_access)
            | Q(created_by_user=user.username)
        )

        work_item_case_circulation_invite = (
            Q(family__case__workflow__pk="document-review")
            | Q(work_item__assigned_users__contains=[user.username])
        ) & (
            Q(family__case__family_id__in=case_ids_circulation)
            | Q(work_item__case__family_id__in=case_ids_circulation)
            | Q(work_item__case_id__in=case_ids_circulation)
        )

        floating_row_document = (
            Q(pk=F("family_id"))
            & Q(form__is_published=False)
            & Q(family__case__isnull=True)
            & Q(family__work_item__isnull=True)
            & Q(created_by_user=user.username)
        )

        row_document_on_applicant_form = Q(family__form__is_published=True) | Q(
            family__work_item__task__slug__in=settings.APPLICANT_TASK_SLUGS,
        )
        return queryset.filter(
            Q(work_item_case_access & access_to_case_by_access)
            | work_item_case_circulation_invite
            | floating_row_document
            | Q(row_document_on_applicant_form & access_to_case_by_access),
        )

    @filter_queryset_for(WorkItem)
    def filter_queryset_for_workitem(self, node, queryset, info):
        if self._is_admin_or_sagw(info):
            return queryset

        user = info.context.user
        case_ids = get_cases_for_user(user)

        return queryset.filter(
            (
                (
                    Q(case__family_id__in=case_ids)
                    | Q(case__created_by_user=user.username)
                )
                & (
                    Q(
                        task__slug__in=[
                            *settings.APPLICANT_TASK_SLUGS,
                            # REVISION workitems must be accessible in order to display the
                            # remarks
                            *list(settings.REVISION_QUESTIONS.keys()),
                            # circulation must be accessible for NWP
                            "circulation",
                        ],
                    )
                    | Q(assigned_users__contains=[user.username])
                )
            ),
        )

    @filter_queryset_for(Case)
    def filter_queryset_for_case(self, node, queryset, info):
        if self._is_admin_or_sagw(info):
            return queryset

        user = info.context.user
        case_ids = get_cases_for_user(user)
        return queryset.filter(Q(pk__in=case_ids) | Q(created_by_user=user.username))

    @filter_queryset_for(Task)
    @filter_queryset_for(Flow)
    @filter_queryset_for(Workflow)
    @filter_queryset_for(Form)
    @filter_queryset_for(Option)
    @filter_queryset_for(Question)
    def filter_queryset_for_blueprints(self, node, queryset, info):
        return queryset

    @filter_queryset_for(AnalyticsCell)
    @filter_queryset_for(AnalyticsField)
    @filter_queryset_for(AnalyticsOutput)
    @filter_queryset_for(AnalyticsRow)
    @filter_queryset_for(AnalyticsTable)
    @filter_queryset_for(AnalyticsTableContent)
    @filter_queryset_for(AvailableField)
    def filter_queryset_for_analytics(self, node, queryset, info):
        return queryset.none()


class MySAGWVisibility(Union):
    visibility_classes = [StaffVisibility, CreateOrAssignVisibility]
