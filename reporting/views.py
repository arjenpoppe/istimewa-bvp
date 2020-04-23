from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render


@login_required
@permission_required('perms.generate_reports')
def index(request):
    return render(request, 'reporting/index.html')
