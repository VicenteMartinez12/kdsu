# Generated by Django 5.1.6 on 2025-03-06 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='company_warehouse_id',
            field=models.CharField(max_length=20),
        ),
    ]
