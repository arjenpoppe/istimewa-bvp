# Generated by Django 3.0.3 on 2020-04-28 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0029_auto_20200428_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestatiemetinganswer',
            name='answer',
            field=models.TextField(),
        ),
    ]