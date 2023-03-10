# Generated by Django 4.1.5 on 2023-03-13 23:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("garage", "0005_alter_zwiftroutelist_world_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="doc",
            name="fit_data",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="doc",
            name="gpx_data",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="doc",
            name="data",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="zwiftroutelist",
            name="world_name",
            field=models.CharField(
                choices=[
                    ("Watopia", "Watopia"),
                    ("Richmond", "Richmond"),
                    ("Lodon", "London"),
                    ("New York", "New York"),
                    ("Innsbruck", "Innsbruck"),
                    ("Bologna TT", "Bologna TT"),
                    ("Yorkshire", "Yorkshire"),
                    ("Crit City", "Crit City"),
                    ("Makuri Islands", "Makuri Islands"),
                    ("France", "France"),
                    ("Paris", "Paris"),
                    ("Scotland", "Scotland"),
                    ("Gravel Mountain", "Gravel Mountain"),
                ],
                max_length=200,
            ),
        ),
    ]
