# Generated by Django 3.0.3 on 2020-05-12 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vpi', '0003_vpi_default_measure'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vpi',
            old_name='method',
            new_name='function',
        ),
    ]