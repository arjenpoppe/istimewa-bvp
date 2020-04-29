from django.db import models
from vpi.models import Project


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

    def __str__(self):
        return f'Question number: {self.number}'


class Prestatiemeting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    number = models.IntegerField(null=True)
    dateTime = models.DateTimeField(null=True)

    def __str__(self):
        return f'Project: {self.project.number}'


class PrestatiemetingGradation(models.Model):
    letter = models.CharField(max_length=1, primary_key=True)
    gradation = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.letter}: {self.gradation}'


class PrestatiemetingAnswer(models.Model):
    answer = models.TextField()
    gradation = models.ForeignKey(PrestatiemetingGradation, on_delete=models.CASCADE)
    question = models.ForeignKey(PrestatiemetingQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.gradation.letter}. {self.gradation.gradation} - {self.answer}'


class PrestatiemetingBeoordeling(models.Model):
    explanation = models.TextField()
    answer = models.ForeignKey(PrestatiemetingAnswer, on_delete=models.CASCADE)
    prestatiemeting = models.ForeignKey(Prestatiemeting, on_delete=models.CASCADE)


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