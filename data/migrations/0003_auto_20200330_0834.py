# Generated by Django 3.0.3 on 2020-03-30 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20200330_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ultimo',
            name='code_installatie3',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
