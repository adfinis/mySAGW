import io
from base64 import urlsafe_b64encode
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from django.utils import formats
from django.utils.translation import get_language
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from mysagw.caluma_client import CalumaClient
from mysagw.case import filters, models, serializers
from mysagw.case.application_parser import ApplicationParser
from mysagw.case.permissions import HasCaseAccess
from mysagw.dms_client import DMSClient, get_dms_error_response
from mysagw.identity.models import Identity
from mysagw.oidc_auth.permissions import IsAdmin, IsAuthenticated
from mysagw.pdf_utils import add_caluma_files_to_pdf

GQL_DIR = Path(__file__).parent.resolve() / "queries"


class CaseAccessViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.CaseAccessSerializer
    queryset = models.CaseAccess.objects.all()
    filterset_class = filters.CaseAccessFilterSet
    permission_classes = (IsAuthenticated & (IsAdmin | HasCaseAccess),)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_admin:
            return qs
        return qs.filter(
            case_id__in=qs.filter(identity=self.request.user.identity).values("case_id")
        )


class CaseDownloadViewSet(GenericViewSet):
    serializer_class = BaseSerializer
    permission_classes = (IsAuthenticated & (IsAdmin | HasCaseAccess),)

    ACKNOWLEDGEMENT_FIELDS = {
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
        "dossier_nr": [
            "data",
            "node",
            "main",
            "dossier_nr",
            "edges",
            0,
            "node",
            "value",
        ],
    }

    CREDIT_APPROVAL_FIELDS = {
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
        "dossier_nr": [
            "data",
            "node",
            "main",
            "dossier_nr",
            "edges",
            0,
            "node",
            "value",
        ],
        "rahmenkredit": [
            "data",
            "node",
            "decisionAndCredit",
            "edges",
            0,
            "node",
            "document",
            "credit",
            "edges",
            0,
            "node",
            "value",
        ],
    }

    @staticmethod
    def get_caluma_client(request):
        return CalumaClient(
            endpoint=f"{request.scheme}://{request.get_host()}/graphql",
            token=request.META.get("HTTP_AUTHORIZATION"),
            # For local testing:
            # endpoint="http://caluma:8000/graphql",
            # token="Bearer ey...",
        )

    def get_formatted_data(self, data, name):
        result = {}

        for field, path in getattr(self, f"{name.upper()}_FIELDS").items():
            value = None
            for node in path:
                if value is None:
                    value = data[node]
                    continue
                try:
                    value = value[node]
                except (KeyError, TypeError, IndexError):
                    value = ""
                    break

            result[field] = value

        # Identity has two possible sources
        identity_id = result["identity_submit"]
        if result["identity_revise"]:
            identity_id = result["identity_revise"]

        identity = Identity.objects.get(idp_id=identity_id)
        identity_dict = {
            "address_block": identity.address_block,
            "greeting_salutation_and_name": identity.greeting_salutation_and_name(),
            "email": identity.email,
        }

        result["identity"] = identity_dict
        del result["identity_submit"]
        del result["identity_revise"]

        result["date"] = formats.date_format(datetime.now())
        return result

    @staticmethod
    def get_filename_translation(name, language):
        trans_map = {
            "application": {
                "de": "Gesuch",
                "en": "Application",
                "fr": "Requête",
            },
            "acknowledgement": {
                "de": "Eingangsbestätigung",
                "en": "Acknowledgement of receipt",
                "fr": "Accusé de réception",
            },
            "credit_approval": {
                "de": "Kreditgutsprache",
                "en": "Credit approval",
                "fr": "Accord de crédit",
            },
        }
        return trans_map[name][language]

    @action(detail=True)
    def application(self, request, pk=None):
        caluma_client = self.get_caluma_client(request)
        variables = {
            "case_id": urlsafe_b64encode(f"Case:{pk}".encode("utf-8")).decode("utf-8"),
        }
        raw_document_id_data = caluma_client.get_data(
            GQL_DIR / "get_document_id.gql", variables
        )
        document_id = raw_document_id_data["data"]["node"]["document"]["id"]
        variables["document_id"] = document_id
        language = get_language()
        raw_data = caluma_client.get_data(
            GQL_DIR / "get_document.gql",
            variables,
            add_headers={"Accept-Language": language},
        )
        parser = ApplicationParser(raw_data)
        data = parser.run()

        dms_client = DMSClient()
        dms_response = dms_client.get_merged_document(
            data,
            settings.DOCUMENT_MERGE_SERVICE_APPLICATION_EXPORT_SLUG,
        )

        if dms_response.status_code != status.HTTP_200_OK:
            return get_dms_error_response(dms_response)

        result = add_caluma_files_to_pdf(
            io.BytesIO(dms_response.content), parser.files_to_add
        )

        return FileResponse(
            result,
            filename=(
                f"{parser.dossier_nr} - "
                f"{self.get_filename_translation('application', language)}.pdf"
            ),
        )

    def get_acknowledgement_and_credit_approval(self, request, name, pk=None):
        caluma_client = self.get_caluma_client(request)
        variables = {
            "case_id": urlsafe_b64encode(f"Case:{pk}".encode("utf-8")).decode("utf-8")
        }
        raw_data = caluma_client.get_data(GQL_DIR / f"get_{name}.gql", variables)
        data = self.get_formatted_data(raw_data, name)
        language = get_language()
        template = f'{getattr(settings, f"DOCUMENT_MERGE_SERVICE_{name.upper()}_TEMPLATE_SLUG")}-{language}'
        file_name = (
            f"{data['dossier_nr']} - "
            f"{self.get_filename_translation(name, language)}.pdf"
        )
        dms_client = DMSClient()
        dms_response = dms_client.get_merged_document(
            data,
            template,
        )

        if dms_response.status_code != status.HTTP_200_OK:
            return get_dms_error_response(dms_response)

        return FileResponse(
            io.BytesIO(dms_response.content),
            filename=file_name,
        )

    @action(detail=True)
    def acknowledgement(self, request, pk=None):
        return self.get_acknowledgement_and_credit_approval(
            request, "acknowledgement", pk
        )

    @action(detail=True)
    def credit_approval(self, request, pk=None):
        return self.get_acknowledgement_and_credit_approval(
            request, "credit_approval", pk
        )
