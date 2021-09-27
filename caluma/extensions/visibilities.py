from django.db.models import Q

from caluma.caluma_core.types import Node
from caluma.caluma_core.visibilities import BaseVisibility, Union, filter_queryset_for
from caluma.caluma_form import models as form_models
from caluma.caluma_form.schema import Answer, Document, Form, Option, Question
from caluma.caluma_workflow.schema import Case, Flow, Task, Workflow, WorkItem
from caluma.extensions.common import get_cases_for_user
from caluma.extensions.settings import settings


class StaffVisibility(BaseVisibility):
    @filter_queryset_for(Node)
    def filter_queryset_for_all(self, node, queryset, info):
        user = info.context.user
        if "sagw" in user.groups or "admin" in user.groups:
            return queryset

        return queryset.none()


class CreateOrAssignVisibility(BaseVisibility):
    @filter_queryset_for(Node)
    def filter_queryset_for_all(self, node, queryset, info):  # pragma: no cover
        user = info.context.user
        return queryset.filter(created_by_user=user.username)

    @filter_queryset_for(Answer)
    def filter_queryset_for_answer(self, node, queryset, info):
        return queryset.filter(
            document__in=self.filter_queryset_for_document(
                None, form_models.Document.objects, info
            )
        )

    @filter_queryset_for(Document)
    def filter_queryset_for_document(self, node, queryset, info):
        user = info.context.user
        case_ids = get_cases_for_user(user)
        return queryset.filter(
            Q(work_item__task__slug__in=settings.APPLICANT_TASK_SLUGS)
            | (Q(work_item__isnull=True) & Q(case__workflow__pk="document-review")),
            Q(case__pk__in=case_ids) | Q(work_item__case__pk__in=case_ids),
        )

    @filter_queryset_for(WorkItem)
    def filter_queryset_for_workitem(self, node, queryset, info):
        user = info.context.user
        case_ids = get_cases_for_user(user)
        return queryset.filter(
            case__pk__in=case_ids, task__slug__in=settings.APPLICANT_TASK_SLUGS
        )

    @filter_queryset_for(Case)
    def filter_queryset_for_case(self, node, queryset, info):
        user = info.context.user
        case_ids = get_cases_for_user(user)
        return queryset.filter(pk__in=case_ids)

    @filter_queryset_for(Task)
    @filter_queryset_for(Flow)
    @filter_queryset_for(Workflow)
    @filter_queryset_for(Form)
    @filter_queryset_for(Option)
    @filter_queryset_for(Question)
    def filter_queryset_for_blueprints(self, node, queryset, info):
        return queryset


class MySAGWVisibility(Union):
    visibility_classes = [StaffVisibility, CreateOrAssignVisibility]
