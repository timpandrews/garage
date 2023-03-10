# Generated by Django 4.1.5 on 2023-03-13 15:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("garage", "0004_zwiftroutelist"),
    ]

    operations = [
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
                ],
                max_length=200,
            ),
        ),
    ]
