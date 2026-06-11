import re
import sys
from io import StringIO

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


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

        caluma_apps = [
            "caluma_core",
            "caluma_user",
            "caluma_form",
            "caluma_workflow",
            "caluma_logging",
            "caluma_data_source",
            "caluma_analytics",
        ]

        self.stdout.write(self.style.WARNING(f"🚀 Starting import from {dump_file}..."))

        # 1. Load the data using standard loaddata by passing the path string directly
        try:
            call_command("loaddata", dump_file, database="default")
            self.stdout.write(
                self.style.SUCCESS("✅ Data successfully loaded into default DB.")
            )
        except Exception as e:  # noqa: BLE001
            self.stdout.write(self.style.ERROR(f"❌ Failed to load data: {e}"))
            sys.exit(1)

        # 2. Automatically fix primary key sequences (Crucial for PostgreSQL if sequence fields exist)
        self.stdout.write(self.style.NOTICE("🔄 Resetting database sequences..."))
        try:
            output = StringIO()

            # Force no_color=True to avoid ANSI escapes entirely
            call_command("sqlsequencereset", *caluma_apps, stdout=output, no_color=True)
            raw_sql = output.getvalue()

            if raw_sql.strip():
                # Regular expression to remove any rogue ANSI escape codes if they still appear
                ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
                clean_sql = ansi_escape.sub("", raw_sql)

                # Split statements cleanly by semicolon now that color blocks are gone
                statements = [
                    stmt.strip()
                    for stmt in clean_sql.split(";")
                    if stmt.strip() and stmt.strip() not in ("BEGIN", "COMMIT")
                ]

                if statements:
                    with connection.cursor() as cursor:
                        for statement in statements:
                            cursor.execute(statement)
                    self.stdout.write(
                        self.style.SUCCESS(
                            "✅ Database sequences successfully updated."
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            "✅ No active sequence modifications needed."
                        )
                    )
            else:
                self.stdout.write(self.style.SUCCESS("✅ No sequences found to reset."))

        except Exception as e:  # noqa: BLE001
            self.stdout.write(
                self.style.ERROR(f"⚠️ Failed to process sequence adjustment: {e}")
            )
