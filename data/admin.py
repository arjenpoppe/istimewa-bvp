from django.contrib import admin
from .models import PrestatiemetingQuestion, PrestatiemetingAnswer, Prestatiemeting


class PrestatiemetingAnswerInline(admin.TabularInline):
    model = PrestatiemetingAnswer
    extra = 0


class PrestatiemetingQuestionAdmin(admin.ModelAdmin):
    inlines = [PrestatiemetingAnswerInline]
    list_display = ('question_number', 'theme', 'question')


admin.site.register(Prestatiemeting)
admin.site.register(PrestatiemetingQuestion, PrestatiemetingQuestionAdmin)

