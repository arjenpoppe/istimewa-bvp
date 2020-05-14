from django.contrib import admin
from .models import GeneralDashboard, Report, ProjectDashboard

admin.site.register(GeneralDashboard)
admin.site.register(ProjectDashboard)
admin.site.register(Report)
