from datetime import datetime

from localized_fields.value import LocalizedValue
from rest_framework import exceptions

from caluma.caluma_core.validations import BaseValidation, validation_for
from caluma.caluma_form.schema import SaveDocumentDateAnswer

from .settings import settings


class CustomValidation(BaseValidation):
    @validation_for(SaveDocumentDateAnswer)
    def validate_birthdate_answers(self, mutation, data, info):
        if (
            settings.BIRTHDATE_SLUG_PART in data["question"].slug
            and data["question"].type == "date"
        ):
            # minimum age of 12
            if datetime.now().year - data["date"].year < 13:
                raise exceptions.ValidationError(
                    LocalizedValue(
                        {
                            "en": "Invalid date",
                            "de": "Nicht gültiges Datum",
                            "fr": "Date non valide",
                        }
                    ).translate()
                )

        return data
