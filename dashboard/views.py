from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.http import HttpResponse


@login_required
@permission_required('perms.view_dashboard', login_url='login')
def index(request):
    print(request.user)
    return render(request, 'dashboard/index.html')