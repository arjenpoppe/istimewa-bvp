# Generated by Django 3.0.3 on 2020-05-13 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20200513_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ultimo',
            name='aankomsttijd',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='melddatum',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
