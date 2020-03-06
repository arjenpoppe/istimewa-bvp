from django.contrib import admin
from .models import PerformanceIndicator, Target, Value, Project, Source, ProjectGoal

class TargetInline(admin.TabularInline):
    model = Target
    extra = 0


class ValueInline(admin.TabularInline):
    model = Value
    list_display = ('value', 'timestamp')


class PerformanceIndicatorAdmin(admin.ModelAdmin):
    inlines = [TargetInline, ValueInline]


admin.site.register(PerformanceIndicator, PerformanceIndicatorAdmin)
admin.site.register(Source)


class ProjectGoalInline(admin.StackedInline):
    model = ProjectGoal
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectGoalInline]


admin.site.register(Project, ProjectAdmin)