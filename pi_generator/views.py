from django.shortcuts import render

def index(request):
    return render(request, 'pi_generator/index.html')
