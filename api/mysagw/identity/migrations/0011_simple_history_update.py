# Generated by Django 3.2.14 on 2022-09-01 13:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("identity", "0010_auto_20220209_1306"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicaladdress",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical address",
                "verbose_name_plural": "historical addresss",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalemail",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical email",
                "verbose_name_plural": "historical emails",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalidentity",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical identity",
                "verbose_name_plural": "historical identitys",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalinterest",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical interest",
                "verbose_name_plural": "historical interests",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalinterestcategory",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical interest category",
                "verbose_name_plural": "historical interest categorys",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalmembership",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical membership",
                "verbose_name_plural": "historical memberships",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalmembershiprole",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical membership role",
                "verbose_name_plural": "historical membership roles",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalphonenumber",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical phone number",
                "verbose_name_plural": "historical phone numbers",
            },
        ),
        migrations.AlterField(
            model_name="historicaladdress",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalemail",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalidentity",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalinterest",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalinterestcategory",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalmembership",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalmembershiprole",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalphonenumber",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
    ]
