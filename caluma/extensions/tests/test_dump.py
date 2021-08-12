import json
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command


@pytest.mark.parametrize(
    "models,json_path",
    [
        (
            [
                "caluma_form.Form",
                "caluma_form.FormQuestion",
                "caluma_form.Question",
                "caluma_form.QuestionOption",
                "caluma_form.Option",
            ],
            Path.cwd() / "caluma" / "data" / "form-config.json",
        ),
        (
            [
                "caluma_workflow.Task",
                "caluma_workflow.Workflow",
                "caluma_workflow.Flow",
                "caluma_workflow.TaskFlow",
                "caluma_workflow.Case",
            ],
            Path.cwd() / "caluma" / "data" / "workflow-config.json",
        ),
    ],
)
def test_dump(caluma_data, models, json_path):
    out = StringIO()

    call_command(
        "dumpdata",
        *models,
        indent=4,
        stdout=out,
    )

    with open(json_path, "r") as dumped:
        assert json.load(dumped) == json.loads(
            out.getvalue()
        ), "Dumped models do not match file content"
