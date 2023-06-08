import io

import requests
from pypdf import PdfWriter
from pypdf.errors import DependencyError, PdfReadError
from reportlab.lib.pagesizes import A4, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

SUPPORTED_MERGE_CONTENT_TYPES = ["application/pdf", "image/png", "image/jpeg"]


def get_caluma_file(url):
    file = io.BytesIO()
    resp = requests.get(url, verify=False)
    file.write(resp.content)
    return {"file": file, "content-type": resp.headers.get("content-type")}


def prepare_files_for_merge(files):
    document_width, document_height = A4
    printable_document_width, printable_document_height = (203 * mm, 289 * mm)
    document_width_diff = document_width - printable_document_width
    document_height_diff = document_height - printable_document_height
    for file in files:
        if file["content-type"] == "application/pdf":
            yield file["file"]
        elif file["content-type"] in ["image/png", "image/jpeg"]:
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
            yield page


def add_caluma_files_to_pdf(pdf, urls):
    files = [get_caluma_file(url) for url in urls]

    merger = PdfWriter()
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
