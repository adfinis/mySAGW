import io

import pytest
from django.conf import settings
from django.core.management import CommandError, call_command
from rest_framework import status

from mysagw.utils import build_url


@pytest.mark.parametrize(
    "args,success",
    [
        ([], True),
        (["-t", "identity-labels.docx"], True),
        (["-t", "no-existing-template.docx"], False),
    ],
)
def test_upload_labels_template_command(requests_mock, args, success):
    def do_assertions(m):
        assert m.called_once
        assert (
            settings.DOCUMENT_MERGE_SERVICE_LABELS_TEMPLATE_SLUG.encode("utf-8")
            in m.last_request.body
        )

    template_url = build_url(
        settings.DOCUMENT_MERGE_SERVICE_URL,
        "template",
        trailing=True,
    )

    mock_upload = requests_mock.post(
        template_url,
        status_code=status.HTTP_400_BAD_REQUEST,
        body=io.BytesIO(b'{"slug":["template with this slug already exists."]}'),
    )

    mock_update = requests_mock.patch(
        build_url(
            template_url,
            settings.DOCUMENT_MERGE_SERVICE_LABELS_TEMPLATE_SLUG,
            trailing=True,
        ),
        status_code=status.HTTP_200_OK,
    )

    if success:
        call_command("upload_template", *args)
        do_assertions(mock_upload)
        do_assertions(mock_update)
    else:
        with pytest.raises(CommandError) as e:
            call_command("upload_template", *args)
        assert e.value.args[0].startswith(
            "Error: argument -t/--template: Template not found:",
        )
