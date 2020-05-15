from django.contrib.admin.utils import unquote
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from data.helpers.excel import prestatiemeting_report
from data.models.prestatiemeting import Prestatiemeting, PrestatiemetingResult, PrestatiemetingQuestion
from data.models.project import Project
from vpi.models import VPI
from .models import Report, Dashboard


@login_required
@permission_required('perms.view_dashboard', login_url='login')
def general_dashboard(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, id=dashboard_id)
    questions = PrestatiemetingQuestion.objects.filter(about=PrestatiemetingQuestion.OPDRACHTNEMER)
    dashboard.get_ordered_objects_by_row()

    for question in questions:
        question.get_avg_score()

    context = {
        'questions': questions,
        'dashboard': dashboard,
    }

    return render(request, 'dashboard/dashboard.html', context=context)


@login_required
@permission_required('perms.view_dashboard', login_url='login')
def project_dashboard(request, project_number):
    project_number = unquote(project_number)
    dashboard = Dashboard.objects.get(project_id=project_number)

    return render(request, 'dashboard/project_dashboard.html', {'dashboard': dashboard})


@login_required
@permission_required('perms.generate_reports')
def reports(request):

    reports = Report.objects.all()
    projects = Project.objects.all()

    return render(request, 'dashboard/reports.html', {'reports': reports,
                                                      'projects': projects})


@login_required
@permission_required('perms.generate_reports')
def reports_detail(request):
    if request.POST:
        pm = Prestatiemeting.objects.get(project_id=request.POST.get('project_select'),
                                         number=request.POST.get('pm_select'))

        output = prestatiemeting_report(pm.id)
        output.seek(0)

        filename = 'prestatiemeting_resultaten.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
