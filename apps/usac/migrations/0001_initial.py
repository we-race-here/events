# Generated by Django 4.1.8 on 2023-04-26 18:03

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UsacDownload",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("license_number", models.IntegerField(db_index=True)),
                ("first_name", models.CharField(blank=True, max_length=255, null=True)),
                ("last_name", models.CharField(blank=True, max_length=255, null=True)),
                ("birth_date", models.DateField(blank=True, null=True)),
                ("race_age", models.IntegerField(blank=True, null=True)),
                ("race_gender", models.CharField(blank=True, max_length=1, null=True)),
                ("sex", models.CharField(blank=True, max_length=1, null=True)),
                ("license_expiration", models.DateField(blank=True, null=True)),
                ("license_type", models.CharField(blank=True, max_length=32, null=True)),
                ("license_status", models.CharField(blank=True, max_length=32, null=True)),
                ("local_association", models.CharField(blank=True, max_length=255, null=True)),
                ("data", models.JSONField(blank=True, null=True)),
                ("data_hash", models.CharField(editable=False, max_length=64, unique=True)),
                ("create_datetime", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
