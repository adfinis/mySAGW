import pytest

from caluma.caluma_form import models as form_models, schema as form_schema
from caluma.caluma_workflow import models as workflow_models, schema as workflow_schema
from caluma.extensions.settings import settings
from caluma.extensions.visibilities import MySAGWVisibility


@pytest.mark.parametrize(
    "user_name,visibility_map",
    [
        (
            "admin",
            {
                "Form": 7,
                "WorkItem": 5,
                "Document": 3,
                "Case": 2,
                "Question": 20,
                "Answer": 3,
            },
        ),
        (
            "test",
            {
                "Form": 7,
                "WorkItem": 2,
                "Document": 2,
                "Case": 1,
                "Question": 20,
                "Answer": 2,
            },
        ),
    ],
)
def test_visibilities_default(
    db,
    caluma_data,
    case_access_event_mock,
    circulation,
    admin_info,
    requests_mock,
    user_name,
    visibility_map,
):
    admin_info.context.user.username = user_name
    admin_info.context.user.groups = [user_name]
    admin_info.context.user.group = user_name

    case = workflow_models.Case.objects.get(workflow__slug="document-review")
    case.document.form.is_published = True
    case.document.form.save()

    data = {"data": [{"attributes": {"case-id": str(case.pk)}}]}
    requests_mock.get(f"{settings.API_BASE_URI}/case/accesses", json=data)

    test_map = [
        (form_models.Form, form_schema.Form),
        (workflow_models.WorkItem, workflow_schema.WorkItem),
        (form_models.Document, form_schema.Document),
        (workflow_models.Case, workflow_schema.Case),
        (form_models.Question, form_schema.Question),
        (form_models.Answer, form_schema.Answer),
    ]

    vis = MySAGWVisibility()

    for model, node in test_map:
        queryset = model.objects.all()
        filtered = vis.filter_queryset(node, queryset, admin_info)
        assert filtered.count() == visibility_map[model.__name__]
