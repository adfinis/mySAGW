from datetime import datetime

import pytest
from rest_framework.exceptions import ValidationError

from caluma.caluma_form.schema import SaveDocumentDateAnswer

from ..validations import CustomValidation


@pytest.mark.parametrize(
    "question__slug,question__type", [("test-geburtsdatum", "date")]
)
@pytest.mark.parametrize(
    "date", [datetime.now(), datetime.strptime("10-10-1990", "%d-%m-%Y")]
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
