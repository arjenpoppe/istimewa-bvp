from django.contrib import messages

from data.models.prestatiemeting import Prestatiemeting, PrestatiemetingQuestion, PrestatiemetingGradation


def validate_prestatiemeting_import(sheet):
    """
    Method to validate a prestatiemeting form filled by OG
    @param sheet: Excel datasheet
    @return: Error or None
    """
    try:
        prestatiemeting_id = int(sheet.cell_value(0, 0).split('=')[1])
        prestatiemeting = Prestatiemeting.objects.get(pk=prestatiemeting_id)
    except (Prestatiemeting.DoesNotExist, IndexError):
        return 'Prestatiemeting id kan niet gevonden worden. Dit is geen geldig formulier.'

    question_amount = int(sheet.cell_value(0, 1).split('=')[1])
    configured_questions = prestatiemeting.get_questions_on()
    configured_question_numbers = []
    for question in configured_questions:
        configured_question_numbers.append(question.number)

    for i in range(question_amount):
        question_number = int(sheet.cell_value(i + 1, 0))
        if question_number not in configured_question_numbers:
            return 'niet de correcte configuratie'

        answer = sheet.cell_value(i + 1, 1)[0]
        if answer not in PrestatiemetingGradation.objects.values_list('letter', flat=True):
            return 'niet alle vragen correct beantwoord'


def validate_ultimo_import():
    pass


def validate_sap_import():
    pass


def file_type_is_allowed():
    pass

