from django.contrib import admin
from .models.prestatiemeting import PrestatiemetingQuestion, PrestatiemetingAnswer, Prestatiemeting, \
    PrestatiemetingGradation, PrestatiemetingTheme

from .models.forms import Form, FormField, FormFieldMultipleChoiceAnswer
from .models.project import Project, Opdrachtgever, OpdrachtgeverContactPersoon, Address, ProjectActiviteit, ProjectFase

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

admin.site.register(Project)
admin.site.register(ProjectActiviteit)
admin.site.register(ProjectFase)
admin.site.register(Opdrachtgever)
admin.site.register(OpdrachtgeverContactPersoon)
admin.site.register(Address)




