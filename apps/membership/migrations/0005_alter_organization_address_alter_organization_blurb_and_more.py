# Generated by Django 4.1.10 on 2023-08-19 17:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0004_alter_organization_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="address",
            field=models.CharField(blank=True, default="", max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="organization",
            name="blurb",
            field=models.TextField(blank=True, default="", max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="organization",
            name="city",
            field=models.CharField(blank=True, default="", max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="organization",
            name="country",
            field=models.CharField(blank=True, default="USA", max_length=128),
        ),
        migrations.AlterField(
            model_name="organization",
            name="description",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="organization",
            name="email",
            field=models.EmailField(blank=True, default="", max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="organization",
            name="state",
            field=models.CharField(blank=True, default="", max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="organization",
            name="waiver_text",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="organization",
            name="website",
            field=models.URLField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="organization",
            name="zipcode",
            field=models.CharField(blank=True, default="", max_length=10),
            preserve_default=False,
        ),
    ]
