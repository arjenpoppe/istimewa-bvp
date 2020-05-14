from django.urls import path

import data.views as dataviews
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('<int:dashboard_id>', views.general_dashboard, name='dashboard'),
    path('project/<project_number>', views.project_dashboard, name='project_dashboard'),
    path('reports', views.reports, name='reports'),
    path('report', views.reports_detail, name='report'),
    path('ajax/get_pms', dataviews.get_prestatiemetingen, name='get_prestatiemetingen')
]