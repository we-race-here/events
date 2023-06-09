# Generated by Django 4.1.8 on 2023-04-26 18:03

import apps.membership.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import simple_history.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HistoricalOrganizationMember",
            fields=[
                ("id", models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name="ID")),
                ("is_admin", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True, null=True)),
                ("start_date", models.DateField(null=True)),
                ("exp_date", models.DateField(null=True)),
                ("datetime", models.DateTimeField(blank=True, editable=False)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")], max_length=1),
                ),
            ],
            options={
                "verbose_name": "historical organization member",
                "verbose_name_plural": "historical organization members",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256, unique=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("regional", "Regional"),
                            ("club", "Club"),
                            ("advocacy_volunteer", "Advocacy, Volunteer"),
                            ("promoter", "Promoter"),
                        ],
                        max_length=32,
                    ),
                ),
                ("blurb", models.TextField(blank=True, max_length=500, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("social_media", models.JSONField(blank=True, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=50, null=True, region=None),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("address", models.CharField(blank=True, max_length=256, null=True)),
                ("country", models.CharField(blank=True, max_length=128, null=True)),
                ("city", models.CharField(blank=True, max_length=128, null=True)),
                ("state", models.CharField(blank=True, max_length=128, null=True)),
                ("zipcode", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "logo",
                    models.ImageField(
                        blank=True, null=True, upload_to=apps.membership.models.organization_logo_file_path_func
                    ),
                ),
                (
                    "hero",
                    models.ImageField(
                        blank=True, null=True, upload_to=apps.membership.models.organization_hero_file_path_func
                    ),
                ),
                ("membership_open", models.BooleanField(blank=True, default=False, null=True)),
                ("approved", models.BooleanField(default=False, null=True)),
                ("waiver_text", models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="OrganizationMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_admin", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True, null=True)),
                ("start_date", models.DateField(null=True)),
                ("exp_date", models.DateField(null=True)),
                ("datetime", models.DateTimeField(auto_now_add=True)),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="membership.organization"),
                ),
            ],
        ),
    ]
