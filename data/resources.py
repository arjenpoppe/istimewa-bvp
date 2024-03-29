from import_export import resources
from import_export.fields import Field
from import_export.results import RowResult

from .models.sources import Ultimo, Sap


class UltimoResource(resources.ModelResource):
    id = Field(column_name='id')
    code = Field(attribute='code', column_name='Code')
    code_contract = Field(attribute='code_contract', column_name='Code contract')
    voortgangsstatus = Field(attribute='voortgangsstatus', column_name='Voortgangsstatus')
    omschrijving_jobsoort = Field(attribute='omschrijving_jobsoort', column_name='Omschrijving jobsoort')
    sap_nr = Field(attribute='sap_nr', column_name='SAP nr')
    vervolgjob_van = Field(attribute='vervolgjob_van', column_name='Vervolgjob van')
    omschrijving = Field(attribute='omschrijving', column_name='Omschrijving')
    code_complex = Field(attribute='code_complex', column_name='Code complex')
    code_object = Field(attribute='code_object', column_name='Code object')
    omschrijving_object = Field(attribute='omschrijving_object', column_name='Omschrijving object')
    storingsnummer = Field(attribute='storingsnummer', column_name='Storingsnummer')
    melddatum = Field(attribute='melddatum', column_name='Melddatum')
    gepl_startdatum = Field(attribute='gepl_startdatum', column_name='Gepl. startdatum')
    vertrektijd_thuis = Field(attribute='vertrektijd_thuis', column_name='Vertrektijd thuis')
    aankomsttijd = Field(attribute='aankomsttijd', column_name='Aankomsttijd')
    functioneel_herstel_tijd = Field(attribute='functioneel_herstel_tijd', column_name='Functioneel herstel tijd')
    gereedmeldtijd = Field(attribute='gereedmeldtijd', column_name='Gereedmeldtijd')
    vertrektijd = Field(attribute='vertrektijd', column_name='Vertrektijd')
    aankomsttijd_thuis = Field(attribute='aankomsttijd_thuis', column_name='Aankomsttijd thuis')
    medewerker = Field(attribute='medewerker', column_name='Medewerker')
    code_installatie = Field(attribute='code_installatie', column_name='Code nstallatie')
    code_installatie2 = Field(attribute='code_installatie2', column_name='Code installatie')
    installatie = Field(attribute=' installatie', column_name='Installatie')
    medewerker2 = Field(attribute='medewerker2', column_name='Medewerker')
    meldtext = Field(attribute='meldtext', column_name='Meldtext')
    functiehersteltijd_voor = Field(attribute='functiehersteltijd_voor', column_name='Functiehersteltijd voor')
    streefdatum_gereed_voor = Field(attribute='streefdatum_gereed_voor', column_name='Streefdatum gereed voor')
    info_tekst = Field(attribute='info_tekst', column_name='INFO tekst')
    storingsoorzaak = Field(attribute='storingsoorzaak', column_name='Storingsoorzaak')
    omschrijving_contract = Field(attribute='omschrijving_contract', column_name='Omschrijving contract')
    prioriteit = Field(attribute='prioriteit', column_name='Prioriteit')
    vestiging = Field(attribute='vestiging', column_name='Vestiging')
    vakgroep = Field(attribute='vakgroep', column_name='Vakgroep')
    leverancier = Field(attribute='leverancier', column_name='Leverancier')
    stremming_ja = Field(attribute='stremming_ja', column_name='Stremming Ja')
    scheepvaart = Field(attribute='scheepvaart', column_name='Scheepvaart')
    landverkeer = Field(attribute='landverkeer ', column_name='Landverkeer')
    geplande_stremming = Field(attribute='geplande_stremming', column_name='Geplande stremming')
    stremming_van = Field(attribute='stremming_van', column_name='Stremming van')
    stremming_tot = Field(attribute='stremming_tot', column_name='Stremming tot')
    stremmingsduur = Field(attribute='stremmingsduur', column_name='Stremmingsduur')
    geplande_uren = Field(attribute='geplande_uren', column_name='Geplande uren')
    geaccepteerd = Field(attribute='geaccepteerd', column_name='Geaccepteerd')
    code_medewerker = Field(attribute='code_medewerker', column_name='Code medewerker')
    medewerker3 = Field(attribute='medewerker3', column_name='Medewerker')
    datum_geaccepteerd = Field(attribute='datum_geaccepteerd', column_name='Datum geaccepteerd')
    meerwerk = Field(attribute='meerwerk', column_name='Meerwerk')
    code_document = Field(attribute='code_document', column_name='Code document')
    omschrijving_document = Field(attribute='omschrijving_document', column_name='Omschrijving document')
    code_jobplan = Field(attribute='code_jobplan', column_name='Code jobplan')
    omschrijving_jobplan = Field(attribute='omschrijving_jobplan', column_name='Omschrijving jobplan')
    omschrijving_job = Field(attribute='omschrijving_job', column_name='Omschrijving job')
    werkinstructie = Field(attribute='werkinstructie', column_name='Werkinstructie')
    observatietekst = Field(attribute='observatietekst', column_name='ObservatieTekst')
    onderzoektekst = Field(attribute='onderzoektekst', column_name='OnderzoekTekst')
    conclusietekst = Field(attribute='conclusietekst', column_name='ConclusieTekst')
    uitgevoerde_werkzaamheden = Field(attribute='uitgevoerde_werkzaamheden', column_name='Uitgevoerde werkzaamheden')
    controletekst = Field(attribute='controletekst', column_name='ControleTekst')
    opmerking_advies = Field(attribute='opmerking_advies', column_name='Opmerking / Advies')
    afbeelding = Field(attribute='afbeelding', column_name='Afbeelding')
    afbeelding2 = Field(attribute='afbeelding2', column_name='Afbeelding2')
    afbeelding3 = Field(attribute='afbeelding3', column_name='Afbeelding3')
    afbeelding4 = Field(attribute='afbeelding4', column_name='Afbeelding4')
    gewerkte_uren = Field(attribute='gewerkte_uren', column_name='Gewerkte uren')
    installatie2 = Field(attribute='installatie2', column_name='Installatie')
    installatie3 = Field(attribute='installatie3', column_name='Installatie')
    code_installatie3 = Field(attribute='code_installatie3', column_name='Code installatie')
    gevalideerd_door_rws = Field(attribute='gevalideerd_door_rws', column_name='Gevalideerd door RWS')
    ontvangen_rws = Field(attribute='ontvangen_rws', column_name='Ontvangen RWS')

    class Meta:
        model = Ultimo
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('code',)


class SapResource(resources.ModelResource):
    class Meta:
        model = Sap
