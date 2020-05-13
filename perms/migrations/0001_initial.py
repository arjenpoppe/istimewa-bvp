# Generated by Django 3.0.3 on 2020-05-12 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('input_datafile', 'Can upload datafile'), ('input_form', 'Can submit form'), ('view_forms', 'Can view forms'), ('generate_reports', 'Can generate reports'), ('manage_app', 'Can manage application'), ('view_logs', 'Can view log files'), ('edit_data', 'Can edit data'), ('export_data', 'Can export data'), ('view_dashboard', 'Can view dashboard'), ('prestatiemeting', 'Can execute a prestatiemeting')),
            },
        ),
    ]
