from django.contrib import admin
from .models import Project, ProjectGoal, VPI, VPITarget, VPIValue, Opdrachtgever, Address, OpdrachtgeverContactPersoon


class ValueInline(admin.TabularInline):
    model = VPIValue
    extra = 0
    readonly_fields = ["created"]


class VPIAdmin(admin.ModelAdmin):
    inlines = [ValueInline]


class OpdrachtgeverContactPersoonInline(admin.StackedInline):
    model = OpdrachtgeverContactPersoon
    extra = 0


class OpdrachtgeverAdmin(admin.ModelAdmin):
    inlines = [OpdrachtgeverContactPersoonInline]


admin.site.register(Project)
admin.site.register(ProjectGoal)
admin.site.register(VPI, VPIAdmin)
admin.site.register(VPITarget)
admin.site.register(VPIValue)
admin.site.register(Opdrachtgever, OpdrachtgeverAdmin)
admin.site.register(Address)

