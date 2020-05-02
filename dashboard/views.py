from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from vpi.models import VPI, VPIValue
from .models import Dashboard


@login_required
@permission_required('perms.view_dashboard', login_url='login')
def dashboard(request, dashboard_id):
    vpis = get_object_or_404(Dashboard, id=dashboard_id).vpis.all()
    return render(request, 'dashboard/dashboard.html', {'vpis': vpis})


@login_required
@permission_required('perms.generate_reports')
def reports(request):
    return render(request, 'dashboard/reporting.html')


@login_required
@permission_required('perms.generate_reports')
def reports_detail(request, report_id):
    return render(request, 'dashboard/reporting.html')
