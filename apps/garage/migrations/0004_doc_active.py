# Generated by Django 4.1.5 on 2023-02-16 15:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("garage", "0003_alter_doc_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="doc",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]
