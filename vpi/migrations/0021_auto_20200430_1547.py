# Generated by Django 3.0.3 on 2020-04-30 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vpi', '0020_auto_20200430_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpitarget',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vpi.Project'),
        ),
    ]
