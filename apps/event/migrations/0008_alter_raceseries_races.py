# Generated by Django 4.1.9 on 2023-06-20 11:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0007_alter_raceseries_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="raceseries",
            name="races",
            field=models.ManyToManyField(blank=True, related_name="race_series", to="event.race"),
        ),
    ]
