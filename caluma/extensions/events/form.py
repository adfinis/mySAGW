from django.db import transaction

from caluma.caluma_core.events import on

from django.db.models.signals import post_save
from caluma.caluma_form import models as caluma_form_models


@on(post_save, sender=caluma_form_models.AnswerDocument, raise_exception=True)
@transaction.atomic
def update_table_summary(instance, *args, **kwargs):
    # TODO deal with updating columns inside already-existing row doc
    question = instance.answer.question
    main_document = instance.answer.document

    summary_question = question.meta.get("summary-question")
    summary_mode = question.meta.get("summary-mode")
    print(f"Updating table summary: tq={instance.answer.question_id}")

    if not summary_question or not summary_mode:
        print(
            f"Updating table summary: missing info in TQ meta: sq={summary_question},sm={summary_mode}"
        )
        return

    print(f"Updating table summary: sq={summary_question} mode={summary_mode}")

    summary_answer, _ = caluma_form_models.Answer.objects.get_or_create(
        document=main_document, question_id=summary_question
    )

    summary_modes = {"csv": _make_csv_summary}

    summary_func = summary_modes.get(summary_mode)
    if not summary_func:
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
    # Trigger by just saving the answerdocument
    ad.save()


def _make_csv_summary(table_answer):
    print(f"Making CSV summary for {table_answer.question}")
    cols = []
    rows = []
    answer_docs = caluma_form_models.AnswerDocument.objects.filter(
        answer=table_answer
    ).order_by("-sort")
    for ad in answer_docs:
        cols = _sorted_form_questions(ad.document.form, cols)
        answers = {
            ans.question_id: ans.value
            for ans in ad.document.answers.filter(question__in=cols)
        }
        values = "; ".join([answers.get(col.slug, "") for col in cols])
        rows.append(values)

    result = "\n".join(rows)
    print(f"Making CSV summary for {table_answer.question}: result={result}")
    return result


def _sorted_form_questions(form, previous_val):
    if previous_val:
        return previous_val
    fqs = caluma_form_models.FormQuestion.objects.filter(form=form).order_by("-sort")
    return [fq.question for fq in fqs]
