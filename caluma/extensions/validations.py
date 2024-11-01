from django.utils import timezone
from localized_fields.value import LocalizedValue
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError

from caluma.caluma_core.validations import BaseValidation, validation_for
from caluma.caluma_form.models import Question
from caluma.caluma_form.schema import SaveDocumentDateAnswer, SaveTableQuestion

from .settings import settings


class CustomValidation(BaseValidation):
    @validation_for(SaveDocumentDateAnswer)
    def validate_birthdate_answers(self, mutation, data, info):
        # minimum age of 12
        if (
            settings.BIRTHDATE_SLUG_PART in data["question"].slug
            and data["question"].type == "date"
            and timezone.now().year - data["date"].year < 13
        ):
            raise exceptions.ValidationError(
                LocalizedValue(
                    {
                        "en": "Invalid date",
                        "de": "Nicht gültiges Datum",
                        "fr": "Date non valide",
                    },
                ).translate(),
            )

        return data

    @validation_for(SaveTableQuestion)
    def validate_table_summary_config(self, mutation, data, info):
        summary_question = data["meta"].get("summary-question")
        summary_mode = data["meta"].get("summary-mode")

        if not summary_question and not summary_mode:
            return data

        if summary_mode and not summary_question:
            msg = (
                '"[meta] summary-question" must be provided when setting "summary-mode"'
            )
            raise ValidationError(msg)

        if summary_question and not summary_mode:
            msg = (
                '"[meta] summary-mode" must be provided when setting "summary-question"'
            )
            raise ValidationError(msg)

        if summary_mode not in settings.TABLE_SUMMARY_MODES:
            msg = f'"[meta] summary-mode" must be one of {settings.TABLE_SUMMARY_MODES} when setting "summary-question"'
            raise ValidationError(msg)

        if not Question.objects.filter(slug=summary_question).exists():
            msg = (
                '"[meta] summary-question" must be a valid slug of an existing question'
            )
            raise ValidationError(msg)

        return data
