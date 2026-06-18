import pytest
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from caluma.caluma_form.schema import SaveDocumentDateAnswer, SaveTableQuestion

from ..validations import CustomValidation


@pytest.mark.parametrize(
    "question__slug,question__type",
    [("test-geburtsdatum", "date")],
)
@pytest.mark.parametrize(
    "date",
    [timezone.now(), timezone.datetime.strptime("10-10-1990", "%d-%m-%Y")],
)
def test_validate_birthdate_answers(db, question, info, date):
    try:
        data = CustomValidation().validate(
            SaveDocumentDateAnswer,
            {"question": question, "date": date},
            info,
        )
        assert data["date"] == date
    except ValidationError as error:
        assert "Nicht gültiges Datum" in str(error)


@pytest.mark.parametrize(
    "question__slug,question__type",
    [("test-summary", "textarea")],
)
@pytest.mark.parametrize(
    "meta,error",
    [
        ({"summary-question": "test-summary"}, True),
        ({"summary-question": "test-summary", "summary-mode": "missing"}, True),
        ({"summary-question": "test-missing", "summary-mode": "csv"}, True),
        ({"summary-mode": "csv"}, True),
        ({"summary-question": "test-summary", "summary-mode": "csv"}, False),
        ({}, False),
    ],
)
def test_validate_table_summary_config(db, question, info, meta, error):
    try:
        CustomValidation().validate(
            SaveTableQuestion,
            {
                "slug": "test-table",
                "label": "test table",
                "is_required": "false",
                "is_hidden": "false",
                "meta": meta,
                "row_form": "foo",
                "type": "table",
            },
            info,
        )
        assert not error
    except ValidationError:
        assert error
