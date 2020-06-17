from django.contrib.auth.models import User

from django.db import models
from django.db.models import Avg


class PrestatiemetingTheme(models.Model):
    theme = models.CharField(max_length=50)

    def __str__(self):
        return self.theme

    def questions_on(self):
        """
        Get questions about ON from prestatiemeting theme object
        @return: Queryset with questions
        """
        return self.prestatiemetingquestion_set.filter(about='ON')

    def questions_og(self):
        """
        Get questions about OG from prestatiemeting theme object
        @return: Queryset with questions
        """
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
    description = models.CharField(max_length=100)
    weight = models.IntegerField()

    def __str__(self):
        return f'Question number: {self.number}'

    def get_avg_score(self):
        """
        Return average result of a prestatiemeting question
        @return: avg prestatiemeting result for specific question
        """
        return PrestatiemetingResult.objects.filter(question=self).aggregate(avg=Avg('answer__gradation__score'))


class Prestatiemeting(models.Model):
    project = models.ForeignKey(to='data.Project', on_delete=models.CASCADE)
    number = models.IntegerField(null=True)
    filled_on = models.DateTimeField(null=True)
    filled_og = models.DateTimeField(null=True)
    submitted_by = models.ForeignKey(User, related_name='%(class)s_submitted', on_delete=models.CASCADE, null=True)
    uploaded_by = models.ForeignKey(User, related_name='%(class)s_uploaded', on_delete=models.CASCADE, null=True)
    excel_file = models.FileField(upload_to='prestatiemetingen/', null=True)

    def __str__(self):
        return f'Project: {self.project}'

    def get_distinct_themes(self, about):
        """
        Return a set of disctict themes present in prestatiemeting object
        @param about: PrestatiemetingQuestion.OPDRACHTNEMER or PrestatiemetingQuestion.OPDRACHTGEVER
        @return: Queryset of prestatiemeting themes
        """
        themes = PrestatiemetingTheme.objects.filter(id__in=self.prestatiemetingconfig_set.filter(
            question__about=about
        ).values_list(
            'question__theme', flat=True
        ).distinct())

        return themes

    def get_distinct_themes_on(self):
        """
        Return a set of distinct prestatiemeting themes for questions about ON only
        @return: Queryset of prestatiemeting themes
        """
        return self.get_distinct_themes(PrestatiemetingQuestion.OPDRACHTNEMER)

    def get_distinct_themes_og(self):
        """
        Return a set of distinct prestatiemeting themes for questions about OG only
        @return: Queryset of prestatiemeting themes
        """
        return self.get_distinct_themes(PrestatiemetingQuestion.OPDRACHTGEVER)

    def get_questions(self, about):
        """
        Return questions present in this prestatiemeting
        @param about: PrestatiemetingQuestion.OPDRACHTNEMER or PrestatiemetingQuestion.OPDRACHTGEVER
        @return: List of question ids
        """
        questions = PrestatiemetingQuestion.objects.filter(
            number__in=self.prestatiemetingconfig_set.filter(
                question__about=about
            ).values_list(
                'question_id'
            )
        )
        return questions

    def get_questions_on(self):
        """
        Return list of questions about ON present in this prestatiemeting
        @return: list of question ids
        """
        return self.get_questions(PrestatiemetingQuestion.OPDRACHTNEMER)

    def get_questions_og(self):
        """
        Return list of questions about OG present in this prestatiemeting
        @return: list of question ids
        """
        return self.get_questions(PrestatiemetingQuestion.OPDRACHTGEVER)

    def save_excel_results(self, sheet):
        """
        Save the results of a prestatiemeting form OG -> ON
        @param sheet: Excel sheet object
        """
        question_amount = int(sheet.cell_value(0, 1).split('=')[1])
        PrestatiemetingResult.objects.filter(prestatiemeting=self,
                                             question__about=PrestatiemetingQuestion.OPDRACHTNEMER).delete()

        for i in range(question_amount):
            question_number = int(sheet.cell_value(i + 1, 0))
            answer_gradation = sheet.cell_value(i + 1, 1).split('.', 1)[0]
            explanation = sheet.cell_value(i + 1, 2)
            if explanation == 0.0:
                explanation = None
            question = PrestatiemetingQuestion.objects.get(pk=question_number)
            answer = question.prestatiemetinganswer_set.get(gradation__pk=answer_gradation)
            pmr = PrestatiemetingResult(prestatiemeting_id=self.id, question=question, answer=answer,
                                        explanation=explanation)
            pmr.save()

    def is_submitted_by_og(self):
        """
        Check whether prestatiemeting is submitted by OG
        @return: boolean
        """
        return self.filled_og is not None

    def is_submitted_by_on(self):
        """
        Check whether prestatiemeting is submitted by ON
        @return: boolean
        """
        return self.filled_on is not None

    def is_configured(self):
        """
        Check whether there is an existing prestatiemeting config for this prestatiemeting
        @return: boolean
        """
        return len(PrestatiemetingConfig.objects.filter(prestatiemeting=self)) > 0

    def get_score(self, about):
        """
        Calculate the total score of a prestatiemeting
        @param about: PrestatiemetingQuestion.OPDRACHTNEMER or PrestatiemetingQuestion.OPDRACHTGEVER
        @return: (float) total score
        """
        total_weight = 0
        result_list = self.prestatiemetingresult_set.filter(question__about=about)

        for result in result_list:
            total_weight += result.question.weight

        total = 0
        for result in result_list:
            rw = result.question.weight / total_weight
            total += rw * result.answer.gradation.score

        return total

    def get_score_on(self):
        """
        Calculate total score for ON of a prestatiemeting
        @return: (float) total score
        """
        return self.get_score(PrestatiemetingQuestion.OPDRACHTNEMER)

    def get_score_og(self):
        """
        Calculate total score for OG of a prestatiemeting
        @return: (float) total score
        """
        return self.get_score(PrestatiemetingQuestion.OPDRACHTGEVER)

    @property
    def date_finished(self):
        """
        property for the datetime on which the prestatiemething was finished
        @return: (datetime)
        """
        if self.filled_og > self.filled_on:
            return self.filled_og
        else:
            return self.filled_on

    def is_finished(self):
        """
        Check whether prestatiemeting is finished or not
        @return: boolean
        """
        return self.filled_og and self.filled_on

    def get_individual_score(self, question_number):
        """
        Get score for a specific question in this prestatiemeting
        @param question_number: question id
        @return: (float) score
        """
        result = self.prestatiemetingresult_set.get(question_id=question_number)
        return result.answer.gradation.score

    def get_results(self):
        """
        Return the totalscore and timestamp at which the prestatiemeting finished
        @return: dictionary where x value is a datetime and y value is the score ON
        """
        return {'x': self.date_finished, 'y': self.get_score_on()}


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

