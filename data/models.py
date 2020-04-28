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
        return f'question: {self.question.number} answer: {self.gradation.letter}'


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


class Ultimo(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    code_contract = models.CharField(max_length=50, blank=True, null=True)
    voortgangsstatus = models.CharField(max_length=30, blank=True, null=True)
    omschrijving_jobsoort = models.CharField(max_length=40, blank=True, null=True)
    sap_nr = models.CharField(max_length=30, blank=True, null=True)
    vervolgjob_van = models.CharField(max_length=30, blank=True, null=True)
    omschrijving = models.TextField(blank=True, null=True)
    code_complex = models.CharField(max_length=30, blank=True, null=True)
    code_object = models.CharField(max_length=30, blank=True, null=True)
    omschrijving_object = models.CharField(max_length=50, blank=True, null=True)
    storingsnummer = models.CharField(max_length=50, blank=True, null=True)
    melddatum = models.CharField(max_length=30, blank=True, null=True)
    gepl_startdatum = models.CharField(max_length=30, blank=True, null=True)
    vertrektijd_thuis = models.CharField(max_length=30, blank=True, null=True)
    aankomsttijd = models.CharField(max_length=30, blank=True, null=True)
    functioneel_herstel_tijd = models.CharField(max_length=30, blank=True, null=True)
    gereedmeldtijd = models.CharField(max_length=30, blank=True, null=True)
    vertrektijd = models.CharField(max_length=30, blank=True, null=True)
    aankomsttijd_thuis = models.CharField(max_length=30, blank=True, null=True)
    medewerker = models.CharField(max_length=30, blank=True, null=True)
    code_installatie = models.CharField(max_length=30, blank=True, null=True)
    code_installatie2 = models.CharField(max_length=25, blank=True, null=True)
    installatie = models.TextField(blank=True, null=True)
    medewerker2 = models.CharField(max_length=40, blank=True, null=True)
    meldtext = models.TextField(blank=True, null=True)
    functiehersteltijd_voor = models.CharField(max_length=30, blank=True, null=True)
    streefdatum_gereed_voor = models.CharField(max_length=30, blank=True, null=True)
    info_tekst = models.TextField(blank=True, null=True)
    storingsoorzaak = models.CharField(max_length=100, blank=True, null=True)
    omschrijving_contract = models.CharField(max_length=100, blank=True, null=True)
    prioriteit = models.CharField(max_length=40, blank=True, null=True)
    vestiging = models.CharField(max_length=10, blank=True, null=True)
    vakgroep = models.CharField(max_length=50, blank=True, null=True)
    leverancier = models.CharField(max_length=60, blank=True, null=True)
    stremming_ja = models.CharField(max_length=5, blank=True, null=True)
    scheepvaart = models.CharField(max_length=5, blank=True, null=True)
    landverkeer = models.CharField(max_length=5, blank=True, null=True)
    geplande_stremming = models.CharField(max_length=2, blank=True, null=True)
    stremming_van = models.CharField(max_length=30, blank=True, null=True)
    stremming_tot = models.CharField(max_length=30, blank=True, null=True)
    stremmingsduur = models.CharField(max_length=30, blank=True, null=True)
    geplande_uren = models.CharField(max_length=30, blank=True, null=True)
    geaccepteerd = models.CharField(max_length=5, blank=True, null=True)
    code_medewerker = models.CharField(max_length=10, blank=True, null=True)
    medewerker3 = models.CharField(max_length=30, blank=True, null=True)
    datum_geaccepteerd = models.CharField(max_length=30, blank=True, null=True)
    meerwerk = models.CharField(max_length=10, blank=True, null=True)
    code_document = models.CharField(max_length=10, blank=True, null=True)
    omschrijving_document = models.CharField(max_length=100, blank=True, null=True)
    code_jobplan = models.CharField(max_length=10, blank=True, null=True)
    omschrijving_jobplan = models.CharField(max_length=100, blank=True, null=True)
    omschrijving_job = models.TextField(blank=True, null=True)
    werkinstructie = models.TextField(blank=True, null=True)
    observatietekst = models.TextField(blank=True, null=True)
    onderzoektekst = models.TextField(blank=True, null=True)
    conclusietekst = models.TextField(blank=True, null=True)
    uitgevoerde_werkzaamheden = models.TextField(blank=True, null=True)
    controletekst = models.TextField(blank=True, null=True)
    opmerking_advies = models.TextField(blank=True, null=True)
    afbeelding = models.CharField(max_length=100, blank=True, null=True)
    afbeelding2 = models.CharField(max_length=100, blank=True, null=True)
    afbeelding3 = models.CharField(max_length=100, blank=True, null=True)
    afbeelding4 = models.CharField(max_length=100, blank=True, null=True)
    gewerkte_uren = models.CharField(max_length=10, blank=True, null=True)
    installatie2 = models.CharField(max_length=100, blank=True, null=True)
    installatie3 = models.CharField(max_length=100, blank=True, null=True)
    code_installatie3 = models.CharField(max_length=30, blank=True, null=True)
    gevalideerd_door_rws = models.CharField(max_length=10, blank=True, null=True)
    ontvangen_rws = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.code

    def _testthingy(self):
        return'test'
