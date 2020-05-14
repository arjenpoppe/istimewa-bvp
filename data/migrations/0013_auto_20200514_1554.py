# Generated by Django 3.0.3 on 2020-05-14 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_auto_20200514_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ultimo',
            name='aankomsttijd',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='aankomsttijd_thuis',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='datum_geaccepteerd',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='functiehersteltijd_voor',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='functioneel_herstel_tijd',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='gepl_startdatum',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='gereedmeldtijd',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='streefdatum_gereed_voor',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='stremming_tot',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='stremming_van',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='vertrektijd',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ultimo',
            name='vertrektijd_thuis',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]