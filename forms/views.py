from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.http import HttpResponse


@login_required
@permission_required('perms.view_forms')
def index(request):
    return render(request, 'forms/index.html')
