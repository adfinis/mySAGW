import io

import requests
from PyPDF2 import PdfMerger
from PyPDF2.errors import DependencyError, PdfReadError
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def get_caluma_file(url):
    file = io.BytesIO()
    resp = requests.get(url, verify=False)
    file.write(resp.content)
    return {"file": file, "content-type": resp.headers.get("content-type")}


def prepare_files_for_merge(files):
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


def add_caluma_files_to_pdf(pdf, urls):
    files = [get_caluma_file(url) for url in urls]

    merger = PdfMerger()
    merger.append(pdf)

    for file in prepare_files_for_merge(files):
        try:
            merger.append(file)
        except PdfReadError:  # pragma: no cover
            ## faulty pdf
            pass
        except DependencyError as e:
            # we don't support AES encrypted PDFs
            if (
                not e.args
                or not e.args[0] == "PyCryptodome is required for AES algorithm"
            ):  # pragma: no cover
                raise

    result = io.BytesIO()

    merger.write(result)
    merger.close()

    result.seek(0)
    return result
