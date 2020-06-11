# Generated by Django 3.0.3 on 2020-05-26 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20200525_1302'),
        ('vpi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vpi',
            name='question',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='VPIValuePrestatiemeting',
            fields=[
                ('vpivalue_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vpi.VPIValue')),
                ('prestatiemeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Prestatiemeting')),
            ],
            bases=('vpi.vpivalue',),
        ),
        migrations.CreateModel(
            name='VPIDetailConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_filters', models.CharField(max_length=10)),
                ('chart_type', models.CharField(choices=[('area', 'Area chart'), ('card', 'Card'), ('bar', 'Bar chart'), ('pie', 'Pie chart'), ('table', 'Table'), ('progress', 'Progress')], max_length=10)),
                ('vpi', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vpi.VPI')),
            ],
        ),
    ]