# Generated by Django 3.0.3 on 2020-05-06 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpi', '0026_auto_20200506_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='CombinedVPI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('theme', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('chart_type', models.CharField(choices=[('AC', 'Area chart'), ('CA', 'Card'), ('BC', 'Bar chart'), ('PC', 'Pie chart')], max_length=2)),
                ('vpis', models.ManyToManyField(to='vpi.VPI')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='combined_vpis',
            field=models.ManyToManyField(blank=True, to='vpi.CombinedVPI'),
        ),
    ]
