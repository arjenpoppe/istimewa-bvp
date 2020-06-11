from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import generic

from data.models.project import Project
from .models import VPI, FilterObjectDateTime, FilterObjectString


def index(request):
    return render(request, 'vpi/index.html')


@login_required
@permission_required('perms.view_dashboard')
def search(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        vpis = VPI.objects.filter(name__icontains=url_parameter)
    else:
        vpis = VPI.objects.all()

    ctx["vpis"] = vpis
    if request.is_ajax():

        html = render_to_string(
            template_name="vpi/vpi-results-partial.html", context={"vpis": vpis}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "vpi/search.html", context=ctx)


def details(request, vpi_id):
    projects = Project.objects.all()
    vpi = VPI.objects.get(pk=vpi_id)

    vpi_detail_object = vpi.vpidetailobject_set.get()

    data_container = vpi_detail_object.get_data_test()

    data = []

    for result in data_container.data:
        data.append(result.get_results())

    if request.POST:
        print(request.POST.get('date-from'))
        print(request.POST.get('date-to'))
        print(request.POST.get('project-select'))


    context = {
        'projects': projects,
        'vpi': vpi,
        'data': data
    }
    return render(request, 'vpi/detail.html', context=context)

    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     return VPI.objects.filter(pub_date__lte=timezone.now())
