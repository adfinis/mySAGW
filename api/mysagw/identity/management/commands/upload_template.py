from argparse import ArgumentTypeError
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from requests import HTTPError

from mysagw.dms_client import DMSClient


class Command(BaseCommand):
    help = "Upload template for exports"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = DMSClient()

    def template_file(self, value):
        template = Path(value)
        if not template.exists() or not template.is_file:
            msg = f"Template not found: {template}"
            raise ArgumentTypeError(msg)
        return template

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--template",
            default=Path(__file__).parent.parent.parent.absolute()
            / "templates"
            / f"{settings.DOCUMENT_MERGE_SERVICE_LABELS_TEMPLATE_SLUG}.docx",
            type=self.template_file,
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
        template = options.get("template")
        if self._upload_template(template) is False:
            assert self._upload_template(template, update=True) is True
