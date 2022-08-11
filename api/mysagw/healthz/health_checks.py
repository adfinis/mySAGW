from io import StringIO

from django.conf import settings
from django.core import management
from watchman.decorators import check

from mysagw.identity.models import Identity


@check
def _check_pending_migrations(db_name):
    """Check database for pending migrations.

    Returns JSON mapping if no pending migrations, otherwise raises Exception.
    @check django-watchman decorator catches and handles exceptions.
    """
    # check for unapplied migrations
    out = StringIO()
    management.call_command("showmigrations", "--plan", stdout=out)
    plan = out.getvalue()
    if "[ ]" in plan:
        raise Exception("Database has unapplied migrations (migrate).")

    return {db_name: {"ok": True}}


@check
def _check_models(database):
    """Check model fetching on database."""
    # Retrieve object
    identity = Identity.objects.get(email="sagw@sagw.ch", is_organisation=True)
    assert identity

    return {database: {"ok": True}}


def check_migrations():
    """Check available databases for unapplied migrations."""
    databases = sorted(settings.DATABASES)
    checked_databases = [_check_pending_migrations(db_name) for db_name in databases]

    return {"database migrations": checked_databases}


def check_models():
    """Check model instantiation."""
    databases = sorted(settings.DATABASES)
    checked_databases = [_check_models(db_name) for db_name in databases]

    return {"database models": checked_databases}
