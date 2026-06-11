import sys
from io import StringIO

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import DatabaseError, connection


class Command(BaseCommand):  # pragma: no cover
    help = "Imports an external Caluma JSON dump and resets database sequences."

    def add_arguments(self, parser):
        parser.add_argument(
            "dump_file",
            type=str,
            help="Path to the caluma_export.json file",
        )

    def handle(self, *args, **options):
        dump_file = options["dump_file"]

        self.stdout.write(self.style.WARNING(f"🚀 Starting import from {dump_file}..."))

        # 1. Load the data using standard loaddata by passing the path string directly
        out = StringIO()
        err = StringIO()
        try:
            call_command(
                "loaddata",
                dump_file,
                database="default",
                stdout=out,
                stderr=err,
                verbosity=2,  # Level 2 or 3 prints exactly what object it's processing
            )
            self.stdout.write("--- LOADDATA STDOUT ---")
            self.stdout.write(out.getvalue())
            self.stdout.write(
                self.style.SUCCESS("✅ Data successfully loaded into default DB.")
            )
        except DatabaseError as db_err:
            self.stderr.write(f"❌ Database error caught during import: {db_err}")
            sys.exit(1)
        except Exception as e:  # noqa: BLE001
            self.stderr.write(f"❌ Unexpected runtime crash: {e}")
            sys.exit(1)
        finally:
            # Check if there were any hidden warnings or errors written to stderr
            stderr_output = err.getvalue()
            if stderr_output:
                self.stderr.write("--- LOADDATA STDERR ---")
                self.stderr.write(stderr_output)

        # 2. Automatically fix primary key sequences (Crucial for PostgreSQL if sequence fields exist)
        self.stdout.write(self.style.NOTICE("🔄 Resetting database sequences..."))
        # Locally generated SQL to reset all the caluma sequences
        sequencereset_sql = """\
BEGIN;
SELECT setval(pg_get_serial_sequence('"caluma_workflow_workflow_start_tasks"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "caluma_workflow_workflow_start_tasks";
SELECT setval(pg_get_serial_sequence('"caluma_workflow_workflow_allow_forms"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "caluma_workflow_workflow_allow_forms";
SELECT setval(pg_get_serial_sequence('"caluma_logging_accesslog"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "caluma_logging_accesslog";
COMMIT;
"""

        try:
            with connection.cursor() as cursor:
                self.stdout.write(f"Running:\n{sequencereset_sql}")
                cursor.execute(sequencereset_sql)
            self.stdout.write(
                self.style.SUCCESS("✅ Database sequences successfully updated.")
            )
        except Exception as e:  # noqa: BLE001
            self.stdout.write(
                self.style.ERROR(f"⚠️ Failed to process sequence adjustment: {e}")
            )
