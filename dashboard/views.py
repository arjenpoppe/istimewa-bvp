from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from vpi.models import VPI, VPIValue
from .models import Dashboard


@login_required
@permission_required('perms.view_dashboard', login_url='login')
def dashboard(request, dashboard_id):
    vpis = get_object_or_404(Dashboard, id=dashboard_id).vpis.all()

    data = []
    labels = ['inrichten', 'ontwerpen', 'uitvoeren', 'opleveren', 'overig']

    percentage1 = int(VPIValue.objects.get(vpi_id=3).value)
    percentage2 = int(VPIValue.objects.get(vpi_id=4).value)
    percentage3 = int(VPIValue.objects.get(vpi_id=5).value)
    percentage4 = int(VPIValue.objects.get(vpi_id=6).value)
    percentage5 = int(VPIValue.objects.get(vpi_id=7).value)
    data.append(percentage1)
    data.append(percentage2)
    data.append(percentage3)
    data.append(percentage4)
    data.append(percentage5)

    print(data)

    return render(request, 'dashboard/dashboard.html', {'vpis': vpis,
                                                        'data': data,
                                                        'labels': labels})


@login_required
@permission_required('perms.generate_reports')
def reports(request):
    return render(request, 'dashboard/reporting.html')


@login_required
@permission_required('perms.generate_reports')
def reports_detail(request, report_id):
    return render(request, 'dashboard/reporting.html')
