from django.db.models import Sum

from data.models.project import ProjectActiviteit, ProjectFase
from data.models.sources import Sap
from vpi.models import VPIValue, Project, VPI


def calc_verhouding_project(project_number, project_fase):
    project = Project.objects.get(pk=project_number)

    activities = ProjectActiviteit.objects.filter(project=project,
                                                  projectfase__fase=project_fase).values_list('code', flat=True)

    sap_data = Sap.objects.values('object', 'objectomschrijving') \
        .filter(object__contains=project_number, he='H') \
        .order_by('object') \
        .annotate(total=Sum('hoeveelheid_totaal'))

    hours = 0

    for row in sap_data:
        if row['object'] in activities:
            hours += row['total']

    total_hours = sap_data.aggregate(Sum('total'))
    percentage = hours / total_hours['total__sum'] * 100
    print(total_hours)
    print(activities)
    print(sap_data)

    return percentage


def verhouding_project_inrichting(project_number):
    percentage = calc_verhouding_project(project_number, ProjectFase.INRICHTING)
    VPIValue(value=percentage, vpi_id=3).save()


def verhouding_project_ontwerp(project_number):
    percentage = calc_verhouding_project(project_number, ProjectFase.ONTWERP)
    VPIValue(value=percentage, vpi_id=4).save()


def verhouding_project_uitvoer(project_number):
    percentage = calc_verhouding_project(project_number, ProjectFase.UITVOER)
    VPIValue(value=percentage, vpi_id=5).save()


def verhouding_project_oplevering(project_number):
    percentage = calc_verhouding_project(project_number, ProjectFase.OPLEVERING)
    VPIValue(value=percentage, vpi_id=6).save()


def verhouding_project_overig(project_number):
    percentage = calc_verhouding_project(project_number, ProjectFase.OVERIG)
    VPIValue(value=percentage, vpi_id=7).save()


def calc_verhouding_all(project_number):
    verhouding_project_inrichting(project_number)
    verhouding_project_ontwerp(project_number)
    verhouding_project_uitvoer(project_number)
    verhouding_project_oplevering(project_number)
    verhouding_project_overig(project_number)

