# Generated by Django 3.0.3 on 2020-06-10 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vpi', '0005_vpisource'),
    ]

    operations = [
        migrations.AddField(
            model_name='vpi',
            name='source',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vpi.VPISource'),
            preserve_default=False,
        ),
    ]
