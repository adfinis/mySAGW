import pytest

from caluma.caluma_form import models as form_models, schema as form_schema
from caluma.caluma_workflow import models as workflow_models, schema as workflow_schema
from caluma.extensions.visibilities import MySAGWVisibility


@pytest.mark.parametrize(
    "name,visibility_map",
    [
        (
            "admin",
            {
                "Form": 3,
                "WorkItem": 3,
                "Document": 6,
                "Case": 3,
                "Question": 1,
                "Answer": 1,
            },
        ),
        (
            "test1",
            {
                "Form": 3,
                "WorkItem": 0,
                "Document": 1,
                "Case": 1,
                "Question": 1,
                "Answer": 1,
            },
        ),
        (
            "test2",
            {
                "Form": 3,
                "WorkItem": 1,
                "Document": 1,
                "Case": 1,
                "Question": 1,
                "Answer": 0,
            },
        ),
        (
            "test3",
            {
                "Form": 3,
                "WorkItem": 1,
                "Document": 0,
                "Case": 0,
                "Question": 1,
                "Answer": 0,
            },
        ),
    ],
)
def test_visibilities_default(
    db,
    work_item_factory,
    form_question_factory,
    answer_factory,
    admin_info,
    name,
    visibility_map,
):
    admin_info.context.user.username = name
    admin_info.context.user.groups = [name]
    admin_info.context.user.group = name

    wi1 = work_item_factory(
        assigned_users=["foo"],
        document__created_by_user="test1",
        case__created_by_user="test2",
        child_case=None,
    )
    work_item_factory(
        assigned_users=["test2"],
        document__created_by_user="foo",
        case__created_by_user="test1",
        document__form=wi1.document.form,
        case__document__form=wi1.document.form,
        task__form=wi1.document.form,
        child_case=None,
    )

    work_item_factory(
        addressed_groups=["test3"],
        document__form=wi1.document.form,
        case__document__form=wi1.document.form,
        task__form=wi1.document.form,
        child_case=None,
    )

    fq = form_question_factory(form=wi1.document.form, question__type="text")
    answer_factory(
        document=wi1.document,
        question=fq.question,
        value="foo",
        created_by_user="test1",
    )

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
