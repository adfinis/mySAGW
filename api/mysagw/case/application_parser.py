from django.utils.html import strip_tags

from mysagw.identity.models import Identity


class ApplicationParser:
    def __init__(self, data):
        self.data = data
        self.parsed_data = None

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

    def _handle_choice(self, question, answer):
        if len(question["choiceOptions"]["edges"]) > 10:
            # We don't want to render more than 10 choices,
            # so we mimic a `TextQuestion`
            choice_label = next(
                choice["node"]["label"]
                for choice in question["choiceOptions"]["edges"]
                if choice["node"]["slug"]
                == answer["node"][self.value_key_for_question(question["__typename"])]
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
            "value": answer["node"][
                self.value_key_for_question(question["__typename"])
            ],
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
            options = [
                option
                for option in options
                if option[0]
                in answer["node"][self.value_key_for_question(question["__typename"])]
            ]

        return {
            "label": question["label"],
            "type": question["__typename"],
            "value": answer["node"][
                self.value_key_for_question(question["__typename"])
            ],
            "options": options,
            "info_text": strip_tags(question["infoText"]) or None,
        }

    def _handle_files(self, question, answer):
        return {
            "label": question["label"],
            "type": question["__typename"],
            "value": [
                value["name"]
                for value in answer["node"][
                    self.value_key_for_question(question["__typename"])
                ]
            ],
            "info_text": strip_tags(question["infoText"]) or None,
        }

    def _handle_static(self, question):
        return {
            "label": question["label"],
            "type": question["__typename"],
            "value": strip_tags(question["staticContent"]),
            "info_text": strip_tags(question["infoText"]) or None,
        }

    def _handle_table(self, question, answer):
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

    def _handle_simple(self, question, answer):
        return {
            "label": question["label"],
            "type": question["__typename"],
            "value": answer["node"][
                self.value_key_for_question(question["__typename"])
            ],
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
                # Questions other than StaticQuestion need the correct answer.
                # We only include questions with an answer.
                answer = self._get_answer(question, answers)
                if not answer:
                    continue

                args.append(answer)

            # now let the type method to its thing
            parsed_data["questions"][question["slug"]] = type_method(*args)

        return parsed_data

    def get_identity(self):
        FIELDS = {
            "identity_created": [
                "data",
                "node",
                "document",
                "createdByUser",
            ],
            "identity_submit": [
                "data",
                "node",
                "submit",
                "edges",
                0,
                "node",
                "closedByUser",
            ],
            "identity_revise": [
                "data",
                "node",
                "revise",
                "edges",
                0,
                "node",
                "closedByUser",
            ],
        }
        result = {}
        for field, path in FIELDS.items():
            value = None
            for node in path:
                if value is None:
                    value = self.data[node]
                    continue
                try:
                    value = value[node]
                except (KeyError, TypeError, IndexError):  # pragma: no cover
                    value = ""
                    break

            result[field] = value
        identity_id = result["identity_created"]
        if result["identity_submit"]:
            identity_id = result["identity_submit"]
        if result["identity_revise"]:
            identity_id = result["identity_revise"]
        return Identity.objects.get(idp_id=identity_id)

    def run(self):
        self.parsed_data = self.format_application_data(
            self.data["data"]["node"]["document"]["form"]["name"],
            self.data["data"]["node"]["document"]["form"]["questions"]["edges"],
            self.data["data"]["node"]["document"]["answers"]["edges"],
        )

        self.parsed_data["dossier_nr"] = self.data["data"]["node"]["document"][
            "dossier_nr"
        ]["edges"][0]["node"]["value"]
        return self.parsed_data
