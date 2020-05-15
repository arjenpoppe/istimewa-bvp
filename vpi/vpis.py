from django.db.models.functions import TruncMonth

from data.models.prestatiemeting import Prestatiemeting, PrestatiemetingResult, PrestatiemetingQuestion

from django.db.models import Sum, Count, F
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from data.models.project import ProjectActiviteit, ProjectFase, Project
from data.models.sources import Sap, Ultimo


"""
These functions get called from the VPI model. The function signatures are saved in the model and called by get_value().
Functions that are meant to provide data for a ChartJs object return a dictionary containing label and data. Other 
functions return float values.
"""


def klanttevredenheid(project_id):
    """
    Calculate the average klanttevredenheid.
    @param project_id: optional project to get project specific klanttevredenheid
    @return: avarege klanttevredenheid score in float
    """
    finished_prestatiemetingen = Prestatiemeting.objects.filter(filled_on__isnull=False, filled_og__isnull=False)
    print(project_id)
    if project_id:
        finished_prestatiemetingen = finished_prestatiemetingen.filter(project_id=project_id)

    print(len(finished_prestatiemetingen))

    total = 0

    for prestatiemeting in finished_prestatiemetingen:
        total += prestatiemeting.get_score_on()

    return total / len(finished_prestatiemetingen)




def aanrijtijd(project_id):
    data = Ultimo.objects.filter(omschrijving_jobsoort='Correctief Onderhoud', melddatum__isnull=False,
                                 aankomsttijd__isnull=False)

    if project_id:
        pass

    total = 0

    for row in data:
        aanrijtijd = row.aankomsttijd - row.melddatum
        total += aanrijtijd.total_seconds()

    return (total / 60) / len(data)


def functioneel_hersteltijd(project_id):
    data = Ultimo.objects.filter(omschrijving_jobsoort='Correctief Onderhoud', melddatum__isnull=False,
                                 functioneel_herstel_tijd__isnull=False)

    total = 0

    for row in data:
        aanrijtijd = row.functioneel_herstel_tijd - row.melddatum
        total += aanrijtijd.total_seconds()

    return (total / 60) / len(data)


def aantal_storingen_monthly(project_id):
    """
    returns
    @param project_id:
    @return:
    """
    past_year = datetime.now() - relativedelta(years=1)
    data = Ultimo.objects.filter(omschrijving_jobsoort='Correctief Onderhoud', melddatum__gt=past_year).annotate(month=TruncMonth('melddatum')).values('month')\
        .annotate(total=Count('code')).order_by('month')

    months = []
    for month in data.values_list('month', flat=True):
        months.append(month.strftime('%B'))

    data = list(data.values_list('total', flat=True))

    data = {
        'data': data,
        'labels': months
    }

    return data


def prestatiemeting_sub_theme(question_id):
    question_id = 1
    finished_prestatiemetingen = Prestatiemeting.objects.filter(filled_on__isnull=False, filled_og__isnull=False,
                                                                prestatiemetingconfig__question__exact=question_id)

    total = 0

    for prestatiemeting in finished_prestatiemetingen:
        total += prestatiemeting.get_individual_score(question_id)

    return total / len(finished_prestatiemetingen)


def verhouding_projectfasen(project_number):
    """
    Calculates the percentage of hours worked on ech project fase
    @param project_number: project_number
    @return: dictionary containing data and labels
    """
    hours = []
    labels = []

    projectfases = ProjectFase.objects.all()
    for projectfase in projectfases:
        project_activities = projectfase.activities.filter(project_id=project_number).values_list('code', flat=True)
        sap_data = Sap.objects.filter(object__in=project_activities, he='H').aggregate(total=Sum('hoeveelheid_totaal'))

        hours.append(sap_data['total'])
        labels.append(projectfase.fase)

    total_hours = sum(hours)

    data = [percentage / total_hours * 100 for percentage in hours]

    context = {
        'data': data,
        'labels': labels
    }

    return context

