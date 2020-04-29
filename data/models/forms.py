from django.contrib.auth.models import User
from django.db import models
from vpi.models import Project


class Form(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ManyToManyField(User)
    last_filled = models.DateTimeField()

    def __str__(self):
        return self.name

    def get_form_fields(self):
        return self.objects.formfield_set.all()


class FormField(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    allow_explanation = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class FormFieldMultipleChoiceAnswer(models.Model):
    answer = models.TextField()
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer