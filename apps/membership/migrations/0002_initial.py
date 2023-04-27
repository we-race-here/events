# Generated by Django 4.1.8 on 2023-04-26 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("membership", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="organizationmember",
            name="user",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="organization",
            name="user",
            field=models.ManyToManyField(
                related_name="organizations", through="membership.OrganizationMember", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="historicalorganizationmember",
            name="history_user",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="historicalorganizationmember",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="membership.organization",
            ),
        ),
        migrations.AddField(
            model_name="historicalorganizationmember",
            name="user",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="organizationmember",
            unique_together={("organization", "user")},
        ),
    ]