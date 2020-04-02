from django.contrib import admin
from .models import Ultimo


class UltimoAdmin(admin.ModelAdmin):
    list_display = ('code', 'code_contract', 'voortgangsstatus', 'stremming_ja')



admin.site.register(Ultimo, UltimoAdmin)

