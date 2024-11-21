import pytest
from django.utils import timezone

from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import (
    complete_work_item,
    redo_work_item,
    reopen_case,
    skip_work_item,
    start_case,
)
from caluma.caluma_workflow.models import Case, Workflow, WorkItem

from ..settings import settings


@pytest.mark.usefixtures("_caluma_data")
def test_work_item_set_assigned_user(
    db,
    case_access_event_mock,
    document_review_case,
):
    assert document_review_case.work_items.get(
        task_id="submit-document",
    ).assigned_users == ["test"]


@pytest.mark.usefixtures("_caluma_data")
def test_work_item_create_circulation(
    db,
    case_access_event_mock,
    circulation,
):
    assert circulation.workflow_id == "circulation"


@pytest.mark.usefixtures("_caluma_data")
def test_work_item_finish_circulation(
    db,
    user,
    case_access_event_mock,
    circulation,
):
    complete_work_item(circulation.work_items.get(task_id="finish-circulation"), user)

    assert (
        circulation.work_items.get(task_id="invite-to-circulation").status
        == WorkItem.STATUS_CANCELED
    )


@pytest.mark.usefixtures("_caluma_data")
def test_work_item_additional_data(
    db,
    user,
    case_access_event_mock,
    circulation,
):
    Question.objects.filter(formquestion__form__pk="additional-data-form").update(
        is_required="false",
    )

    case = circulation.parent_work_item.case

    skip_work_item(case.work_items.get(task_id="circulation"), user)

    case.work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value="decision-and-credit-decision-additional-data",
    )

    skip_work_item(case.work_items.get(task_id="decision-and-credit"), user)

    assert (
        case.work_items.get(task_id="additional-data").status == WorkItem.STATUS_READY
    )

    complete_work_item(case.work_items.get(task_id="additional-data"), user)

    assert (
        case.work_items.get(task_id="advance-credits").status == WorkItem.STATUS_READY
    )
    assert (
        case.work_items.get(task_id="additional-data-form").status
        == WorkItem.STATUS_SUSPENDED
    )


@pytest.mark.usefixtures("_caluma_data")
def test_work_item_define_amount(
    db,
    user,
    case_access_event_mock,
    circulation,
    send_mail_mock,
):
    work_items = circulation.parent_work_item.case.work_items

    skip_work_item(work_items.get(task_id="circulation"), user)
    work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value="decision-and-credit-decision-additional-data",
    )
    complete_work_item(work_items.get(task_id="decision-and-credit"), user)
    complete_work_item(work_items.get(task_id="additional-data"), user)
    work_items.get(task_id="define-amount").document.answers.create(
        question_id="define-amount-decision",
        value="define-amount-decision-reject",
    )
    skip_work_item(work_items.get(task_id="define-amount"), user)

    assert (
        work_items.get(task_id="additional-data-form").status
        == WorkItem.STATUS_SUSPENDED
    )

    complete_work_item(
        work_items.get(task_id="additional-data", status=WorkItem.STATUS_READY),
        user,
    )

    answers = work_items.get(task_id="additional-data-form").document.answers

    answers.create(
        question_id="define-amount-decision",
        value="define-amount-decision-continue",
    )
    answers.create(
        question_id="additional-data-adresse",
        value="Foo",
    )
    answers.create(
        question_id="additional-data-bank",
        value="Foo",
    )
    answers.create(
        question_id="additional-data-iban",
        value="Foo",
    )
    answers.create(
        question_id="additional-data-name",
        value="Foo",
    )

    define_amount = work_items.get(
        task_id="define-amount",
        status=WorkItem.STATUS_READY,
    )
    define_amount.document.answers.create(
        question_id="define-amount-decision",
        value="define-amount-decision-continue",
    )
    complete_work_item(define_amount, user)

    assert work_items.get(task_id="complete-document").status == WorkItem.STATUS_READY
    assert (
        work_items.get(task_id="additional-data-form").status
        == WorkItem.STATUS_COMPLETED
    )
    assert work_items.get(task_id="advance-credits").status == WorkItem.STATUS_COMPLETED
    assert circulation.parent_work_item.case.status == Case.STATUS_RUNNING


@pytest.mark.usefixtures("_caluma_data")
def test_work_item_invite_to_circulation(
    db,
    user,
    case_access_event_mock,
    circulation,
):
    complete_work_item(
        circulation.work_items.get(task_id="invite-to-circulation"),
        user,
        {
            "assign_users": [
                {"idpId": "ab", "name": "AB", "email": "a@b.c"},
                {"idpId": "cd", "name": "CD", "email": "c@d.e"},
            ],
        },
    )

    decisions = circulation.work_items.filter(task_id="circulation-decision")
    assert decisions.count() == 2
    assert [v["assigned_users"][0] for v in decisions.values("assigned_users")] == [
        "ab",
        "cd",
    ]


@pytest.mark.usefixtures("_caluma_data")
def test_case_complete_circulation(
    db,
    user,
    case_access_event_mock,
    circulation,
):
    complete_work_item(circulation.work_items.get(task_id="finish-circulation"), user)

    assert circulation.parent_work_item.status == WorkItem.STATUS_COMPLETED


@pytest.mark.usefixtures("_caluma_data")
@pytest.mark.parametrize(
    "same_year,first",
    [(True, False), (False, False), (False, True)],
)
def test_case_number(
    db,
    case_access_event_mock,
    user,
    form_question_factory,
    answer_factory,
    same_year,
    first,
):
    question = Question.objects.get(pk="dossier-nr")
    form_question = form_question_factory(question=question)
    old_year = year = timezone.now().year
    if not same_year:
        old_year = old_year - 1

    if not first:
        for i in range(1, 4):
            answer_factory(question=form_question.question, value=f"{old_year}-000{i}")

    expected_no = f"{year}-0004"
    if not same_year:
        expected_no = f"{year}-0001"

    case = start_case(
        workflow=Workflow.objects.get(pk="document-review"),
        form=form_question.form,
        user=user,
    )

    assert case.document.answers.get(question=question).value == expected_no


@pytest.mark.usefixtures("_caluma_data")
def test_case_status(
    db,
    case_access_event_mock,
    document_review_case,
    user,
):
    case = document_review_case
    assert case.meta["status"] == "submit"

    skip_work_item(case.work_items.get(task_id="submit-document"), user)
    assert case.meta["status"] == "audit"

    case.work_items.get(task_id="review-document").document.answers.create(
        question_id="review-document-decision",
        value="review-document-decision-continue",
    )
    skip_work_item(case.work_items.get(task_id="review-document"), user)
    assert case.meta["status"] == "audit"

    skip_work_item(case.work_items.get(task_id="circulation"), user)
    assert case.meta["status"] == "audit"

    case.work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value="decision-and-credit-decision-additional-data",
    )
    skip_work_item(case.work_items.get(task_id="decision-and-credit"), user)
    assert case.meta["status"] == "submit-receipts"

    skip_work_item(case.work_items.get(task_id="additional-data"), user)
    skip_work_item(case.work_items.get(task_id="additional-data-form"), user)
    assert case.meta["status"] == "decision"

    skip_work_item(case.work_items.get(task_id="advance-credits"), user)
    assert case.meta["status"] == "decision"

    case.work_items.get(task_id="define-amount").document.answers.create(
        question_id="define-amount-decision",
        value="define-amount-decision-continue",
    )
    skip_work_item(case.work_items.get(task_id="define-amount"), user)
    assert case.meta["status"] == "decision"

    skip_work_item(case.work_items.get(task_id="complete-document"), user)
    assert case.meta["status"] == "complete"

    reopen_case(case, [case.work_items.get(task_id="complete-document")], user)
    assert case.meta["status"] == "decision"


@pytest.mark.usefixtures("_caluma_data")
@pytest.mark.parametrize("lang", ["de", "en", "fr"])
@pytest.mark.parametrize(
    "task_slug, revise, early_career_form",
    [
        ("review-document", False, False),
        ("review-document", False, True),
        ("revise-document", False, False),
        ("additional-data", False, False),
        ("additional-data", True, False),
        ("complete-document", False, False),
        ("decision-and-credit", False, False),
        ("decision-and-credit", False, True),
    ],
)
def test_send_work_item_mail(  # noqa: PLR0915
    db,
    user,
    case_access_event_mock,
    document_review_case,
    mailoutbox,
    task_slug,
    revise,
    early_career_form,
    lang,
    snapshot,
    mocker,
):
    if lang != "de":
        mock = mocker.patch("caluma.extensions.events.work_item.get_users_for_case")
        mock.return_value = [
            {
                "idp-id": "267796f2-ae48-4235-93d7-bf26e8ba66bb",
                "first-name": "Winston",
                "last-name": "Smith",
                "email": "test-send@example.com",
                "language": lang,
            },
        ]
    case = document_review_case
    if early_career_form:
        case.document.form.slug = settings.EARLY_CAREER_AWARD_FORM_SLUG
        case.document.form.save()

    review_document_decision_answer = "review-document-decision-continue"

    if task_slug == "revise-document":
        review_document_decision_answer = "review-document-decision-reject"
    elif task_slug == "review-document":
        review_document_decision_answer = "review-document-decision-complete"

    case.document.answers.create(
        question_id="dossier-nr",
        value="1984-0023",
    )

    skip_work_item(case.work_items.get(task_id="submit-document"), user)
    review_work_item = case.work_items.get(task_id="review-document")
    review_work_item.document.answers.create(
        question_id="review-document-decision",
        value=review_document_decision_answer,
    )
    complete_work_item(review_work_item, user)

    if task_slug == "decision-and-credit":
        skip_work_item(case.work_items.get(task_id="circulation"), user)
        decision_credit_work_item = case.work_items.get(task_id="decision-and-credit")
        decision_credit_work_item.document.answers.create(
            question_id="decision-and-credit-decision",
            value="decision-and-credit-decision-close",
        )
        complete_work_item(decision_credit_work_item, user)

    if task_slug in ["additional-data", "complete-document"]:
        skip_work_item(case.work_items.get(task_id="circulation"), user)
        decision_credit_work_item = case.work_items.get(task_id="decision-and-credit")
        decision_credit_work_item.document.answers.create(
            question_id="decision-and-credit-decision",
            value="decision-and-credit-decision-additional-data",
        )
        decision_credit_work_item.document.answers.create(
            question_id="gesprochener-rahmenkredit",
            value=23000.0,
        )
        complete_work_item(decision_credit_work_item, user)

        if revise:
            complete_work_item(case.work_items.get(task_id="additional-data"), user)
            define_amount_work_item = case.work_items.get(task_id="define-amount")
            define_amount_work_item.document.answers.create(
                question_id="define-amount-decision",
                value="define-amount-decision-reject",
            )
            complete_work_item(define_amount_work_item, user)

    if task_slug == "complete-document":
        additional_data_work_item = case.work_items.get(task_id="additional-data")
        additional_data_form_work_item = case.work_items.get(
            task_id="additional-data-form",
        )
        additional_data_form_work_item.document.answers.create(
            question_id="additional-data-adresse",
            value="street",
        )
        additional_data_form_work_item.document.answers.create(
            question_id="additional-data-bank",
            value="bank",
        )
        additional_data_form_work_item.document.answers.create(
            question_id="additional-data-iban",
            value="iban",
        )
        additional_data_form_work_item.document.answers.create(
            question_id="additional-data-name",
            value="name",
        )
        complete_work_item(additional_data_form_work_item, user)
        complete_work_item(additional_data_work_item, user)

        define_amount_work_item = case.work_items.get(task_id="define-amount")
        define_amount_work_item.document.answers.create(
            question_id="define-amount-amount-float",
            value=23000.0,
        )
        define_amount_work_item.document.answers.create(
            question_id="define-amount-decision",
            value="define-amount-decision-continue",
        )
        complete_work_item(define_amount_work_item, user)

    expected_mails = 1
    if task_slug == "complete-document" or revise:
        expected_mails = 2

    assert len(mailoutbox) == expected_mails
    mail = mailoutbox[expected_mails - 1]
    assert mail.from_email == settings.MAILING_SENDER
    assert mail.to == ["test-send@example.com"]
    snapshot.assert_match(mail.subject)
    snapshot.assert_match(mail.body.replace(str(case.pk), "my-case-id"))


@pytest.mark.usefixtures("_caluma_data")
def test_access_control(
    db,
    user,
    identities_mock,
    form_question_factory,
    get_token_mock,
    case_access_create_request_mock,
):
    form_question = form_question_factory()

    start_case(
        workflow=Workflow.objects.get(pk="document-review"),
        form=form_question.form,
        user=user,
    )
    assert case_access_create_request_mock.called


@pytest.mark.usefixtures("_caluma_data")
def test_redo_circulation(
    db,
    user,
    case_access_event_mock,
    circulation,
    work_item_factory,
):
    Question.objects.filter(formquestion__form__pk="additional-data-form").update(
        is_required="false",
    )

    circ_work_item = circulation.parent_work_item

    work_item_factory(
        case=circulation,
        task_id="circulation-decision",
        status=WorkItem.STATUS_READY,
    )
    skip_work_item(circ_work_item.case.work_items.get(task_id="circulation"), user)

    assert (
        circ_work_item.child_case.work_items.get(task_id="finish-circulation").status
        == WorkItem.STATUS_CANCELED
    )
    assert circ_work_item.child_case.pk == circulation.pk
    assert circ_work_item.child_case.work_items.count() == 3

    redo_work_item(circ_work_item.case.work_items.get(task_id="circulation"), user)

    circ_work_item.refresh_from_db()
    assert (
        circ_work_item.child_case.work_items.get(task_id="finish-circulation").status
        == WorkItem.STATUS_READY
    )
    assert circ_work_item.child_case.pk == circulation.pk
    assert circ_work_item.child_case.work_items.count() == 3


@pytest.mark.usefixtures("_caluma_data")
def test_redo_review_document(
    db,
    user,
    case_access_event_mock,
    circulation,
    work_item_factory,
):
    Question.objects.filter(formquestion__form__pk="additional-data-form").update(
        is_required="false",
    )

    circ_work_item = circulation.parent_work_item

    previous_case = circ_work_item.child_case.pk
    work_item_factory(
        case=circulation,
        task_id="circulation-decision",
        status=WorkItem.STATUS_READY,
    )
    assert circ_work_item.child_case.work_items.count() == 3

    redo_work_item(circ_work_item.case.work_items.get(task_id="review-document"), user)

    circ_work_item.refresh_from_db()
    new_case = circ_work_item.child_case.pk
    assert previous_case != new_case
    assert circ_work_item.child_case.work_items.count() == 2


@pytest.mark.usefixtures("_caluma_data")
@pytest.mark.parametrize(
    "decision,expected_work_item_task",
    [
        (
            "define-amount",
            "define-amount",
        ),
        (
            "additional-data",
            "advance-credits",
        ),
    ],
)
def test_redo_define_amount(
    db,
    user,
    case_access_event_mock,
    circulation,
    decision,
    expected_work_item_task,
    send_mail_mock,
):
    Question.objects.filter(formquestion__form__pk="additional-data-form").update(
        is_required="false",
    )

    case = circulation.parent_work_item.case

    skip_work_item(case.work_items.get(task_id="circulation"), user)

    case.work_items.get(task_id="decision-and-credit").document.answers.create(
        question_id="decision-and-credit-decision",
        value=f"decision-and-credit-decision-{decision}",
    )

    complete_work_item(case.work_items.get(task_id="decision-and-credit"), user)

    if decision != "define-amount":
        complete_work_item(case.work_items.get(task_id="additional-data"), user)

    case.work_items.get(task_id="define-amount").document.answers.create(
        question_id="define-amount-decision",
        value="define-amount-decision-continue",
    )

    complete_work_item(case.work_items.get(task_id="define-amount"), user)

    redo_work_item(case.work_items.get(task_id="define-amount"), user)

    assert case.status == Case.STATUS_RUNNING
    assert case.work_items.filter(
        task_id=expected_work_item_task,
        status=WorkItem.STATUS_READY,
    ).exists()


@pytest.fixture
def add_table_with_summary(
    _caluma_data,
    form_factory,
    question_factory,
    form_question_factory,
    case_access_event_mock,
    document_review_case,
):
    main_doc = document_review_case.document
    main_form = main_doc.form

    row_form = form_factory(slug="row_form")
    table_question = question_factory(
        type=Question.TYPE_TABLE,
        slug="table",
        row_form=row_form,
        is_required="true",
        is_hidden="false",
        meta={"summary-question": "summary", "summary-mode": "csv"},
    )
    form_question_factory(form=main_form, question=table_question)
    row_question_1 = question_factory(
        type=Question.TYPE_FLOAT,
        slug="row1",
        is_required="true",
        is_hidden="false",
    )
    form_question_factory(form=row_form, question=row_question_1)

    row_question_2 = question_factory(
        type=Question.TYPE_TEXT,
        slug="row2",
        is_required="true",
        is_hidden="false",
    )
    form_question_factory(form=row_form, question=row_question_2)

    row_question_3 = question_factory(
        type=Question.TYPE_TEXT,
        slug="row3",
        is_required="true",
        is_hidden="false",
    )
    form_question_factory(form=row_form, question=row_question_3)

    question_factory(type=Question.TYPE_TEXTAREA, slug="summary", is_hidden="true")
    question_factory(type=Question.TYPE_TEXTAREA, slug="summary2", is_hidden="true")
    return main_doc, main_form, table_question, row_form, row_question_1, row_question_3


def test_table_summary(
    document_factory,
    case_access_event_mock,
    add_table_with_summary,
):
    main_doc, main_form, table_question, row_form, row_question_1, row_question_3 = (
        add_table_with_summary
    )

    # save first row document in TableAnswer
    row_document_1 = document_factory(form=row_form)
    save_answer(question=table_question, document=main_doc, value=[row_document_1.pk])
    assert (
        main_doc.answers.get(question_id="summary").value == "row1;row2;row3\r\n;;\r\n"
    )

    # save answer to first row question
    save_answer(value=23.5, question=row_question_1, document=row_document_1)
    assert (
        main_doc.answers.get(question_id="summary").value
        == "row1;row2;row3\r\n23.5;;\r\n"
    )

    # save answer to third row question and test quoting
    save_answer(
        value='bar;baz\r\nlorem "ipsem"; \'dolor\n',
        question=row_question_3,
        document=row_document_1,
    )
    assert (
        main_doc.answers.get(question_id="summary").value
        == 'row1;row2;row3\r\n23.5;;"bar;baz\r\nlorem ""ipsem""; \'dolor\n"\r\n'
    )

    # override answer to third row question
    save_answer(value="bar", question=row_question_3, document=row_document_1)
    assert (
        main_doc.answers.get(question_id="summary").value
        == "row1;row2;row3\r\n23.5;;bar\r\n"
    )

    # save second row document in TableAnswer
    row_document_2 = document_factory(form=row_form)
    save_answer(
        question=table_question,
        document=main_doc,
        value=[row_document_1.pk, row_document_2.pk],
    )
    assert (
        main_doc.answers.get(question_id="summary").value
        == "row1;row2;row3\r\n23.5;;bar\r\n;;\r\n"
    )

    # save answer to first row question to second row document
    save_answer(value=23.5, question=row_question_1, document=row_document_2)
    assert (
        main_doc.answers.get(question_id="summary").value
        == "row1;row2;row3\r\n23.5;;bar\r\n23.5;;\r\n"
    )

    table_question.meta = {"summary-question": "summary2", "summary-mode": "csv"}
    table_question.save()
    assert (
        main_doc.answers.get(question_id="summary2").value
        == "row1;row2;row3\r\n23.5;;bar\r\n23.5;;\r\n"
    )


def test_table_summary_errors(
    caplog,
    document_factory,
    case_access_event_mock,
    add_table_with_summary,
):
    main_doc, main_form, table_question, row_form, row_question_1, row_question_3 = (
        add_table_with_summary
    )

    table_question.meta = {}
    table_question.save()

    # save a row document in TableAnswer
    # this should not try to make a summary and should not error
    row_document = document_factory(form=row_form)
    save_answer(question=table_question, document=main_doc, value=[row_document.pk])

    # save row document with faulty summary config
    table_question.meta = {"summary-question": "summary"}
    table_question.save()
    assert len(caplog.records) == 1
    assert (
        caplog.messages[0]
        == "Updating table summary: missing info in TQ meta: sq=summary, sm=None"
    )
    row_document = document_factory(form=row_form)
    save_answer(question=table_question, document=main_doc, value=[row_document.pk])
    assert len(caplog.records) == 2
    assert (
        caplog.messages[1]
        == "Updating table summary: missing info in TQ meta: sq=summary, sm=None"
    )

    # save row document with faulty summary config
    table_question.meta = {"summary-question": "summary", "summary-mode": "missing"}
    table_question.save()
    assert len(caplog.records) == 3
    assert (
        caplog.messages[2]
        == f'Updating table summary: summary mode "missing" does not exist. '
        f"Must be one of {settings.TABLE_SUMMARY_MODES}"
    )
    row_document = document_factory(form=row_form)
    save_answer(question=table_question, document=main_doc, value=[row_document.pk])
    assert len(caplog.records) == 4
    assert (
        caplog.messages[3]
        == f'Updating table summary: summary mode "missing" does not exist. '
        f"Must be one of {settings.TABLE_SUMMARY_MODES}"
    )

    # save row document with faulty summary config
    table_question.meta = {"summary-mode": "csv"}
    table_question.save()
    row_document = document_factory(form=row_form)
    save_answer(question=table_question, document=main_doc, value=[row_document.pk])
    assert len(caplog.records) == 5
    assert (
        caplog.messages[4]
        == "Updating table summary: missing info in TQ meta: sq=None, sm=csv"
    )
