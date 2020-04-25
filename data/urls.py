from django.urls import path

from . import views

app_name = 'data'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('forms', views.forms, name='forms'),
    path('forms/<int:form_id>', views.forms_detail, name='forms_detail'),
    path('prestatiemeting/<int:pk>', views.prestatiemeting, name='prestatiemeting'),
    path('prestatiemeting/<int:pk>/conf', views.configure_prestatiemeting, name='configure_prestatiemeting'),
    path('prestatiemeting/<int:pk>/upload', views.upload_prestatiemeting, name='upload_prestatiemeting')
]