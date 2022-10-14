import io
from base64 import urlsafe_b64encode
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.forms.models import model_to_dict
from django.http import FileResponse, HttpResponse
from django.utils import formats
from requests import HTTPError
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from mysagw.accounting.caluma_client import CalumaClient
from mysagw.case import filters, models, serializers
from mysagw.case.permissions import HasCaseAccess
from mysagw.dms_client import DMSClient
from mysagw.identity.models import Address, Identity
from mysagw.oidc_auth.permissions import IsAdmin, IsAuthenticated

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

    acknowledgement_fields = {
        "identity": (["data", "node", "createdByUser"], None),
        "dossier_nr": (
            [
                "data",
                "node",
                "main",
                "dossier_nr",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
    }

    credit_approval_fields = {
        "identity": (["data", "node", "createdByUser"], None),
        "dossier_nr": (
            [
                "data",
                "node",
                "main",
                "dossier_nr",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
        "rahmenkredit": (
            [
                "data",
                "node",
                "decisionAndCredit",
                "credit",
                "edges",
                0,
                "node",
                "value",
            ],
            None,
        ),
    }

    def get_data(self, case_id, request, name):
        with (GQL_DIR / f"get_{name}.gql").open("r") as f:
            query = f.read()
        global_id = urlsafe_b64encode(f"Case:{case_id}".encode("utf-8")).decode("utf-8")
        client = CalumaClient(
            endpoint=f"{request.scheme}://{request.get_host()}/graphql",
            token=request.META.get("HTTP_AUTHORIZATION"),
            # For local testing:
            # endpoint="http://caluma:8000/graphql",
            # token="Bearer ey...",
        )
        variables = {"case_id": global_id}
        resp = client.execute(query, variables)
        return resp

    def get_formatted_data(self, data, name):
        result = {}

        for field, path in getattr(self, f"{name}_fields").items():
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

            if field == "identity":
                identity = Identity.objects.get(idp_id=value)
                address = model_to_dict(
                    Address.objects.get(identity=identity, default=True)
                )
                identity = model_to_dict(identity)

                # remove objects which cannot be turned into json
                del address["identity"]
                del address["country"]
                del identity["interests"]

                identity["address"] = address
                value = identity

            result[field] = value

        result["date"] = formats.date_format(datetime.now())
        return result

    def get_merged_document(self, request, data, name):
        document = io.BytesIO()
        client = DMSClient()
        # add identity data to data
        # use different dms template based on case submitter identity language
        try:
            resp = client.merge(
                f'{getattr(settings, f"DOCUMENT_MERGE_SERVICE_{name.upper()}_TEMPLATE_SLUG")}-{data["identity"]["language"]}',
                data=data,
                convert="pdf",
            )
            document.write(resp.content)
            document.seek(0)

            return FileResponse(
                document,
                content_type="application/pdf",
                filename=f"{data.get('dossier_no')}.pdf",
            )
        except HTTPError as e:
            return HttpResponse(
                e.response.content,
                status=e.response.status_code,
                content_type=e.response.headers["Content-Type"],
            )

    @action(detail=True)
    def application(self, request, pk=None):
        pass
        """
        name = "application"
        # prepare all answers for dms
        response = self.get_merged_document(data, name)

        return response
        """

    @action(detail=True)
    def acknowledgement(self, request, pk=None):
        name = "acknowledgement"
        raw_data = self.get_data(pk, request, name)
        data = self.get_formatted_data(raw_data, name)
        response = self.get_merged_document(request, data, name)

        return response

    @action(detail=True)
    def credit_approval(self, request, pk=None):
        name = "credit_approval"
        raw_data = self.get_data(pk, request, name)
        data = self.get_formatted_data(raw_data, name)
        response = self.get_merged_document(request, data, name)

        return response
