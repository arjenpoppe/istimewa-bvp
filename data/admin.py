from django.contrib import admin
from .models.prestatiemeting import PrestatiemetingQuestion, PrestatiemetingAnswer, Prestatiemeting, \
    PrestatiemetingGradation, PrestatiemetingTheme

from .models.forms import Form, FormField, FormFieldMultipleChoiceAnswer


admin.site.register(Prestatiemeting)


class PrestatiemetingAnswerInline(admin.TabularInline):
    model = PrestatiemetingAnswer
    extra = 0


class PrestatiemetingQuestionAdmin(admin.ModelAdmin):
    inlines = [PrestatiemetingAnswerInline]
    list_display = ('number', 'theme', 'question')


admin.site.register(PrestatiemetingQuestion, PrestatiemetingQuestionAdmin)


class FormFieldInline(admin.TabularInline):
    model = FormField


class FormAdmin(admin.ModelAdmin):
    inlines = [FormFieldInline]


admin.site.register(Form, FormAdmin)


class FormFieldMultipleChoiceAnswerInline(admin.TabularInline):
    model = FormFieldMultipleChoiceAnswer


class FormFieldAdmin(admin.ModelAdmin):
    inlines = [FormFieldMultipleChoiceAnswerInline]


admin.site.register(FormField, FormFieldAdmin)
admin.site.register(PrestatiemetingGradation)
admin.site.register(PrestatiemetingTheme)




