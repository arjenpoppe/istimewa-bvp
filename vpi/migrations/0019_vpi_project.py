# Generated by Django 3.0.3 on 2020-04-30 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpi', '0018_auto_20200430_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='vpi',
            name='project',
            field=models.ManyToManyField(blank=True, to='vpi.Project'),
        ),
    ]
