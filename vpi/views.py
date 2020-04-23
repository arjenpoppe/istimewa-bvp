from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

from bvp import settings
from data.models import VPI


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


class DetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'perms.view_dashboard'
    model = VPI
    template_name = 'vpi/detail.html'

    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     return VPI.objects.filter(pub_date__lte=timezone.now())
