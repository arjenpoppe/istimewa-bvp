import time
from datetime import datetime

import xlrd
import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from tablib import Dataset

from data.helpers.excel import export_prestatiemeting
from data.helpers.validator import validate_prestatiemeting_import
from vpi.models import Project
from vpi.models import VPIValue
from vpi.vpis.prestatiemeting import calc_klanttevredenheid
from vpi.vpis.project import calc_verhouding_all
from .models.forms import Form
from .models.prestatiemeting import PrestatiemetingTheme, Prestatiemeting, \
    PrestatiemetingConfig, PrestatiemetingResult, PrestatiemetingAnswer
from .models.project import ProjectActiviteit
from .models.sources import Sap
from .resources import UltimoResource, SapResource


@login_required
@permission_required('perms.input_datafile')
def index(request):
    return render(request, 'data/index.html')


@login_required
@permission_required('perms.input_datafile')
def upload(request):
    if request.method == 'POST':
        if not request.FILES['datafile'] is None:
            if request.POST.get('source') == 'prestatiemeting':
                upload_prestatiemeting(request)

            elif request.POST.get('source') == 'ultimo':
                upload_ultimo(request, UltimoResource())

            elif request.POST.get('source') == 'sap':
                upload_sap(request)
        else:
            print('Er is geen bestand geupload')
    return render(request, 'data/upload.html')


def upload_sap(request):
    file = request.FILES['datafile']
    data = pd.read_excel(file)

    # determine project number
    uploaded_project = None

    projects = Project.objects.all()
    for project in projects:
        if project.number in data['Object'].iloc[0]:
            uploaded_project = project

    data.rename(columns={
        data.columns[0]: "object",
        data.columns[1]: "wbs_element",
        data.columns[2]: "objectomschrijving",
        data.columns[3]: "kost_soort",
        data.columns[4]: "omschrijving",
        data.columns[5]: "personeelsnummer",
        data.columns[6]: "naam_kost_soort",
        data.columns[7]: "achternaam_voornaam",
        data.columns[8]: "per",
        data.columns[9]: "aan_afw",
        data.columns[10]: "parprs",
        data.columns[11]: "doc_number",
        data.columns[12]: "doc_datum",
        data.columns[13]: "boek_datum",
        data.columns[14]: "hoeveelheid_totaal",
        data.columns[15]: "he",
        data.columns[16]: "waarde_co_valuta",
        data.columns[17]: "omschrijving2",
        data.columns[18]: "categorie",
        data.columns[19]: "jaar",
        data.columns[20]: "maand",
        data.columns[21]: "week",
        data.columns[22]: "surcharge",
        data.columns[23]: "overhead",
        data.columns[24]: "besteltekst",
    }, inplace=True)

    # resource = SapResource()
    # dataset = Dataset()
    # dataset.load(data)
    # result = resource.import_data(dataset, dry_run=True, raise_errors=True)  # Test the data import
    #
    # if not result.has_errors():
    #     resource.import_data(dataset, dry_run=False)  # Actually import now
    #
    # save_project_activiteiten(uploaded_project)

    calc_verhouding_all(uploaded_project.number)


def save_project_activiteiten(project):
    unique_activiteit_codes = Sap.objects.order_by('object').values('object', 'objectomschrijving').distinct()

    for data in unique_activiteit_codes:
        ProjectActiviteit.objects.get_or_create(project=project, code=data['object'],
                                                description=data['objectomschrijving'])


def upload_ultimo(request, resource):
    dataset = Dataset()

    start = time.time()
    dataset.load(request.FILES['datafile'].read())
    print('Loading the dataset took:', time.time() - start, 'seconds.')

    dry_run_start = time.time()
    result = resource.import_data(dataset, dry_run=True, raise_errors=True)  # Test the data import
    print('Dry run took:', time.time() - dry_run_start, 'seconds.')

    print('Has errors:', result.has_errors())

    if not result.has_errors():
        start_import = time.time()
        resource.import_data(dataset, dry_run=False)  # Actually import now
        print('Import took:', time.time() - start_import, 'seconds.')


def upload_prestatiemeting(request):
    data = request.FILES['datafile']
    book = xlrd.open_workbook(file_contents=data.read())
    sheet = book.sheet_by_index(0)

    error = validate_prestatiemeting_import(sheet)
    print(error)

    if error is None:
        prestatiemeting_id = int(sheet.cell_value(0, 0).split('=')[1])
        pm = Prestatiemeting.objects.get(pk=prestatiemeting_id)

        pm.save_excel_results(sheet)
        pm.filled_og = datetime.now()
        pm.uploaded_by = request.user

        val = VPIValue(vpi_id=1, value=calc_klanttevredenheid(pm.id))
        val.save()
    else:
        messages.error(request, error)
        print(messages)


@login_required
@permission_required('perms.view_forms')
def forms(request):
    if request.POST:
        project = Project.objects.get(pk=request.POST.get('project_select'))
        pm_select = request.POST.get('pm_select')
        pm = Prestatiemeting.objects.get_or_create(project=project, number=pm_select)

        if 'prestatiemeting_conf' in request.POST:
            if pm[0].is_submitted_by_og() is False and pm[0].is_submitted_by_on() is False:
                return redirect('data:prestatiemeting_config', prestatiemeting_id=pm[0].id)
            else:
                messages.error(request, 'Prestatiemeting is al ingevuld. Configuratie kan niet meer worden'
                                        ' gewijzigd.')
        if 'prestatiemeting_fill' in request.POST:
            return redirect('data:prestatiemeting', prestatiemeting_id=pm[0].id)

        if 'prestatiemeting_upload' in request.POST:
            print('Go to prestatiemeting upload')

    context = {
        'projects': Project.objects.all(),
        'forms': request.user.form_set.all()
    }
    return render(request, 'data/forms.html', context=context)


@login_required
@permission_required('perms.view_forms')
def prestatiemeting_config(request, prestatiemeting_id):
    if request.POST:
        PrestatiemetingConfig.objects.filter(prestatiemeting_id=prestatiemeting_id).delete()

        for option in request.POST.getlist('question_checkbox'):
            PrestatiemetingConfig(prestatiemeting_id=prestatiemeting_id, question_id=option).save()

        return redirect('data:forms')

    pm = Prestatiemeting.objects.get(pk=prestatiemeting_id)
    themes = PrestatiemetingTheme.objects.all()

    return render(request, 'data/prestatiemeting_config.html', {'prestatiemeting': pm,
                                                                'themes': themes})


def get_prestatiemetingen(request):
    project = Project.objects.get(pk=request.GET.get('project_number', None))
    numbers = []
    prestatiemetingen = Prestatiemeting.objects.filter(project=project)
    for pm in prestatiemetingen:
        numbers.append(pm.number)

    data = {
        'numbers': numbers
    }

    return JsonResponse(data)


@login_required
@permission_required('perms.view_forms')
def forms_detail(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
    return render(request, 'data/forms_detail.html', {'form': form})


@login_required
@permission_required('perms.view_forms')
def prestatiemeting(request, prestatiemeting_id):
    pm = get_object_or_404(Prestatiemeting, pk=prestatiemeting_id)
    questions = pm.get_questions_og()

    if request.POST:
        PrestatiemetingResult.objects.filter(prestatiemeting_id=prestatiemeting_id).delete()
        print(request.POST)
        for question in questions:
            print(question)
            answer_id = request.POST.get(f'question_{question.number}')
            pmr = PrestatiemetingResult(prestatiemeting_id=prestatiemeting_id, question=question,
                                        answer=PrestatiemetingAnswer.objects.get(id=answer_id))
            pmr.save()

        pm.filled_on = datetime.now()
        pm.submitted_by = request.user
        pm.save()
        return redirect('data:forms')

    if pm.is_submitted_by_on():
        messages.warning(request,
                         f'Deze prestatiemeting is al ingevuld op {pm.filled_on.astimezone().strftime("%d-%m-%Y %H:%M")}'
                         f' door {pm.submitted_by.first_name} {pm.submitted_by.last_name}'
                         f' ({pm.submitted_by.email}). Voorgaande resultaten worden overschreven.')

    return render(request, 'data/prestatiemeting.html', {'prestatiemeting': pm})


@login_required
@permission_required('perms.view_forms')
def export_excel(request, prestatiemeting_id):
    output = export_prestatiemeting(prestatiemeting_id)
    output.seek(0)

    filename = 'prestatiemeting.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


def projects_view(request):
    projects = Project.objects.all()
    return render(request, 'data/projects.html', {'projects': projects})

