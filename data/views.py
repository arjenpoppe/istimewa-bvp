from django.shortcuts import render
from django.http import HttpResponse
from tablib import Dataset
import time

from .resources import UltimoResource


def index(request):
    return render(request, 'data/index.html')


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
