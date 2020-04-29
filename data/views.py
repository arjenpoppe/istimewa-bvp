from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from tablib import Dataset
import time

from .models.forms import Form

from .models.prestatiemeting import PrestatiemetingQuestion, PrestatiemetingTheme, Prestatiemeting, \
    PrestatiemetingConfig, PrestatiemetingResult, PrestatiemetingAnswer

from .resources import UltimoResource
from data.helpers.excel import export_prestatiemeting

from vpi.models import Project


@login_required
@permission_required('perms.input_datafile')
def index(request):
    return render(request, 'data/index.html')


@login_required
@permission_required('perms.input_datafile')
def upload(request):
    if request.method == 'POST':
        if not request.FILES['myfile'] is None:
            ultimo_resource = UltimoResource()
            dataset = Dataset()

            new_records = request.FILES['myfile']

            start = time.time()
            dataset.load(new_records.read())
            print('Loading the dataset took:', time.time() - start, 'seconds.')

            dry_run_start = time.time()
            result = ultimo_resource.import_data(dataset, dry_run=True, raise_errors=True)  # Test the data import
            print('Dry run took:', time.time() - dry_run_start, 'seconds.')

            print('Has errors:', result.has_errors())

            if not result.has_errors():
                start_import = time.time()
                ultimo_resource.import_data(dataset, dry_run=False)  # Actually import now
                print('Import took:', time.time() - start_import, 'seconds.')

    return render(request, 'data/upload.html')


@login_required
@permission_required('perms.view_forms')
def forms(request):
    if request.POST:
        project = Project.objects.get(number=request.POST.get('project_select'))
        pm = Prestatiemeting.objects.get_or_create(project=project)

        if 'prestatiemeting_conf' in request.POST:
            return redirect('data:prestatiemeting_config', prestatiemeting_id=pm[0].id)
        if 'prestatiemeting_fill' in request.POST:
            return redirect('data:prestatiemeting', prestatiemeting_id=pm[0].id)
        if 'prestatiemeting_upload' in request.POST:
            print('Go to prestatiemeting upload')

    context = {
        'projects': Project.objects.all(),
        'forms': request.user.form_set.all(),
    }
    return render(request, 'data/forms.html', context=context)


@login_required
@permission_required('perms.view_forms')
def prestatiemeting_config(request, prestatiemeting_id, about='OG'):
    if request.POST:
        PrestatiemetingConfig.objects.filter(prestatiemeting=prestatiemeting_id).delete()

        for option in request.POST.getlist('question_checkbox'):
            print(request.POST.getlist('question_checkbox'))
            pmc = PrestatiemetingConfig(prestatiemeting=Prestatiemeting.objects.get(id=prestatiemeting_id),
                                        question=PrestatiemetingQuestion.objects.get(number=option))
            pmc.save()

        return redirect('data:forms')

    pm = Prestatiemeting.objects.get(id=prestatiemeting_id)
    themes = PrestatiemetingTheme.objects.all()

    return render(request, 'data/prestatiemeting_config.html', {'prestatiemeting': pm,
                                                                'themes': themes,
                                                                'about': about})


@login_required
@permission_required('perms.view_forms')
def forms_detail(request, form_id):
    form = Form.objects.get(pk=form_id)
    return render(request, 'data/forms_detail.html', {'form': form})


@login_required
@permission_required('perms.view_forms')
def prestatiemeting(request, prestatiemeting_id):
    pm = Prestatiemeting.objects.get(id=prestatiemeting_id)

    question_id_list = PrestatiemetingConfig.objects.filter(prestatiemeting=pm)\
        .values_list('question__number', flat=True).filter(question__about='OG')

    questions = PrestatiemetingQuestion.objects.filter(number__in=question_id_list,
                                                       about='OG')

    themes = []

    for question in questions:
        if question.theme not in themes:
            themes.append(question.theme)

    if request.POST:
        print(request.POST)
        for question in questions:
            print(question)
            answer_id = request.POST.get(f'question_{question.number}')
            pmr = PrestatiemetingResult(prestatiemeting=pm, question=question,
                                        answer=PrestatiemetingAnswer.objects.get(id=answer_id))
            pmr.save()

        pm.dateTime = datetime.now()
        pm.save()
        return redirect('data:forms')

    return render(request, 'data/prestatiemeting.html', {'prestatiemeting': pm, 'questions': questions, 'themes': themes})


@login_required
@permission_required('perms.view_forms')
def upload_prestatiemeting(request, project_id):
    return render(request, 'data/prestatiemeting_config.html')


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
