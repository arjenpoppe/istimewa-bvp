from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from tablib import Dataset
import time
import xlrd

from .models.forms import Form

from .models.prestatiemeting import PrestatiemetingQuestion, PrestatiemetingTheme, Prestatiemeting, \
    PrestatiemetingConfig, PrestatiemetingResult, PrestatiemetingAnswer

from vpi.models import VPIValue, VPI
from vpi.vpis.prestatiemeting import calc_klanttevredenheid

from .resources import UltimoResource
from data.helpers.excel import export_prestatiemeting

from vpi.models import Project
from data.helpers.validator import validate_prestatiemeting_import


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
                upload_ultimo(request)
        else:
            print('Er is geen bestand geupload')
    return render(request, 'data/upload.html')


def upload_ultimo(request):
    ultimo_resource = UltimoResource()
    dataset = Dataset()

    start = time.time()
    dataset.load(request.FILES['datafile'].read())
    print('Loading the dataset took:', time.time() - start, 'seconds.')

    dry_run_start = time.time()
    result = ultimo_resource.import_data(dataset, dry_run=True, raise_errors=True)  # Test the data import
    print('Dry run took:', time.time() - dry_run_start, 'seconds.')

    print('Has errors:', result.has_errors())

    if not result.has_errors():
        start_import = time.time()
        ultimo_resource.import_data(dataset, dry_run=False)  # Actually import now
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

        val = VPIValue(vpi_id=1, value=calc_klanttevredenheid(pm.id))
        val.save()
    else:
        messages.error(request, error)
        print(messages)


@login_required
@permission_required('perms.view_forms')
def forms(request):
    if request.POST:
        project = get_object_or_404(Project, pk=request.POST.get('project_select'))
        pm = Prestatiemeting.objects.get_or_create(project=project)

        if 'prestatiemeting_conf' in request.POST:
            return redirect('data:prestatiemeting_config', prestatiemeting_id=pm[0].id)
        if 'prestatiemeting_fill' in request.POST:
            return redirect('data:prestatiemeting', prestatiemeting_id=pm[0].id)
        if 'prestatiemeting_upload' in request.POST:
            print('Go to prestatiemeting upload')

    context = {
        'projects': get_list_or_404(Project),
        'forms': get_list_or_404(request.user.form_set)
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

    pm = get_object_or_404(Prestatiemeting, pk=prestatiemeting_id)
    themes = PrestatiemetingTheme.objects.all()

    return render(request, 'data/prestatiemeting_config.html', {'prestatiemeting': pm,
                                                                'themes': themes})


@login_required
@permission_required('perms.view_forms')
def forms_detail(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
    return render(request, 'data/forms_detail.html', {'form': form})


@login_required
@permission_required('perms.view_forms')
def prestatiemeting(request, prestatiemeting_id):
    pm = Prestatiemeting.objects.get(pk=prestatiemeting_id)
    questions = pm.get_questions_og()

    if request.POST:
        print(request.POST)
        for question in questions:
            print(question)
            answer_id = request.POST.get(f'question_{question.number}')
            pmr = PrestatiemetingResult(prestatiemeting_id=prestatiemeting_id, question=question,
                                        answer=PrestatiemetingAnswer.objects.get(id=answer_id))
            pmr.save()

        pm.dateTime = datetime.now()
        pm.save()
        return redirect('data:forms')

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
