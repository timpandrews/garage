# Generated by Django 4.1.5 on 2023-03-22 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("garage", "0008_alter_profile_profile_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_pic",
            field=models.ImageField(default="default.jpg", upload_to="profile_pics"),
        ),
    ]
