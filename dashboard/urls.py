from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reports', views.reports, name='reports'),
    path('reports/<int:pk>', views.reports_detail, name='report')
]
