import io
from base64 import urlsafe_b64encode
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.db.models import Exists, OuterRef, Q, Subquery
from django.http import FileResponse
from django.utils import formats, timezone
from django.utils.translation import get_language
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from mysagw.caluma_client import CalumaClient
from mysagw.caluma_document_parser import DMSException, DocumentParser, generate_pdf
from mysagw.case import filters, models, serializers
from mysagw.case.permissions import HasCaseAccess
from mysagw.dms_client import DMSClient, get_dms_error_response
from mysagw.identity.models import Identity, Membership
from mysagw.oidc_auth.permissions import IsAdmin, IsAuthenticated, IsStaff
from mysagw.utils import format_currency

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
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | HasCaseAccess),)

    def list(self, request, *args, **kwargs):
        expected_keys = ["filter[idpId]", "filter[caseIds]", "filter[idpIds]"]
        if not request.GET or set(expected_keys).isdisjoint(request.GET.keys()):
            msg = f"At least one of following filters must be used: {', '.join(expected_keys)}"
            raise ValidationError(
                msg,
            )
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if models.CaseAccess.objects.filter(case_id=instance.case_id).count() == 1:
            msg = "This is the only CaseAccess for this case, hence it cannot be destroyed."
            raise ValidationError(msg)
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_staff:
            return qs
        return qs.filter(
            case_id__in=qs.filter(identity=self.request.user.identity).values(
                "case_id",
            ),
        )

    @action(
        methods=["post"],
        detail=False,
        serializer_class=serializers.CaseTransferSerializer,
        permission_classes=(IsAuthenticated & (IsAdmin | IsStaff),),
        parser_classes=(JSONParser,),
    )
    @transaction.atomic
    def transfer(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()
        return Response({"created": len(instances)}, status=status.HTTP_201_CREATED)


class CaseDownloadViewSet(GenericViewSet):
    serializer_class = BaseSerializer
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff | HasCaseAccess),)

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

    def get_identity(self, graphql_value, case_id):
        """
        Get correct identity for the address on the downloads.

        The identity is chosen by following priorities:

        1. Use the identity that submitted the main document
        2. If it doesn't exist anymore, use the identity, which has had access for the
        longest time and does not belong to SAGW
        3. If there is no such identity, use the one, which has had access for the
        longest time, even if they are in the SAGW organisation
        """
        try:
            # get and return identity, which has submitted the main doc
            return Identity.objects.get(idp_id=graphql_value)
        except Identity.DoesNotExist:
            pass

        # the identity doesn't exist. Annotate CaseAccesses for this case with
        # history_date of adding the access and order by it. Additionally also annotate
        # the QuerySet with `is_staff` containing the information, if the CaseAccess
        # belongs to a staff member
        created_at_subquery = models.CaseAccess.history.filter(
            id=OuterRef("pk"), history_type="+"
        ).order_by("history_date")
        staff_organisation_subquery = Membership.objects.filter(
            Q(identity_id=OuterRef("identity_id")),
            Q(inactive=False),
            Q(time_slot__isnull=True) | Q(time_slot__contains=timezone.now()),
            Q(organisation__organisation_name=settings.STAFF_ORGANISATION_NAME),
        )
        accesses = (
            models.CaseAccess.objects.filter(case_id=case_id)
            .annotate(
                created_at=Subquery(created_at_subquery.values("history_date")[:1]),
                is_staff=Exists(staff_organisation_subquery),
            )
            .order_by("created_at")
        )

        # use the oldest access
        identity = accesses.first().identity
        if non_sagw_access := accesses.exclude(is_staff=True).first():
            # if there are accesses belonging to an external users, use the oldest
            identity = non_sagw_access.identity

        return identity

    def get_formatted_data(self, data, name, case_id):
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

            if field == "rahmenkredit":
                value = format_currency(value, "CHF")

            result[field] = value

        # Identity has two possible sources
        identity = self.get_identity(
            result.pop("identity_revise") or result.pop("identity_submit"), case_id
        )
        result["identity"] = {
            "address_block": identity.address_block,
            "greeting_salutation_and_name": identity.greeting_salutation_and_name(),
            "email": identity.email,
        }

        result["date"] = formats.date_format(timezone.now())
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

        # first we get the document-ID from the main-form document. this is needed
        # in the main query for applying the visibilities
        variables = {
            "case_id": urlsafe_b64encode(f"Case:{pk}".encode()).decode("utf-8"),
        }
        raw_document_id_data = caluma_client.get_data(
            [GQL_DIR / "get_document_id.gql"],
            variables,
        )
        document_id = raw_document_id_data["data"]["node"]["document"]["id"]

        # now we execute the main query for the accounting document
        variables["document_id"] = document_id
        language = get_language()
        raw_data = caluma_client.get_data(
            [
                GQL_DIR / "get_document.gql",
                settings.COMMON_GQL_DIR / "document_fragments.gql",
            ],
            variables,
            add_headers={"Accept-Language": language},
        )
        parser = DocumentParser(raw_data)
        parser.run()

        # Let's generate the PDF
        try:
            pdf = generate_pdf(parser)
        except DMSException as e:
            return get_dms_error_response(e.response)

        return FileResponse(
            pdf,
            filename=(
                f"{parser.dossier_nr} - "
                f"{self.get_filename_translation('application', language)}.pdf"
            ),
        )

    def get_acknowledgement_and_credit_approval(self, request, name, pk=None):
        caluma_client = self.get_caluma_client(request)
        variables = {
            "case_id": urlsafe_b64encode(f"Case:{pk}".encode()).decode("utf-8"),
        }
        raw_data = caluma_client.get_data([GQL_DIR / f"get_{name}.gql"], variables)
        data = self.get_formatted_data(raw_data, name, pk)
        language = get_language()
        template = f"{getattr(settings, f'DOCUMENT_MERGE_SERVICE_{name.upper()}_TEMPLATE_SLUG')}-{language}"
        file_name = (
            f"{data['dossier_nr']} - "
            f"{self.get_filename_translation(name, language)}.pdf"
        )
        dms_client = DMSClient()
        dms_response = dms_client.get_merged_document(data, template, convert="pdf")

        if dms_response.status_code != status.HTTP_200_OK:
            return get_dms_error_response(dms_response)

        return FileResponse(
            io.BytesIO(dms_response.content),
            filename=file_name,
        )

    @action(detail=True)
    def acknowledgement(self, request, pk=None):
        return self.get_acknowledgement_and_credit_approval(
            request,
            "acknowledgement",
            pk,
        )

    @action(detail=True)
    def credit_approval(self, request, pk=None):
        return self.get_acknowledgement_and_credit_approval(
            request,
            "credit_approval",
            pk,
        )
