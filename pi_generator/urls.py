from django.urls import path

from . import views


app_name = 'pi_generator'
urlpatterns = [
    path('', views.index, name='index'),
]