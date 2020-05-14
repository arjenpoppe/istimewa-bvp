from django.contrib import admin

from .models import VPI, VPIValue, CombinedVPI, VPITarget


class ValueInline(admin.TabularInline):
    model = VPIValue
    extra = 0
    readonly_fields = ["created"]


class VPIAdmin(admin.ModelAdmin):
    inlines = [ValueInline]


admin.site.register(VPI, VPIAdmin)

admin.site.register(CombinedVPI)
admin.site.register(VPITarget)

