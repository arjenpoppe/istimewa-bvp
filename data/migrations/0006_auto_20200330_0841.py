# Generated by Django 3.0.3 on 2020-03-30 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20200330_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ultimo',
            name='leverancier',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
