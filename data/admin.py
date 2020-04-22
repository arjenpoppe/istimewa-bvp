from django.contrib import admin
from .models import Project, ProjectGoal, VPI, VPITarget, Value


class ValueInline(admin.TabularInline):
    model = Value
    extra = 0
    readonly_fields = ["created"]


class VPIAdmin(admin.ModelAdmin):
    inlines = [ValueInline]


admin.site.register(Project)
admin.site.register(ProjectGoal)
admin.site.register(VPI, VPIAdmin)
admin.site.register(VPITarget)
admin.site.register(Value)


