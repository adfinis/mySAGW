from argparse import ArgumentTypeError

from django.conf import settings
from django.core.management.base import BaseCommand
from requests import HTTPError

from mysagw.dms_client import DMSClient


class Command(BaseCommand):
    help = "Upload templates for exports"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = DMSClient()

    def template_file(self, value):
        template = settings.DOCUMENT_MERGE_SERVICE_TEMPLATE_DIR / value
        if not template.exists() or not template.is_file:
            msg = f"Template not found: {template}"
            raise ArgumentTypeError(msg)
        return template

    def add_arguments(self, parser):
        parser.add_argument(
            "templates",
            default=[
                settings.DOCUMENT_MERGE_SERVICE_TEMPLATE_DIR
                / f"{settings.DOCUMENT_MERGE_SERVICE_LABELS_TEMPLATE_SLUG}.docx"
            ],
            type=self.template_file,
            nargs="*",
        )

    def _upload_template(self, template, update=False):
        try:
            with template.open("rb") as t_file:
                resp = self.client.upload_template(
                    template.stem,
                    t_file,
                    update=update,
                )
        except HTTPError as e:
            assert (
                e.response.content
                == b'{"slug":["template with this slug already exists."]}'
            ), e.response.content
            return False

        self.stdout.write(resp.content.decode())
        return True

    def handle(self, *args, **options):
        templates = options.get("templates")
        for template in templates:
            if self._upload_template(template) is False:
                assert self._upload_template(template, update=True) is True
