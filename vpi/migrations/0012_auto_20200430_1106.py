# Generated by Django 3.0.3 on 2020-04-30 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpi', '0011_auto_20200430_1100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vpitarget',
            name='green',
        ),
        migrations.RemoveField(
            model_name='vpitarget',
            name='red',
        ),
        migrations.RemoveField(
            model_name='vpitarget',
            name='yellow',
        ),
        migrations.AddField(
            model_name='vpitarget',
            name='is_better',
            field=models.CharField(choices=[('lower', 'Lower'), ('higher', 'Higher')], default='higher', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vpitarget',
            name='lower_limit',
            field=models.FloatField(default=7.5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vpitarget',
            name='upper_limit',
            field=models.FloatField(default=8.0),
            preserve_default=False,
        ),
    ]
