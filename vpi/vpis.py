from data.models.prestatiemeting import Prestatiemeting, PrestatiemetingResult, PrestatiemetingQuestion

from django.db.models import Sum
from datetime import datetime

from data.models.project import ProjectActiviteit, ProjectFase, Project
from data.models.sources import Sap, Ultimo


# these function names have to be written like <vpi.method>_<vpi.measure>


def klanttevredenheid_avg(project_id):
    finished_prestatiemetingen = Prestatiemeting.objects.filter(filled_on__isnull=False, filled_og__isnull=False)

    total = 0

    for prestatiemeting in finished_prestatiemetingen:
        total += prestatiemeting.get_score_on()

    return total / len(finished_prestatiemetingen)


def aanrijtijd_avg(project_id):
    # TODO hier verder
    if project_id:
        print('True')

    data = Ultimo.objects.filter(omschrijving_jobsoort='Correctief Onderhoud', melddatum__isnull=False, aankomsttijd__isnull=False)

    total = 0

    for row in data:
        melddatum = datetime.strptime(row.melddatum, "%Y-%m-%d %H:%M:%S")
        aankomsttijd = datetime.strptime(row.aankomsttijd, "%Y-%m-%d %H:%M:%S")

        aanrijtijd = aankomsttijd - melddatum

        total += aanrijtijd.total_seconds()

    print(total / len(data))


def prestatiemeting_sub_theme(question_id):
    question_id = 1
    finished_prestatiemetingen = Prestatiemeting.objects.filter(filled_on__isnull=False, filled_og__isnull=False,
                                                                prestatiemetingconfig__question__exact=question_id)

    total = 0

    for prestatiemeting in finished_prestatiemetingen:
        total += prestatiemeting.get_individual_score(question_id)

    return total / len(finished_prestatiemetingen)


def calc_verhouding_project(project_number, project_fase):
    print(project_number)
    project_number = project_number[0]
    print(project_number)
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

    return percentage


def verhouding_project_inrichting_single(project_number):
    percentage = calc_verhouding_project(project_number, ProjectFase.INRICHTING)
    return percentage


def verhouding_project_ontwerp_single(project_number):
    percentage = calc_verhouding_project(project_number, ProjectFase.ONTWERP)
    return percentage


def verhouding_project_uitvoer_single(project_number):
    percentage = calc_verhouding_project(project_number, ProjectFase.UITVOER)
    return percentage


def verhouding_project_oplevering_single(project_number):
    percentage = calc_verhouding_project(project_number, ProjectFase.OPLEVERING)
    return percentage


def verhouding_project_overig_single(project_number):
    percentage = calc_verhouding_project(project_number, ProjectFase.OVERIG)
    return percentage


def calc_verhouding_all(project_number):
    # verhouding_project_inrichting(project_number)
    # verhouding_project_ontwerp(project_number)
    # verhouding_project_uitvoer(project_number)
    # verhouding_project_oplevering(project_number)
    # verhouding_project_overig(project_number)
    pass

