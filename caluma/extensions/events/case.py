from django.db import transaction
from django.utils import timezone

from caluma.caluma_core.events import on
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as caluma_workflow_api
from caluma.caluma_workflow.events import post_complete_case, post_create_case


@on(post_complete_case, raise_exception=True)
@transaction.atomic
def complete_circulation(sender, case, user, **kwargs):
    if case.workflow_id == "circulation":
        caluma_workflow_api.complete_work_item(
            work_item=case.parent_work_item, user=user
        )


@on(post_create_case, raise_exception=True)
def create_case_number(sender, case, user, context, **kwargs):
    if (
        not case.workflow.slug == "document-review"
        or not case.document.form.questions.filter(pk="dossier-nr").exists()
        or case.document.answers.filter(question__slug="dossier-nr").exists()
    ):
        return

    question = caluma_form_models.Question.objects.get(pk="dossier-nr")
    last_answer = (
        caluma_form_models.Answer.objects.filter(question=question)
        .order_by("-value")
        .first()
    )

    year = str(timezone.now().year)
    last_year, last_no = year, "0000"

    if last_answer:
        last_year, last_no = last_answer.value.split("-")

    new_no = "1"
    if last_year == year:
        new_no = str(int(last_no) + 1)

    new_dossier_no = f"{year}-{new_no.zfill(4)}"

    caluma_form_models.Answer.objects.create(
        question=question, document=case.document, value=new_dossier_no
    )
