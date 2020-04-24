from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.http import HttpResponse


@login_required
@permission_required('perms.view_dashboard', login_url='login')
def dashboard(request):
    print(request.user)
    return render(request, 'dashboard/dashboard.html')


@login_required
@permission_required('perms.generate_reports')
def reports(request):
    return render(request, 'dashboard/reporting.html')


@login_required
@permission_required('perms.generate_reports')
def reports_detail(request, report_id):
    return render(request, 'dashboard/reporting.html')
