# Generated by Django 4.1.9 on 2023-06-20 13:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0008_alter_raceseries_races"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="champion_event",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="historicalevent",
            name="champion_event",
            field=models.BooleanField(default=False),
        ),
    ]
