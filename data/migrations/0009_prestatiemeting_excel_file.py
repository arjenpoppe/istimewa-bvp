# Generated by Django 3.0.3 on 2020-05-14 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_auto_20200513_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestatiemeting',
            name='excel_file',
            field=models.FileField(null=True, upload_to='prestatiemetingen'),
        ),
    ]