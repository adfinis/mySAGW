from pathlib import Path

import pytest
from django.core.management import call_command


@pytest.fixture
def caluma_data(db):
    call_command("loaddata", Path.cwd() / "caluma" / "data" / "form-config.json")
    call_command("loaddata", Path.cwd() / "caluma" / "data" / "workflow-config.json")
