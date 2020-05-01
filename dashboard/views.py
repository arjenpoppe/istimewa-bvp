from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.http import HttpResponse

from vpi.models import VPI, VPIValue
from .models import Dashboard


@login_required
@permission_required('perms.view_dashboard', login_url='login')
def dashboard(request, dashboard_id):
    db = Dashboard.objects.get(id=dashboard_id)
    vpis = db.vpis.all()

    context = {
        'vpis': vpis
    }

    for vpi in vpis:
        print(vpi.name)
    return render(request, 'dashboard/dashboard.html', context=context)


@login_required
@permission_required('perms.generate_reports')
def reports(request):
    return render(request, 'dashboard/reporting.html')


@login_required
@permission_required('perms.generate_reports')
def reports_detail(request, report_id):
    return render(request, 'dashboard/reporting.html')
