from django.core.mail import send_mail

from caluma.caluma_form.models import Answer

from ..common import format_currency, get_users_for_case
from ..settings import settings
from .email_texts import (
    email_cost_approval,
    email_decision_and_credit_rejection_early_career_award,
    email_general,
    email_payout_amount,
    email_rejection,
    email_review_document_complete_early_career_award,
    email_review_document_rejection_early_career_award,
)


def get_work_item(case, task_slug, order_by="-created_at"):
    return case.work_items.filter(task__slug=task_slug).order_by(order_by).first()


def check_define_amount_not_rejected(case):
    define_amount_work_item = get_work_item(case, "define-amount", "-closed_at")
    return not (
        define_amount_work_item
        and define_amount_work_item.status == "completed"
        and define_amount_work_item.document.answers.filter(
            question_id="define-amount-decision",
            value="define-amount-decision-reject",
        ).exists()
    )


def get_mail_template_and_values(work_item):
    case = work_item.case
    try:
        dossier_nr = case.document.answers.get(question_id="dossier-nr").value
    except Answer.DoesNotExist:
        dossier_nr = "Not found"

    format_values = {
        "link": f"{settings.SELF_URI}/cases/{case.pk}",
        "dossier_nr": dossier_nr,
    }

    is_eca_form = case.document.form.slug in settings.EARLY_CAREER_AWARD_FORM_SLUGS

    match work_item.task.slug:
        case "additional-data" if check_define_amount_not_rejected(case):
            # If the `additional-data` WorkItem is opened for the first time, we
            # send the cost approval email. For each subsequent reopening of the
            # WorkItem (in case of rejection) , we'll send the general email.
            decision_and_credit_work_item = get_work_item(case, "decision-and-credit")
            framework_credit = decision_and_credit_work_item.document.answers.get(
                question__slug="gesprochener-rahmenkredit",
            ).value
            format_values["framework_credit"] = format_currency(framework_credit, "CHF")

            template = email_cost_approval
        case "complete-document":
            # This means that the case has been completed and the requested amount is
            # approved.
            define_amount_work_item = get_work_item(case, "define-amount")
            payout_amount_answer = define_amount_work_item.document.answers.filter(
                question__slug="define-amount-amount-float",
            ).first()
            format_values["payout_amount"] = format_currency(
                payout_amount_answer.value if payout_amount_answer else 0,
                "CHF",
            )
            template = email_payout_amount
        case "revise-document" if is_eca_form:
            # There is missing information in the application. Since this
            # is for the Early Career Award, all mail templates are in english.
            template = email_review_document_rejection_early_career_award
        case "review-document" if is_eca_form:
            # The application was rejected (not to be confused with the question value
            # "Zurückgewiesen" reject which is handled in the case `revise-document`).
            # Since this is for the Early Career Award, all mail templates are in english.
            template = email_review_document_complete_early_career_award
        case "decision-and-credit" if is_eca_form:
            # The decision was negative and the requested amount will not be granted.
            # Since this is for the Early Career Award, all mail templates are in english.
            template = email_decision_and_credit_rejection_early_career_award
        case "review-document" | "decision-and-credit":
            # If this is a non Early Career Award form, we send the same email if it was
            # rejected at `review-document` or `decision-and-credit`.
            template = email_rejection
        case _:
            # Catch all for tasks `revise-document` and `additional-data` if previous
            # conditions are not fulfilled. So if `revise-document` is not a ECA form or
            # `additional-data` was rejected.
            template = email_general
    return template, format_values


def send_work_item_mail(work_item):
    """
    Send the work_item emails.

    This must reside in a separate function in order to be able to patch it in the
    tests.
    """
    users = get_users_for_case(work_item.case)
    email_template, format_values = get_mail_template_and_values(work_item)
    for user in users:
        subject = email_template.EMAIL_SUBJECTS[user["language"]]

        subject = subject.format(**format_values)

        body = email_template.EMAIL_BODIES[user["language"]].format(
            first_name=user["first-name"] or "",
            last_name=user["last-name"] or "",
            **format_values,
        )
        send_mail(
            subject,
            body,
            settings.MAILING_SENDER,
            [user["email"]],
            fail_silently=True,
        )
