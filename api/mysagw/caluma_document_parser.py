import io

import requests
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.translation import get_language
from pypdf import PdfWriter
from pypdf.errors import FileNotDecryptedError, PdfReadError
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from rest_framework import status

from mysagw.dms_client import DMSClient
from mysagw.utils import format_currency

SUPPORTED_MERGE_CONTENT_TYPES = ["application/pdf", "image/png", "image/jpeg"]


class DMSException(Exception):
    def __init__(self, response):
        self.response = response


def prepare_image_file_for_pdf_merge(file):
    document_width, document_height = A4
    printable_document_width, printable_document_height = (203 * mm, 289 * mm)
    document_width_diff = document_width - printable_document_width
    document_height_diff = document_height - printable_document_height

    # prepare the page
    page = io.BytesIO()
    can = canvas.Canvas(page, pagesize=A4)

    # load image and get dimensions
    image = ImageReader(file["file"])
    image_width, image_height = image.getSize()
    image_aspect = image_height / float(image_width)

    # determine the print dimensions - here be dragons
    print_width = printable_document_width
    print_height = printable_document_width * image_aspect
    if print_height > printable_document_height:
        print_height = printable_document_height
        print_width = printable_document_height * image_aspect

    if image_width < print_width:
        print_width = image_width
        print_height = print_width * image_aspect
        if print_height > printable_document_height:
            print_height = printable_document_height
            print_width = printable_document_height * image_aspect

    # calculate x and y for `can.drawImage()`
    x_start = document_width - (document_width - document_width_diff / 2)
    y_start = document_height - document_height_diff / 2 - print_height

    # draw the image to the canvas and yield the page
    can.drawImage(
        image,
        x_start,
        y_start,
        width=print_width,
        height=print_height,
        preserveAspectRatio=True,
        anchor="nw",
        mask="auto",
    )
    can.save()
    return page


def get_caluma_file(url):
    file = io.BytesIO()
    resp = requests.get(url, verify=settings.ENV != "dev", timeout=15)
    file.write(resp.content)
    return {"file": file, "content-type": resp.headers.get("content-type")}


class DocumentParser:
    def __init__(self, data):
        self.data = data
        self.parsed_data = None
        self.merger = PdfWriter()  # will contain all attachments
        self.file_count = 0

    @staticmethod
    def value_key_for_question(question_type):
        value_key_map = {
            "TextQuestion": "stringValue",
            "TextareaQuestion": "stringValue",
            "IntegerQuestion": "integerValue",
            "FloatQuestion": "floatValue",
            "MultipleChoiceQuestion": "listValue",
            "ChoiceQuestion": "stringValue",
            "FilesQuestion": "filesValue",
            "DateQuestion": "dateValue",
            "CalculatedFloatQuestion": "floatValue",
            "TableQuestion": "tableValue",
        }
        return value_key_map.get(question_type)

    def _handle_choice(self, question, answer, only_selected=False):
        if len(question["choiceOptions"]["edges"]) > 10 or only_selected:
            # We don't want to render more than 10 choices,
            # so we mimic a `TextQuestion`
            choice_label = None
            if answer:
                choice_label = next(
                    choice["node"]["label"]
                    for choice in question["choiceOptions"]["edges"]
                    if choice["node"]["slug"]
                    == answer["node"][
                        self.value_key_for_question(question["__typename"])
                    ]
                )

            return {
                "label": question["label"],
                "type": "TextQuestion",
                "value": choice_label,
                "info_text": strip_tags(question["infoText"]) or None,
            }

        return {
            "label": question["label"],
            "type": question["__typename"],
            "value": answer["node"][self.value_key_for_question(question["__typename"])]
            if answer
            else None,
            "options": [
                (node["node"]["slug"], node["node"]["label"])
                for node in question["choiceOptions"]["edges"]
            ],
            "info_text": strip_tags(question["infoText"]) or None,
        }

    def _handle_multiple_choice(self, question, answer):
        options = [
            (node["node"]["slug"], node["node"]["label"])
            for node in question["multipleChoiceOptions"]["edges"]
        ]
        if len(question["multipleChoiceOptions"]["edges"]) > 10:
            # We don't want to render more than 10 choices,
            # so we remove the unchecked
            options = (
                [
                    option
                    for option in options
                    if option[0]
                    in answer["node"][
                        self.value_key_for_question(question["__typename"])
                    ]
                ]
                if answer
                else []
            )

        return {
            "label": question["label"],
            "type": question["__typename"],
            "value": answer["node"][self.value_key_for_question(question["__typename"])]
            if answer
            else [],
            "options": options,
            "info_text": strip_tags(question["infoText"]) or None,
        }

    def _handle_files(self, question, answer):
        if not answer:
            return {
                "label": question["label"],
                "type": question["__typename"],
                "value": [],
                "info_text": strip_tags(question["infoText"]) or None,
            }

        filename_list = []
        for value in answer["node"][
            self.value_key_for_question(question["__typename"])
        ]:
            name = value["name"]
            if (value.get("metadata", {}) or {}).get(
                "content_type",
            ) in SUPPORTED_MERGE_CONTENT_TYPES:
                file = get_caluma_file(value["downloadUrl"])
                if file["content-type"] == "application/pdf":
                    file = file["file"]
                elif file["content-type"] in ["image/png", "image/jpeg"]:
                    file = prepare_image_file_for_pdf_merge(file)
                try:
                    self.merger.append(file)
                    self.file_count += 1
                    # On success, add attachement index to filename
                    name = f"{name} ({self.file_count})"
                except FileNotDecryptedError as e:
                    # we don't support AES encrypted PDFs
                    if (
                        not e.args or e.args[0] != "File has not been decrypted"
                    ):  # pragma: no cover
                        pass
                except PdfReadError:  # pragma: no cover
                    # faulty pdf
                    pass
                except KeyError:  # pragma: no cover
                    # PDF probably not supported by pypdf
                    pass
            filename_list.append(name)

        return {
            "label": question["label"],
            "type": question["__typename"],
            "value": filename_list,
            "info_text": strip_tags(question["infoText"]) or None,
        }

    def _handle_static(self, question):
        return {
            "label": "",  # we only want to render the staticContent
            "type": question["__typename"],
            "value": strip_tags(question["staticContent"]),
            "info_text": strip_tags(question["infoText"]) or None,
        }

    def _handle_table(self, question, answer):
        if not answer:
            return {
                "type": "TextQuestion",
                "label": question["label"],
                "value": None,
                "info_text": strip_tags(question["infoText"]) or None,
            }

        row_form_questions = question["rowForm"]["questions"]["edges"]
        rows = [
            self.format_application_data(
                question["rowForm"]["name"],
                row_form_questions,
                row["answers"]["edges"],
            )
            for row in answer["node"][
                self.value_key_for_question(question["__typename"])
            ]
        ]
        return {
            "rows": rows,
            "type": question["__typename"],
            "label": question["label"],
            "info_text": strip_tags(question["infoText"]) or None,
        }

    def _handle_waehrung(self, question, answer):
        value = answer["node"][self.value_key_for_question(question["__typename"])]

        return {
            "label": question["label"],
            "type": question["__typename"],
            "value": format_currency(value, question["meta"]["waehrung"])
            if answer
            else None,
            "info_text": strip_tags(question["infoText"]) or None,
        }

    def _handle_simple(self, question, answer):
        return {
            "label": question["label"],
            "type": question["__typename"],
            "value": answer["node"][self.value_key_for_question(question["__typename"])]
            if answer
            else None,
            "info_text": strip_tags(question["infoText"]) or None,
        }

    def _get_answer(self, question, answers):
        try:
            return next(
                answer
                for answer in answers
                if answer["node"]["question"]["slug"] == question["slug"]
            )
        except StopIteration:
            pass

    def format_application_data(self, name, questions, answers):
        type_method_map = {
            "ChoiceQuestion": self._handle_choice,
            "MultipleChoiceQuestion": self._handle_multiple_choice,
            "FilesQuestion": self._handle_files,
            "StaticQuestion": self._handle_static,
            "TableQuestion": self._handle_table,
        }

        parsed_data = {"name": name, "questions": {}}

        for question in questions:
            question = question["node"]

            # separately handle FormQuestion
            if question["__typename"] == "FormQuestion":
                if "sub_forms" not in parsed_data:
                    parsed_data["sub_forms"] = {}

                parsed_data["sub_forms"][question["subForm"]["slug"]] = (
                    self.format_application_data(
                        question["subForm"]["name"],
                        question["subForm"]["questions"]["edges"],
                        answers,
                    )
                )
                continue

            # get the correct method for this question type
            type_method = type_method_map.get(
                question["__typename"],
                self._handle_simple,
            )

            args = [question]

            # StaticQuestions need some special handling, as they do not need an answer
            # and should only be included in the PDF, if they actually contain
            # StaticContent.
            answer = None
            if (
                question["__typename"] == "StaticQuestion"
                and not question["staticContent"]
            ):
                continue

            if question["__typename"] != "StaticQuestion":
                # Questions other than StaticQuestion need their answer if there is one.
                answer = self._get_answer(question, answers)

                args.append(answer)

            if (
                answer
                and question["__typename"]
                in [
                    "IntegerQuestion",
                    "FloatQuestion",
                    "CalculatedFloatQuestion",
                ]
                and question["meta"].get("waehrung")
            ):
                type_method = self._handle_waehrung

            # now let the type method do its thing
            parsed_data["questions"][question["slug"]] = type_method(*args)

        return parsed_data

    def _get_verteilplan(self):
        if "verteilplan" not in self.data["data"]["node"]["document"] or not len(
            self.data["data"]["node"]["document"]["verteilplan"]["edges"],
        ):
            return
        verteilplan = self.data["data"]["node"]["document"]["verteilplan"]
        answer = verteilplan["edges"][0]
        question = verteilplan["edges"][0]["node"]["question"]
        return self._handle_choice(question, answer, only_selected=True)

    @property
    def dossier_nr(self):
        return self.data["data"]["node"]["document"]["dossier_nr"]["edges"][0]["node"][
            "value"
        ]

    def _get_dossier_nr(self):
        trans_map = {
            "de": "Referenznummer",
            "en": "Reference No.",
            "fr": "N° de référence",
        }

        title = trans_map[get_language()]
        return f"{title}: {self.dossier_nr}"

    def run(self):
        self.file_count = 0
        self.parsed_data = self.format_application_data(
            self.data["data"]["node"]["document"]["form"]["name"],
            self.data["data"]["node"]["document"]["form"]["questions"]["edges"],
            self.data["data"]["node"]["document"]["answers"]["edges"],
        )

        self.parsed_data["dossier_nr"] = self._get_dossier_nr()

        vp = self._get_verteilplan()
        if vp:
            self.parsed_data["questions"]["verteilplan-nr"] = vp
        return self.parsed_data


def generate_pdf(parser, append_to=None):
    """
    Generate a PDF from the parser data.

    This helper function takes a DocumentParser instance and generates a PDF file
    containing the whole document, followed by all render-able attachments.
    Optionally, a PDF can be supplied (`append_to`), that will be put at the top of the
    resulting PDF.
    """

    def merge_files_to_pdf(pdf):
        parser.merger.merge(0, pdf)
        if append_to:
            # for the accounting export, we also have a cover sheet, that needs to
            # be on the first page of the resulting export. If provided, merge it to
            # index 0
            parser.merger.merge(0, append_to)

        # Write result PDF
        result = io.BytesIO()
        parser.merger.write(result)
        parser.merger.close()

        result.seek(0)
        return result

    # Generate PDF from document data
    dms_client = DMSClient()
    dms_document_response = dms_client.get_merged_document(
        parser.parsed_data,
        settings.DOCUMENT_MERGE_SERVICE_APPLICATION_EXPORT_SLUG,
        convert="pdf",
    )

    if dms_document_response.status_code != status.HTTP_200_OK:
        raise DMSException(dms_document_response)

    # Then we merge the attachments to the newly generated PDF
    return merge_files_to_pdf(io.BytesIO(dms_document_response.content))
