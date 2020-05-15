# Generated by Django 3.0.3 on 2020-05-15 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpi', '0002_vpitarget_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vpi',
            name='default_measure',
        ),
        migrations.AddField(
            model_name='vpi',
            name='has_subset',
            field=models.BooleanField(default=0),
        ),
    ]
