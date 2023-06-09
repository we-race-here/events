# Generated by Django 4.1.8 on 2023-04-26 18:03

import apps.event.models
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("blurb", models.TextField(blank=True, max_length=500, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=300, null=True)),
                ("country", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(blank=True, max_length=255, null=True)),
                ("state", models.CharField(blank=True, max_length=255, null=True)),
                ("website", models.URLField(blank=True, max_length=500, null=True)),
                ("registration_website", models.URLField(blank=True, max_length=500, null=True)),
                (
                    "logo",
                    models.ImageField(blank=True, null=True, upload_to=apps.event.models.event_logo_file_path_func),
                ),
                (
                    "hero",
                    models.ImageField(blank=True, null=True, upload_to=apps.event.models.event_hero_file_path_func),
                ),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=50
                    ),
                ),
                ("panels", models.JSONField(blank=True, null=True)),
                ("location_lat", models.FloatField(blank=True, null=True)),
                ("location_lon", models.FloatField(blank=True, null=True)),
                ("permit_no", models.CharField(blank=True, max_length=25, null=True)),
                ("is_usac_permitted", models.BooleanField(default=False)),
                ("featured_event", models.BooleanField(default=False)),
                ("approved", models.BooleanField(default=False, null=True)),
                (
                    "publish_type",
                    models.CharField(
                        choices=[("public", "Public"), ("org_public", "Org Public"), ("org_private", "Org Private")],
                        max_length=32,
                        null=True,
                    ),
                ),
                ("create_datetime", models.DateTimeField(auto_now_add=True)),
                ("update_datetime", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="EventAttachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to=apps.event.models.event_attachment_file_path_func)),
                ("file_name", models.CharField(max_length=256)),
                ("title", models.CharField(blank=True, max_length=256, null=True)),
                ("create_datetime", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalEvent",
            fields=[
                ("id", models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("blurb", models.TextField(blank=True, max_length=500, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=300, null=True)),
                ("country", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(blank=True, max_length=255, null=True)),
                ("state", models.CharField(blank=True, max_length=255, null=True)),
                ("website", models.URLField(blank=True, max_length=500, null=True)),
                ("registration_website", models.URLField(blank=True, max_length=500, null=True)),
                ("logo", models.TextField(blank=True, max_length=100, null=True)),
                ("hero", models.TextField(blank=True, max_length=100, null=True)),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=50
                    ),
                ),
                ("panels", models.JSONField(blank=True, null=True)),
                ("location_lat", models.FloatField(blank=True, null=True)),
                ("location_lon", models.FloatField(blank=True, null=True)),
                ("permit_no", models.CharField(blank=True, max_length=25, null=True)),
                ("is_usac_permitted", models.BooleanField(default=False)),
                ("featured_event", models.BooleanField(default=False)),
                ("approved", models.BooleanField(default=False, null=True)),
                (
                    "publish_type",
                    models.CharField(
                        choices=[("public", "Public"), ("org_public", "Org Public"), ("org_private", "Org Private")],
                        max_length=32,
                        null=True,
                    ),
                ),
                ("create_datetime", models.DateTimeField(blank=True, editable=False)),
                ("update_datetime", models.DateTimeField(blank=True, editable=False)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")], max_length=1),
                ),
            ],
            options={
                "verbose_name": "historical event",
                "verbose_name_plural": "historical events",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalEventAttachment",
            fields=[
                ("id", models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name="ID")),
                ("file", models.TextField(max_length=100)),
                ("file_name", models.CharField(max_length=256)),
                ("title", models.CharField(blank=True, max_length=256, null=True)),
                ("create_datetime", models.DateTimeField(blank=True, editable=False)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")], max_length=1),
                ),
            ],
            options={
                "verbose_name": "historical event attachment",
                "verbose_name_plural": "historical event attachments",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalRace",
            fields=[
                ("id", models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name="ID")),
                ("name", models.CharField(max_length=256)),
                ("start_date", models.DateField(null=True)),
                ("start_time", models.TimeField(blank=True, null=True)),
                (
                    "categories",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100), null=True, size=50
                    ),
                ),
                ("create_datetime", models.DateTimeField(blank=True, editable=False)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")], max_length=1),
                ),
            ],
            options={
                "verbose_name": "historical race",
                "verbose_name_plural": "historical races",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalRaceResult",
            fields=[
                ("id", models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name="ID")),
                ("name", models.CharField(max_length=256, null=True)),
                ("place", models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)])),
                (
                    "finish_status",
                    models.CharField(
                        choices=[("ok", "OK"), ("dns", "DNS"), ("dnf", "DNF")], default="ok", max_length=16
                    ),
                ),
                ("category", models.CharField(max_length=32, null=True)),
                ("time", models.CharField(blank=True, max_length=32, null=True)),
                ("gap", models.CharField(blank=True, max_length=32, null=True)),
                ("bib_number", models.CharField(blank=True, max_length=32, null=True)),
                ("usac_license", models.CharField(blank=True, max_length=32, null=True)),
                ("club", models.CharField(blank=True, max_length=256, null=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("more_data", models.JSONField(blank=True, null=True)),
                ("create_datetime", models.DateTimeField(blank=True, editable=False)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")], max_length=1),
                ),
            ],
            options={
                "verbose_name": "historical race result",
                "verbose_name_plural": "historical race results",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalRaceSeries",
            fields=[
                ("id", models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name="ID")),
                ("name", models.CharField(max_length=256)),
                (
                    "categories",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100), null=True, size=50
                    ),
                ),
                ("points_map", models.JSONField(blank=True, null=True)),
                ("create_datetime", models.DateTimeField(blank=True, editable=False)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")], max_length=1),
                ),
            ],
            options={
                "verbose_name": "historical race series",
                "verbose_name_plural": "historical race seriess",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="Race",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256)),
                ("start_date", models.DateField(null=True)),
                ("start_time", models.TimeField(blank=True, null=True)),
                (
                    "categories",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100), null=True, size=50
                    ),
                ),
                ("create_datetime", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="RaceResult",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256, null=True)),
                ("place", models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)])),
                (
                    "finish_status",
                    models.CharField(
                        choices=[("ok", "OK"), ("dns", "DNS"), ("dnf", "DNF")], default="ok", max_length=16
                    ),
                ),
                ("category", models.CharField(max_length=32, null=True)),
                ("time", models.CharField(blank=True, max_length=32, null=True)),
                ("gap", models.CharField(blank=True, max_length=32, null=True)),
                ("bib_number", models.CharField(blank=True, max_length=32, null=True)),
                ("usac_license", models.CharField(blank=True, max_length=32, null=True)),
                ("club", models.CharField(blank=True, max_length=256, null=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("more_data", models.JSONField(blank=True, null=True)),
                ("create_datetime", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="RaceSeries",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256)),
                (
                    "categories",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100), null=True, size=50
                    ),
                ),
                ("points_map", models.JSONField(blank=True, null=True)),
                ("create_datetime", models.DateTimeField(auto_now_add=True)),
                ("events", models.ManyToManyField(related_name="race_series", to="event.event")),
            ],
        ),
    ]
