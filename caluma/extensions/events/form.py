import csv
import io
import logging

from django.db import transaction
from django.db.models.signals import post_save

from caluma.caluma_core.events import on
from caluma.caluma_form import models as caluma_form_models

from ..settings import settings

logger = logging.getLogger(__name__)


@on(post_save, sender=caluma_form_models.AnswerDocument, raise_exception=True)
@transaction.atomic
def update_table_summary(instance, *args, **kwargs):
    """
    Update table summary.

    If a table question has the `meta` attributes `summary-question` and
    `summary-mode` set, then upon save of a table row (or answer within),
    a summary of the table will be written, as follows:

    In the parent document (the one containing the table answer), the
    referenced summary question is updated to contain a summary, calculated
    according to the given summary mode.

    Currently, only `csv` is allowed as a summary mode, but the code can be extended
    to support sums, averages, etc. as needed.
    """
    question = instance.answer.question
    main_document = instance.answer.document

    summary_question = question.meta.get("summary-question")
    summary_mode = question.meta.get("summary-mode")

    if not summary_question and not summary_mode:
        # no summary requested
        return

    logger.debug("Updating table summary: tq=%s", instance.answer.question_id)

    if not summary_question or not summary_mode:
        logger.warning(
            "Updating table summary: missing info in TQ meta: " "sq=%s, sm=%s",
            summary_question,
            summary_mode,
        )
        return

    logger.debug("Updating table summary: sq=%s sm=%s", summary_question, summary_mode)

    summary_answer, _ = caluma_form_models.Answer.objects.get_or_create(
        document=main_document, question_id=summary_question
    )

    summary_modes = {"csv": _make_csv_summary}

    summary_func = summary_modes.get(summary_mode)
    if not summary_func:
        logger.warning(
            'Updating table summary: summary mode "%s" does not exist. '
            "Must be one of %s",
            summary_mode,
            settings.TABLE_SUMMARY_MODES,
        )
        return

    summary_answer.value = summary_func(instance.answer)
    summary_answer.save()


@on(post_save, sender=caluma_form_models.Answer, raise_exception=True)
@transaction.atomic
def update_table_summary_from_row(instance, *args, **kwargs):
    ad = caluma_form_models.AnswerDocument.objects.filter(
        document=instance.document
    ).first()
    if not ad:
        return

    # AnswerDocument available, we're in a table
    # Make sure the summary (if any) is being updated
    update_table_summary(instance=ad)


@on(post_save, sender=caluma_form_models.Question, raise_exception=True)
@transaction.atomic
def update_table_summary_from_table_question(instance, *args, **kwargs):
    if instance.type != "table" or "summary-question" not in instance.meta:
        return

    # Call `update_table_summary()` for one AnswerDocument per every existing Answer
    updated_answers = []
    for ad in caluma_form_models.AnswerDocument.objects.filter(
        answer__question_id=instance.slug
    ):
        if ad.answer not in updated_answers:
            updated_answers.append(ad.answer)
            update_table_summary(instance=ad)


def _make_csv_summary(table_answer):
    def get_lines(answer_docs, row_question_slugs):
        for ad in answer_docs:
            result = {}
            answer_data = {
                a.question.slug: a.value
                for a in ad.document.answers.filter(question_id__in=row_question_slugs)
            }
            for question_slug in row_question_slugs:
                result[question_slug] = answer_data.get(question_slug, "")
            yield result

    logger.debug("Making CSV summary for %s", table_answer.question)
    answer_docs = caluma_form_models.AnswerDocument.objects.filter(
        answer=table_answer
    ).order_by("-sort")
    row_question_slugs = _sorted_form_question_slugs(table_answer.question.row_form)

    with io.StringIO() as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=row_question_slugs,
            delimiter=";",
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        for line in get_lines(answer_docs, row_question_slugs):
            writer.writerow(line)

        return csvfile.getvalue()


def _sorted_form_question_slugs(form):
    fqs = caluma_form_models.FormQuestion.objects.filter(form=form).order_by("-sort")
    return [fq.question.slug for fq in fqs]
