from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth import views as auth_views


@login_required
def index(request):
    return render(request, 'index.html')


def logout(request):
    return logout_then_login(request, '/login/')