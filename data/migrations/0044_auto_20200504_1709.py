# Generated by Django 3.0.3 on 2020-05-04 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0043_auto_20200504_1502'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sap',
            old_name='waarde_co_value',
            new_name='waarde_co_valuta',
        ),
    ]
