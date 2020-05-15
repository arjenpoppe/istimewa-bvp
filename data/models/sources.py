from django.db import models
from django.db.models import Sum


class Ultimo(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    code_contract = models.CharField(max_length=30, blank=True, null=True)
    voortgangsstatus = models.CharField(max_length=30, blank=True, null=True)
    omschrijving_jobsoort = models.CharField(max_length=40, blank=True, null=True)
    sap_nr = models.CharField(max_length=30, blank=True, null=True)
    vervolgjob_van = models.CharField(max_length=30, blank=True, null=True)
    omschrijving = models.TextField(blank=True, null=True)
    code_complex = models.CharField(max_length=30, blank=True, null=True)
    code_object = models.CharField(max_length=30, blank=True, null=True)
    omschrijving_object = models.CharField(max_length=50, blank=True, null=True)
    storingsnummer = models.CharField(max_length=50, blank=True, null=True)
    melddatum = models.DateTimeField(blank=True, null=True)
    gepl_startdatum = models.DateTimeField(blank=True, null=True)
    vertrektijd_thuis = models.DateTimeField(blank=True, null=True)
    aankomsttijd = models.DateTimeField(blank=True, null=True)
    functioneel_herstel_tijd = models.DateTimeField(blank=True, null=True)
    gereedmeldtijd = models.DateTimeField(blank=True, null=True)
    vertrektijd = models.DateTimeField(blank=True, null=True)
    aankomsttijd_thuis = models.DateTimeField(blank=True, null=True)
    medewerker = models.CharField(max_length=30, blank=True, null=True)
    code_installatie = models.CharField(max_length=30, blank=True, null=True)
    code_installatie2 = models.CharField(max_length=25, blank=True, null=True)
    installatie = models.TextField(blank=True, null=True)
    medewerker2 = models.CharField(max_length=40, blank=True, null=True)
    meldtext = models.TextField(blank=True, null=True)
    functiehersteltijd_voor = models.DateTimeField(blank=True, null=True)
    streefdatum_gereed_voor = models.DateTimeField(blank=True, null=True)
    info_tekst = models.TextField(blank=True, null=True)
    storingsoorzaak = models.CharField(max_length=100, blank=True, null=True)
    omschrijving_contract = models.CharField(max_length=100, blank=True, null=True)
    prioriteit = models.CharField(max_length=40, blank=True, null=True)
    vestiging = models.CharField(max_length=10, blank=True, null=True)
    vakgroep = models.CharField(max_length=50, blank=True, null=True)
    leverancier = models.CharField(max_length=60, blank=True, null=True)
    stremming_ja = models.BooleanField(blank=True, null=True)
    scheepvaart = models.BooleanField(blank=True, null=True)
    landverkeer = models.BooleanField(blank=True, null=True)
    geplande_stremming = models.BooleanField(blank=True, null=True)
    stremming_van = models.DateTimeField(blank=True, null=True)
    stremming_tot = models.DateTimeField(blank=True, null=True)
    stremmingsduur = models.FloatField(blank=True, null=True)
    geplande_uren = models.CharField(max_length=30, blank=True, null=True)
    geaccepteerd = models.CharField(max_length=5, blank=True, null=True)
    code_medewerker = models.CharField(max_length=10, blank=True, null=True)
    medewerker3 = models.CharField(max_length=30, blank=True, null=True)
    datum_geaccepteerd = models.DateTimeField(blank=True, null=True)
    meerwerk = models.BooleanField(blank=True, null=True)
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
    gewerkte_uren = models.FloatField(blank=True, null=True)
    installatie2 = models.CharField(max_length=100, blank=True, null=True)
    installatie3 = models.CharField(max_length=100, blank=True, null=True)
    code_installatie3 = models.CharField(max_length=30, blank=True, null=True)
    gevalideerd_door_rws = models.BooleanField(blank=True, null=True)
    ontvangen_rws = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.code




class Sap(models.Model):
    object = models.CharField(max_length=100, null=True, blank=True)
    wbs_element = models.CharField(max_length=100, null=True, blank=True)
    objectomschrijving = models.CharField(max_length=100, null=True, blank=True)
    kost_soort = models.CharField(max_length=100, null=True, blank=True)
    omschrijving = models.CharField(max_length=255, null=True, blank=True)
    personeelsnummer = models.CharField(max_length=100, null=True, blank=True)
    naam_kost_soort = models.CharField(max_length=100, null=True, blank=True)
    achternaam_voornaam = models.CharField(max_length=100, null=True, blank=True)
    per = models.IntegerField(blank=True, null=True)
    aan_afw = models.CharField(max_length=100, null=True, blank=True)
    parprs = models.CharField(max_length=100, null=True, blank=True)
    doc_number = models.CharField(max_length=100, null=True, blank=True)
    doc_datum = models.DateField(blank=True, null=True)
    boek_datum = models.DateField(blank=True, null=True)
    hoeveelheid_totaal = models.FloatField(blank=True, null=True)
    he = models.CharField(max_length=100, null=True, blank=True)
    waarde_co_valuta = models.FloatField(blank=True, null=True)
    omschrijving2 = models.CharField(max_length=100, null=True, blank=True)
    categorie = models.CharField(max_length=100, null=True, blank=True)
    jaar = models.CharField(max_length=255, null=True, blank=True)
    maand = models.CharField(max_length=255, null=True, blank=True)
    week = models.CharField(max_length=255, null=True, blank=True)
    surcharge = models.CharField(max_length=255, null=True, blank=True)
    overhead = models.CharField(max_length=255, null=True, blank=True)
    besteltekst = models.TextField(blank=True, null=True)

    def totaal_uren_per_activiteit(self):
        data = self.objects.values('object', 'objectomschrijving') \
            .filter(he='H') \
            .order_by('object') \
            .annotate(total=Sum('hoeveelheid_totaal'))

        return data




