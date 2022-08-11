import pytest
from django.core import management


@pytest.fixture
def roll_back_migrations():
    """Roll back database migrations to ensure unapplied migrations exist."""
    # undo applied migrations for app contenttypes
    management.call_command("migrate", "contenttypes", "zero")
    try:
        yield
    finally:
        # re-apply migrations for app contenttypes
        management.call_command("migrate", "contenttypes")
