from django.contrib import admin
from .models import PrestatiemetingQuestion, PrestatiemetingAnswer, Prestatiemeting, Form, FormField, FormFieldMultipleChoiceAnswer


admin.site.register(Prestatiemeting)


class PrestatiemetingAnswerInline(admin.TabularInline):
    model = PrestatiemetingAnswer
    extra = 0


class PrestatiemetingQuestionAdmin(admin.ModelAdmin):
    inlines = [PrestatiemetingAnswerInline]
    list_display = ('question_number', 'theme', 'question')


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

