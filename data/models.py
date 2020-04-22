from django.db import models


class Project(models.Model):
    number = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.number}: {self.name}'


class ProjectGoal(models.Model):
    number = models.IntegerField()
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    goal = models.TextField()

    def __str__(self):
        return f'{self.project.number}:{self.project.name} - Projectdoel {self.number}'


class VPI(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    measuring_unit = models.CharField(max_length=20)
    formula = models.CharField(max_length=200, blank=True, null=True)
    theme = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class VPITarget(models.Model):
    project_goal = models.OneToOneField(ProjectGoal, on_delete=models.CASCADE, null=True)
    vpi = models.OneToOneField(VPI, on_delete=models.CASCADE)
    green = models.CharField(max_length=10)
    yellow = models.CharField(max_length=20)
    red = models.CharField(max_length=20)

    def __str__(self):
        if self.project_goal:
            return f'{str(self.project_goal)}'
        else:
            return f'VPI: {str(self.vpi)}'


class Value(models.Model):
    value = models.FloatField()
    vpi = models.ForeignKey(VPI, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)


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
