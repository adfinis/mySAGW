import pytest

from caluma.caluma_analytics import (
    models as analytics_models,
    schema as analytics_schema,
)
from caluma.caluma_form import models as form_models, schema as form_schema
from caluma.caluma_user.models import OIDCUser
from caluma.caluma_workflow import models as workflow_models, schema as workflow_schema
from caluma.caluma_workflow.api import complete_work_item
from caluma.extensions.settings import settings
from caluma.extensions.visibilities import MySAGWVisibility


@pytest.mark.parametrize(
    "user_name,visibility_map",
    [
        (
            "admin",
            {
                "Form": 8,
                "WorkItem": 16,
                "Document": 10,
                "Case": 6,
                "Question": 22,
                "Answer": 7,
                "AnalyticsTable": 1,
            },
        ),
        (
            "test",
            {
                "Form": 8,
                "WorkItem": 6,
                "Document": 3,
                "Case": 3,
                "Question": 22,
                "Answer": 4,
                "AnalyticsTable": 0,
            },
        ),
    ],
)
def test_visibilities_default(
    db,
    caluma_data,
    case_access_event_mock,
    create_document_review_case,
    admin_info,
    admin_user,
    requests_mock,
    analytics_table,
    user_name,
    visibility_map,
    work_item_factory,
    snapshot,
):
    admin_info.context.user.username = user_name
    admin_info.context.user.groups = [user_name]
    admin_info.context.user.group = user_name

    admin_user = OIDCUser(
        b"sometoken", {"sub": "admin", settings.OIDC_GROUPS_CLAIM: ["admin"]}
    )
    user = OIDCUser(
        b"sometoken", {"sub": user_name, settings.OIDC_GROUPS_CLAIM: [user_name]}
    )

    def prepare_case(case_identifier):
        case = create_document_review_case()
        case.meta = {"identifier": case_identifier}
        case.save()
        complete_work_item(case.work_items.get(task_id="submit-document"), admin_user)
        case.work_items.get(task_id="review-document").document.answers.create(
            question_id="review-document-decision",
            value="review-document-decision-continue",
        )
        complete_work_item(case.work_items.get(task_id="review-document"), admin_user)
        return case

    # case_1 with access
    case_1 = prepare_case("access")
    data = {"data": [{"attributes": {"case-id": str(case_1.pk)}}]}
    requests_mock.get(f"{settings.API_BASE_URI}/case/accesses", json=data)

    # case_2 with circulation invite
    case_2 = prepare_case("circulation")
    case_2_circulation = case_2.work_items.get(task_id="circulation").child_case
    work_item_factory(
        case=case_2_circulation,
        assigned_users=[user.username],
        task=workflow_models.Task.objects.get(slug="circulation-decision"),
        document__form=form_models.Form.objects.get(slug="circulation-form"),
        child_case=None,
    )

    # case_3 no access for non-admin
    prepare_case("only admin")

    test_map = [
        (
            form_models.Form,
            form_schema.Form,
            ["pk"],
        ),
        (
            workflow_models.WorkItem,
            workflow_schema.WorkItem,
            ["task_id", "case__workflow_id"],
        ),
        (
            form_models.Document,
            form_schema.Document,
            ["work_item__task_id", "case__workflow_id"],
        ),
        (
            workflow_models.Case,
            workflow_schema.Case,
            ["family__meta__identifier", "workflow__pk"],
        ),
        (
            form_models.Question,
            form_schema.Question,
            ["pk"],
        ),
        (
            form_models.Answer,
            form_schema.Answer,
            ["question__pk", "value"],
        ),
        (
            analytics_models.AnalyticsTable,
            analytics_schema.AnalyticsTable,
            ["pk"],
        ),
    ]

    vis = MySAGWVisibility()

    for model, node, values_list in test_map:
        queryset = model.objects.all()
        filtered = vis.filter_queryset(node, queryset, admin_info)
        assert filtered.count() == visibility_map[model.__name__]
        values_to_snapshot = [
            tuple(xi for xi in v if xi is not None)
            for v in filtered.values_list(*values_list)
        ]

        assert sorted(values_to_snapshot) == snapshot(name=model.__name__)
