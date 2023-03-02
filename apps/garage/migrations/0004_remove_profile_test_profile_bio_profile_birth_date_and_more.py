# Generated by Django 4.1.5 on 2023-03-01 19:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("garage", "0003_profile_test"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="test",
        ),
        migrations.AddField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="profile",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="location",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
