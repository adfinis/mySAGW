from django.utils.html import strip_tags
from django.utils.translation import get_language

from mysagw.pdf_utils import SUPPORTED_MERGE_CONTENT_TYPES
from mysagw.utils import format_currency


class ApplicationParser:
    def __init__(self, data):
        self.data = data
        self.parsed_data = None
        self.files_to_add = []

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
                "content_type"
            ) in SUPPORTED_MERGE_CONTENT_TYPES:
                self.files_to_add.append(value["downloadUrl"])
                name = f"{name} ({len(self.files_to_add)})"
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
                question["rowForm"]["name"], row_form_questions, row["answers"]["edges"]
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

                parsed_data["sub_forms"][
                    question["subForm"]["slug"]
                ] = self.format_application_data(
                    question["subForm"]["name"],
                    question["subForm"]["questions"]["edges"],
                    answers,
                )
                continue

            # get the correct method for this question type
            type_method = type_method_map.get(
                question["__typename"], self._handle_simple
            )

            args = [question]

            # StaticQuestions need some special handling, as they do not need an answer
            # and should only be included in the PDF, if they actually contain
            # StaticContent.
            if (
                question["__typename"] == "StaticQuestion"
                and not question["staticContent"]
            ):
                continue
            elif question["__typename"] != "StaticQuestion":
                # Questions other than StaticQuestion need their answer if there is one.
                answer = self._get_answer(question, answers)

                args.append(answer)

            if question["meta"].get("waehrung"):
                type_method = self._handle_waehrung

            # now let the type method to its thing
            parsed_data["questions"][question["slug"]] = type_method(*args)

        return parsed_data

    def _get_verteilplan(self):
        verteilplan = self.data["data"]["node"]["document"]["verteilplan"]
        if not len(verteilplan["edges"]):
            return
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
