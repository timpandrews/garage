# Generated by Django 4.1.5 on 2023-03-22 04:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("garage", "0007_profile_profile_pic_profile_strava_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_pic",
            field=models.ImageField(
                default="profile_pics/default.jpg", upload_to="profile_pics"
            ),
        ),
    ]
