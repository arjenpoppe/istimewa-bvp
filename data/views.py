from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.http import HttpResponse
from tablib import Dataset
import time

from .resources import UltimoResource


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
    return render(request, 'data/forms.html')


@login_required
@permission_required('perms.view_forms')
def forms_detail(request, form_id):
    return render(request, 'data/forms.html')


@login_required
@permission_required('perms.view_forms')
def prestatiemeting(request):
    return render(request, 'data/prestatiemeting.html')


@login_required
@permission_required('perms.view_forms')
def configure_prestatiemeting(request):
    return render(request, 'data/prestatiemeting_configure.html')
