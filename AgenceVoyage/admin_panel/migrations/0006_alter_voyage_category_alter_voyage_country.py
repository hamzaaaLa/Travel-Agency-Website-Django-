# Generated by Django 5.0 on 2023-12-31 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0005_rename_prix_voyage_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voyage',
            name='category',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='country',
            field=models.CharField(max_length=200),
        ),
    ]
