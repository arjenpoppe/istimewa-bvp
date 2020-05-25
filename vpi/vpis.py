from django.db.models.functions import TruncMonth

from data.models.prestatiemeting import Prestatiemeting, PrestatiemetingResult, PrestatiemetingQuestion

from django.db.models import Sum, Count, F, Avg
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from data.models.project import ProjectActiviteit, ProjectFase, Project
from data.models.sources import Sap, Ultimo

import random

"""
These functions get called from the VPI model. The function signatures are saved in the model and called by get_value().
Functions that are meant to provide data for a ChartJs object return a dictionary containing label and data. Other 
functions return float values.
"""


def klanttevredenheid(project):
    """
    Calculate the average klanttevredenheid.
    @param project: optional project to get project specific klanttevredenheid
    @return: avarege klanttevredenheid score in float
    """
    finished_prestatiemetingen = Prestatiemeting.objects.filter(filled_on__isnull=False, filled_og__isnull=False)
    if project:
        finished_prestatiemetingen = finished_prestatiemetingen.filter(project=project)
        print(finished_prestatiemetingen)

    if len(finished_prestatiemetingen) == 0:
        return None

    total = 0

    for prestatiemeting in finished_prestatiemetingen:
        total += prestatiemeting.get_score_on()

    return total / len(finished_prestatiemetingen)


def aanrijtijd(project):
    """
    Returns average aanrijtijd
    @param project: (optional) project object to execute this function for specific projects
    @return: Average aanrijtijd in minutes
    """
    data = Ultimo.objects.filter(omschrijving_jobsoort='Correctief Onderhoud', melddatum__isnull=False,
                                 aankomsttijd__isnull=False)
    if project:
        data = data.filter(code__contains=project.number)

    if len(data) is None:
        return None

    total = 0

    for row in data:
        aanrijtijd = row.aankomsttijd - row.melddatum
        total += aanrijtijd.total_seconds()

    return (total / 60) / len(data)


def functioneel_hersteltijd(project):
    """
    Returns average functiehersteltijd
    @param project: (optional) project object to execute this function for specific projects
    @return: Average hersteltijd in minutes
    """
    data = Ultimo.objects.filter(omschrijving_jobsoort='Correctief Onderhoud', melddatum__isnull=False,
                                 functioneel_herstel_tijd__isnull=False)

    if project:
        data = data.filter(code__contains=project.number)

    if len(data) is None:
        return None

    total = 0

    for row in data:
        aanrijtijd = row.functioneel_herstel_tijd - row.melddatum
        total += aanrijtijd.total_seconds()

    return (total / 60) / len(data)


def aantal_storingen_monthly(project):
    """
    Returns aantal storingen per month
    @param project: (optional) project object to execute this function for specific projects
    @return: Dictionary containing data and labels. Returns None id no data is available
    """
    past_year = datetime.now() - relativedelta(years=1)
    data = Ultimo.objects.filter(omschrijving_jobsoort='Correctief Onderhoud', melddatum__gt=past_year)
    if project:
        data = data.filter(code__contains=project.number)

    if len(data) is None:
        return None

    data = data.annotate(month=TruncMonth('melddatum')).values('month').annotate(total=Count('code')).order_by('month')

    months = []
    for month in data.values_list('month', flat=True):
        months.append(month.strftime('%B'))

    data = list(data.values_list('total', flat=True))

    data = {
        'data': data,
        'labels': months
    }

    return data


def prestatiemeting_opbouw(project):
    """
    Returns the sub themes and their scores of prestatiemetingen
    @param project:
    @return:
    """
    prestatiemeting_results = PrestatiemetingResult.objects.filter(question__about=PrestatiemetingQuestion.OPDRACHTNEMER)
    questions = PrestatiemetingQuestion.objects.filter(number__in=prestatiemeting_results.values_list('question', flat=True).distinct())

    if project:
        prestatiemeting_results = prestatiemeting_results.filter(prestatiemeting__project_id=project.number)

    if len(prestatiemeting_results) is None:
        return None

    rows = []

    for question in questions:
        theme = question.description
        weight = question.weight
        score = prestatiemeting_results.filter(question=question).aggregate(avg=Avg('answer__gradation__score'))
        rows.append([theme, f'{weight}%', score['avg']])

    data = {
        'headers': ['Thema', 'Weging', 'Score'],
        'rows': rows
    }

    return data


def verhouding_projectfasen(project):
    """
    Calculates the percentage of hours worked on ech project fase
    @param project: (optional) project object to execute this function for specific projects
    @return: dictionary containing data and labels
    """
    hours = []
    labels = []

    projectfases = ProjectFase.objects.all()
    for projectfase in projectfases:
        project_activities = projectfase.activities.filter(project=project).values_list('code', flat=True)
        sap_data = Sap.objects.filter(object__in=project_activities, he='H').aggregate(
            total=Sum(F('hoeveelheid_totaal')))

        hours.append(sap_data['total']) if sap_data['total'] else hours.append(0)
        labels.append(projectfase.get_fase_display())

    if not hours == [0, 0, 0, 0, 0]:
        total_hours = sum(hours)
    else:
        return None

    data = [percentage / total_hours * 100 for percentage in hours]

    context = {
        'data': data,
        'labels': labels,
    }

    return context


# def get_vpi_data(model, calc_way, attribute, *columns, **filters):
#     if not attribute in columns:
#         return None
#
#     data = model.objects.values(columns).filter(filters)
#
#     Deviation
#     Sum
#     Avg
#     Min
#     Max
#     Count
#     Annotate
#     Aggregate
