import io
from base64 import urlsafe_b64encode
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.http import FileResponse
from django.utils import timezone
from django.utils.translation import get_language
from rest_framework import status
from rest_framework.views import APIView

from mysagw.caluma_client import CalumaClient
from mysagw.caluma_document_parser import DocumentParser, generate_pdf
from mysagw.dms_client import DMSClient, get_dms_error_response
from mysagw.oidc_auth.permissions import IsAdmin, IsAuthenticated, IsStaff
from mysagw.utils import format_currency

GQL_DIR = Path(__file__).parent.resolve() / "queries"


def get_cover_context(data):  # noqa: C901
    def mitgliedinstitution_label(slug):
        for option in data["data"]["node"]["main"]["mitgliedinstitution"]["edges"][0][
            "node"
        ]["question"]["options"]["edges"]:
            if option["node"]["slug"] == slug:
                return option["node"]["label"]

    def circ_kontonummer_label(slug):
        for option in data["data"]["node"]["decisionCredit"]["edges"][0]["node"][
            "document"
        ]["circKontonummer"]["edges"][0]["node"]["question"]["options"]["edges"]:
            if option["node"]["slug"] == slug:
                return option["node"]["label"]

    fields = {
        "form": (
            [
                "data",
                "node",
                "main",
                "form",
                "name",
            ],
            None,
        ),
        "applicant_address": (
            [
                "data",
                "node",
                "additionalData",
                "edges",
                0,
                "node",
                "document",
                "applicant_address",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "applicant_postcode": (
            [
                "data",
                "node",
                "additionalData",
                "edges",
                0,
                "node",
                "document",
                "applicant_postcode",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "applicant_city": (
            [
                "data",
                "node",
                "additionalData",
                "edges",
                0,
                "node",
                "document",
                "applicant_city",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "applicant_land": (
            [
                "data",
                "node",
                "additionalData",
                "edges",
                0,
                "node",
                "document",
                "applicant_land",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "applicant_name": (
            [
                "data",
                "node",
                "additionalData",
                "edges",
                0,
                "node",
                "document",
                "applicant_name",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "bank": (
            [
                "data",
                "node",
                "additionalData",
                "edges",
                0,
                "node",
                "document",
                "bank",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "bank_town": (
            [
                "data",
                "node",
                "additionalData",
                "edges",
                0,
                "node",
                "document",
                "bank_town",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "dossier_nr": (
            [
                "data",
                "node",
                "main",
                "dossierno",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "zahlungszweck": (
            [
                "data",
                "node",
                "additionalData",
                "edges",
                0,
                "node",
                "document",
                "zahlungszweck",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "iban": (
            [
                "data",
                "node",
                "additionalData",
                "edges",
                0,
                "node",
                "document",
                "iban",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "section": (
            [
                "data",
                "node",
                "main",
                "sektion",
                "edges",
                0,
                "node",
                "value",
            ],
            lambda x: x.split("-")[1],
        ),
        "total": (
            [
                "data",
                "node",
                "defineAmount",
                "edges",
                0,
                "node",
                "document",
                "total",
                "edges",
                0,
                "node",
                "value",
            ],
            lambda x: format_currency(x, "CHF") if x else "",
        ),
        "vp_year": (
            [
                "data",
                "node",
                "main",
                "vp_year",
                "edges",
                0,
                "node",
                "stringValue",
            ],
            lambda x: x.split("-")[3],
        ),
        "mitgliedinstitution": (
            [
                "data",
                "node",
                "main",
                "mitgliedinstitution",
                "edges",
                0,
                "node",
                "value",
            ],
            mitgliedinstitution_label,
        ),
        "circ_kontonummer": (
            [
                "data",
                "node",
                "decisionCredit",
                "edges",
                0,
                "node",
                "document",
                "circKontonummer",
                "edges",
                0,
                "node",
                "value",
            ],
            circ_kontonummer_label,
        ),
        "vorschussbetrag": (
            [
                "data",
                "node",
                "advanceCredits",
                "edges",
                0,
                "node",
                "document",
                "vorschussbetrag",
                "edges",
                0,
                "node",
                "value",
            ],
            lambda x: format_currency(x, "CHF") if x else "",
        ),
        "vorschussdatum": (
            [
                "data",
                "node",
                "advanceCredits",
                "edges",
                0,
                "node",
                "document",
                "vorschussdatum",
                "edges",
                0,
                "node",
                "value",
            ],
            lambda x: timezone.datetime.fromisoformat(x).strftime("%d. %m. %Y")
            if x
            else "",
        ),
    }

    result = {}

    for field, path in fields.items():
        value = None
        for node in path[0]:
            if value is None:
                value = data[node]
                continue
            try:
                value = value[node]
            except (KeyError, TypeError, IndexError):
                value = ""
                break
        if value and path[1] is not None:
            value = path[1](value)
        result[field] = value

    return result


class ReceiptView(APIView):
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)

    def get(self, request, pk, **kwargs):
        caluma_client = CalumaClient(
            endpoint=f"{request.scheme}://{request.get_host()}/graphql",
            token=request.META.get("HTTP_AUTHORIZATION"),
            # For local testing:
            # endpoint="http://caluma:8000/graphql",
            # token="Bearer ey...",
        )

        # first we have to fetch the ID of the additional-data document,
        # if it's available
        variables = {
            "case_id": urlsafe_b64encode(f"Case:{pk}".encode()).decode("utf-8"),
        }

        raw_document_id_data = caluma_client.get_data(
            [GQL_DIR / "get_document_id.gql"],
            variables,
        )

        # check if the accounting-form document is available
        additional_data_available = True
        try:
            document_id = raw_document_id_data["data"]["node"]["additionalData"][
                "edges"
            ][0]["node"]["document"]["id"]
        except (IndexError, KeyError):
            # additional_data document is not available. Use random ID to make the
            # query go through and return empty values.
            # This is not very nice, but lets us use the same query
            document_id = str(uuid4())
            additional_data_available = False

        # now we execute the main query for the accounting document
        variables["document_id"] = document_id

        raw_data = caluma_client.get_data(
            [
                GQL_DIR / "get_receipts.gql",
                settings.COMMON_GQL_DIR / "document_fragments.gql",
            ],
            variables,
            add_headers={"Accept-Language": get_language()},
        )

        # Let's generate the cover sheet
        cover_context = get_cover_context(raw_data)
        cover_context["date"] = timezone.now().date().strftime("%d. %m. %Y")

        dms_client = DMSClient()
        dms_cover_response = dms_client.get_merged_document(
            cover_context,
            settings.DOCUMENT_MERGE_SERVICE_ACCOUNTING_COVER_TEMPLATE_SLUG,
            convert="pdf",
        )

        if dms_cover_response.status_code != status.HTTP_200_OK:
            return get_dms_error_response(dms_cover_response)

        pdf = io.BytesIO(dms_cover_response.content)

        # Only call document parser, if document is available
        if additional_data_available:
            additional_data = raw_data["data"]["node"]["additionalData"]["edges"][0][
                "node"
            ]["document"]

            # The DecumentParser only needs a subset of the data and expects it to be
            # in a specific format
            prepared_data = {
                "data": {
                    "node": {
                        "document": {
                            "dossier_nr": raw_data["data"]["node"]["main"]["dossierno"],
                            "verteilplan": raw_data["data"]["node"]["main"]["vp_year"],
                            "answers": additional_data["answers"],
                            "form": additional_data["form"],
                        },
                    },
                },
            }

            parser = DocumentParser(prepared_data)
            parser.run()
            pdf = generate_pdf(parser, append_to=io.BytesIO(dms_cover_response.content))

        dossier_nr = cover_context.get("dossier_nr", "unknown_dossier_nr")
        form_name = cover_context.get("form", "unknown_form")

        return FileResponse(
            pdf,
            content_type="application/pdf",
            filename=f"{form_name} - {dossier_nr}.pdf",
        )
