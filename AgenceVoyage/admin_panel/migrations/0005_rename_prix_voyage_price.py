# Generated by Django 5.0 on 2023-12-31 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_rename_categorie_voyage_category_destination'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voyage',
            old_name='prix',
            new_name='price',
        ),
    ]
