# Generated by Django 3.0.3 on 2020-04-30 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpi', '0022_auto_20200430_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpi',
            name='measuring_unit',
            field=models.CharField(blank=True, default='', max_length=20),
            preserve_default=False,
        ),
    ]
