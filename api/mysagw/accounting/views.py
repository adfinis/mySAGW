import io
from base64 import urlsafe_b64encode
from pathlib import Path

import requests
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.utils import timezone
from PyPDF2 import PdfFileMerger
from PyPDF2.utils import PdfReadError
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from requests import HTTPError
from rest_framework import status
from rest_framework.viewsets import GenericViewSet

from mysagw.accounting.caluma_client import CalumaClient
from mysagw.dms_client import DMSClient
from mysagw.oidc_auth.permissions import IsAdmin, IsAuthenticated, IsStaff

GQL_DIR = Path(__file__).parent.resolve() / "queries"


def get_receipt_urls(data):
    try:
        rows = data["data"]["node"]["additionalData"]["edges"][0]["node"]["document"][
            "quittungen"
        ]["edges"][0]["node"]["value"]
    except (KeyError, TypeError, IndexError):
        return []

    result = []
    for row in rows:
        try:
            result.append(row["answers"]["edges"][0]["node"]["file"]["downloadUrl"])
        except (KeyError, TypeError, IndexError):
            continue
    return result


def get_cover(context):
    cover = io.BytesIO()
    client = DMSClient()
    try:
        resp = client.merge(
            settings.DOCUMENT_MERGE_SERVICE_ACCOUNTING_COVER_TEMPLATE_SLUG,
            data=context,
            convert="pdf",
        )
        cover.write(resp.content)
        cover.seek(0)
        return resp.status_code, resp.headers["Content-Type"], cover
    except HTTPError as e:
        content = client.get_error_content(e.response)
        return e.response.status_code, e.response.headers["Content-Type"], content


def get_receipt(url):
    file = io.BytesIO()
    resp = requests.get(url, verify=False)
    file.write(resp.content)
    return {"file": file, "content-type": resp.headers.get("content-type")}


def get_data(case_id, request):
    with (GQL_DIR / "get_receipts.gql").open("r") as f:
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


def get_cover_context(data):
    fields = {
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
        "dossier_no": (
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
        "fibu": (
            [
                "data",
                "node",
                "additionalData",
                "edges",
                0,
                "node",
                "document",
                "fibu",
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
            None,
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
                "value",
            ],
            lambda x: x.split("-")[3],
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


def get_files_to_merge(files):
    for file in files:
        if file["content-type"] == "application/pdf":
            yield file["file"]
        elif file["content-type"] in ["image/png", "image/jpeg"]:
            page = io.BytesIO()
            can = canvas.Canvas(page, pagesize=A4)
            image = ImageReader(file["file"])
            height = image.getSize()[1]
            x_start = 50
            y_start = 800 - height
            can.drawImage(
                image,
                x_start,
                y_start,
                preserveAspectRatio=True,
                mask="auto",
            )
            can.save()
            page.seek(0)
            yield page


class ReceiptViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated & (IsAdmin | IsStaff),)

    def retrieve(self, request, pk, **kwargs):
        raw_data = get_data(pk, request)

        cover_context = get_cover_context(raw_data)
        cover_context["date"] = timezone.now().date().strftime("%d. %m. %Y")

        receipt_urls = get_receipt_urls(raw_data)
        status_code, content_type, cover = get_cover(cover_context)

        if status_code != status.HTTP_200_OK:
            return HttpResponse(cover, status=status_code, content_type=content_type)

        files = [get_receipt(url) for url in receipt_urls]

        merger = PdfFileMerger()
        merger.append(cover)

        for file in get_files_to_merge(files):
            try:
                merger.append(file)
            except PdfReadError:
                ## faulty pdf or AES encrypted
                pass

        result = io.BytesIO()

        merger.write(result)
        merger.close()

        result.seek(0)

        response = FileResponse(
            result,
            content_type="application/pdf",
            filename=f"{cover_context.get('dossier_no', 'receipts')}.pdf",
        )

        return response
