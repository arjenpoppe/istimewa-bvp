from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.shortcuts import get_list_or_404, get_object_or_404

from vpi.models import Project, VPIValue


class PrestatiemetingTheme(models.Model):
    theme = models.CharField(max_length=50)

    def __str__(self):
        return self.theme

    def questions_on(self):
        return self.prestatiemetingquestion_set.filter(about='ON')

    def questions_og(self):
        return self.prestatiemetingquestion_set.filter(about='OG')


class PrestatiemetingQuestion(models.Model):
    OPDRACHTGEVER = 'OG'
    OPDRACHTNEMER = 'ON'
    ABOUT_CHOICES = [
        (OPDRACHTGEVER, 'Opdrachtgever'),
        (OPDRACHTNEMER, 'Opdrachtnemer'),
    ]

    number = models.IntegerField(primary_key=True)
    question = models.TextField()
    about = models.CharField(max_length=2, choices=ABOUT_CHOICES)
    theme = models.ForeignKey(PrestatiemetingTheme, on_delete=models.CASCADE)
    weight = models.IntegerField()

    def __str__(self):
        return f'Question number: {self.number}'


class Prestatiemeting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    number = models.IntegerField(null=True)
    filled_on = models.DateTimeField(null=True)
    filled_og = models.DateTimeField(null=True)

    def __str__(self):
        return f'Project: {self.project.number}'

    def get_distinct_themes(self, about):
        themes = PrestatiemetingTheme.objects.filter(id__in=self.prestatiemetingconfig_set.filter(
            question__about=about
        ).values_list(
            'question__theme', flat=True
        ).distinct())

        return themes

    def get_distinct_themes_on(self):
        return self.get_distinct_themes(PrestatiemetingQuestion.OPDRACHTNEMER)

    def get_distinct_themes_og(self):
        return self.get_distinct_themes(PrestatiemetingQuestion.OPDRACHTGEVER)

    def get_questions(self, about):
        questions = PrestatiemetingQuestion.objects.filter(
            number__in=self.prestatiemetingconfig_set.filter(
                question__about=about
            ).values_list(
                'question_id'
            )
        )
        return questions

    def get_questions_on(self):
        return self.get_questions(PrestatiemetingQuestion.OPDRACHTNEMER)

    def get_questions_og(self):
        return self.get_questions(PrestatiemetingQuestion.OPDRACHTGEVER)

    def save_excel_results(self, sheet):
        question_amount = int(sheet.cell_value(0, 1).split('=')[1])

        for i in range(question_amount):
            question_number = int(sheet.cell_value(i + 1, 0))
            answer_gradation = sheet.cell_value(i + 1, 1).split('.', 1)[0]
            question = PrestatiemetingQuestion.objects.get(pk=question_number)
            answer = question.prestatiemetinganswer_set.get(gradation__pk=answer_gradation)
            pmr = PrestatiemetingResult(prestatiemeting_id=self.id, question=question, answer=answer)
            pmr.save()


class PrestatiemetingGradation(models.Model):
    letter = models.CharField(max_length=1, primary_key=True)
    description = models.CharField(max_length=10)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.letter}: {self.description}'


class PrestatiemetingAnswer(models.Model):
    answer = models.TextField()
    gradation = models.ForeignKey(PrestatiemetingGradation, on_delete=models.CASCADE)
    question = models.ForeignKey(PrestatiemetingQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.gradation.letter}. {self.gradation.description} - {self.answer}'


class PrestatiemetingOpenQuestion(models.Model):
    question = models.TextField()
    answer = models.TextField()
    prestatiemeting = models.ForeignKey(Prestatiemeting, on_delete=models.CASCADE)


class PrestatiemetingConfig(models.Model):
    prestatiemeting = models.ForeignKey(Prestatiemeting, on_delete=models.CASCADE)
    question = models.ForeignKey(PrestatiemetingQuestion, on_delete=models.CASCADE)


class PrestatiemetingResult(models.Model):
    prestatiemeting = models.ForeignKey(Prestatiemeting, on_delete=models.CASCADE)
    question = models.ForeignKey(PrestatiemetingQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(PrestatiemetingAnswer, on_delete=models.CASCADE)
    explanation = models.TextField(null=True, blank=True)