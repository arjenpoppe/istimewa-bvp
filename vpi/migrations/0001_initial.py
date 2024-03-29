# Generated by Django 3.0.3 on 2020-05-25 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VPI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('measuring_unit', models.CharField(blank=True, max_length=20)),
                ('function', models.CharField(blank=True, max_length=30, null=True)),
                ('has_subset', models.BooleanField(default=False)),
                ('decimal_amount', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='VPIValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happened', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('project_number', models.CharField(blank=True, max_length=8, null=True)),
                ('vpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vpi.VPI')),
            ],
        ),
        migrations.CreateModel(
            name='VPIValueBoolean',
            fields=[
                ('vpivalue_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vpi.VPIValue')),
                ('value', models.BooleanField()),
            ],
            bases=('vpi.vpivalue',),
        ),
        migrations.CreateModel(
            name='VPIValueNumber',
            fields=[
                ('vpivalue_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vpi.VPIValue')),
                ('value', models.FloatField()),
            ],
            bases=('vpi.vpivalue',),
        ),
        migrations.CreateModel(
            name='VPITarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lower_limit', models.FloatField()),
                ('upper_limit', models.FloatField()),
                ('is_better', models.CharField(choices=[('lower', 'Lager is beter'), ('higher', 'Hoger is better')], max_length=6)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.Project')),
                ('vpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vpi.VPI')),
            ],
        ),
    ]
