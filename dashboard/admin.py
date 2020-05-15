from django.contrib import admin
from .models import Dashboard, Report, DashboardObject


class DashboardObjectInline(admin.TabularInline):
    model = DashboardObject


class DashboardAdmin(admin.ModelAdmin):
    inlines = [DashboardObjectInline]
    list_display = ('name', 'description', 'project')


admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(Report)
