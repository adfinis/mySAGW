from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.utils import timezone
from localized_fields.value import LocalizedStringValue


def test_migrate_public_localized_interests(transactional_db):  # pragma: no cover
    executor = MigrationExecutor(connection)
    migrate_from = [
        ("localized_fields", "0001_initial"),
        ("identity", "0007_organisation_types"),
    ]
    migrate_to = [
        ("identity", "0008_public_localized_interests"),
    ]

    executor.loader.build_graph()
    executor.migrate(migrate_from)

    old_apps = executor.loader.project_state(migrate_from).apps

    old_models = {
        "InterestCategory": old_apps.get_model("identity", "InterestCategory"),
        "Interest": old_apps.get_model("identity", "Interest"),
        "HistoricalInterestCategory": old_apps.get_model(
            "identity",
            "HistoricalInterestCategory",
        ),
        "HistoricalInterest": old_apps.get_model("identity", "HistoricalInterest"),
    }

    old_records = []

    cat = None
    for name, model in old_models.items():
        kwargs = {}
        if name.startswith("Historical"):
            kwargs["history_date"] = timezone.now()
        if name.endswith("Interest"):
            kwargs["category"] = cat
        record = model.objects.create(title="foo", **kwargs)
        if cat is None:
            cat = record
        old_records.append(record)

    # Migrate forwards.
    executor.loader.build_graph()  # reload.
    executor.migrate(migrate_to)

    new_apps = executor.loader.project_state(migrate_to).apps

    new_models = {
        "InterestCategory": new_apps.get_model("identity", "InterestCategory"),
        "Interest": new_apps.get_model("identity", "Interest"),
        "HistoricalInterestCategory": new_apps.get_model(
            "identity",
            "HistoricalInterestCategory",
        ),
        "HistoricalInterest": new_apps.get_model("identity", "HistoricalInterest"),
    }

    for old_record in old_records:
        new_record = new_models[old_record.__class__.__name__].objects.get(
            pk=old_record.pk,
        )
        assert isinstance(new_record.title, LocalizedStringValue)
        assert dict(new_record.title) == {"de": "foo", "en": "", "fr": ""}
