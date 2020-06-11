from django.urls import path

from . import views


app_name = 'vpi'
urlpatterns = [
    path('', views.search, name='index'),
    path('<int:vpi_id>/', views.details, name='detail'),
]