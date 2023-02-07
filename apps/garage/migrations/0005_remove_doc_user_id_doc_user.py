# Generated by Django 4.1.5 on 2023-02-06 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("garage", "0004_rename_title_doc_data_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doc",
            name="user_id",
        ),
        migrations.AddField(
            model_name="doc",
            name="user",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
