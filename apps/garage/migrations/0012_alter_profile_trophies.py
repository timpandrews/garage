# Generated by Django 4.1.5 on 2023-03-04 20:12

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):
    dependencies = [
        ("garage", "0011_alter_profile_trophies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="trophies",
            field=django_quill.fields.QuillField(blank=True, null=True),
        ),
    ]
