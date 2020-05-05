# Generated by Django 3.0.3 on 2020-05-04 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0042_auto_20200504_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sap',
            name='jaar',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sap',
            name='maand',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sap',
            name='omschrijving',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sap',
            name='overhead',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sap',
            name='surcharge',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sap',
            name='week',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
