# Generated by Django 3.0.3 on 2020-03-30 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20200330_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ultimo',
            name='code',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
