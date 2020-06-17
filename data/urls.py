from django.urls import path

from . import views

app_name = 'data'
urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('forms', views.forms, name='forms'),
    path('forms/<int:form_id>', views.forms_detail, name='forms_detail'),
    path('projects', views.projects_view, name='projects'),
    path('prestatiemeting/<int:prestatiemeting_id>/', views.prestatiemeting, name='prestatiemeting'),
    path('prestatiemeting/<int:prestatiemeting_id>/config/', views.prestatiemeting_config, name='prestatiemeting_config'),
    path('prestatiemeting/<int:prestatiemeting_id>/export/', views.export_excel, name='export_excel'),
    path('ajax/get_pms', views.get_prestatiemetingen, name='get_prestatiemetingen'),
]