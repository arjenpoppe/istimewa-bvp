from django.contrib import admin

from .models import VPI, VPIValue, VPITarget, VPIDetailObject, FilterObjectBoolean, FilterObjectString, \
    FilterObjectDateTime, VPISource


class ValueInline(admin.TabularInline):
    model = VPIValue
    extra = 0
    readonly_fields = ["created"]


class VPIAdmin(admin.ModelAdmin):
    inlines = [ValueInline]


admin.site.register(VPI, VPIAdmin)

admin.site.register(VPITarget)

admin.site.register(VPIDetailObject)
admin.site.register(VPISource)
admin.site.register(FilterObjectBoolean)
admin.site.register(FilterObjectString)
admin.site.register(FilterObjectDateTime)

