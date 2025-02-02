# Generated by Django 5.0 on 2024-01-11 12:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_panel", "0006_alter_voyage_category_alter_voyage_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="country",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="media/"),
        ),
        migrations.AddField(
            model_name="destination",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="media/"),
        ),
    ]
