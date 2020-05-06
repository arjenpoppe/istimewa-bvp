from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('<int:dashboard_id>', views.dashboard, name='dashboard'),
    path('project/<project_number>', views.project_dashboard, name='project_dashboard'),
    path('reports', views.reports, name='reports'),
    path('reports/<int:pk>', views.reports_detail, name='report')
]