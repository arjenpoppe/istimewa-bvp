import io

import xlsxwriter

from data.models import PrestatiemetingConfig, Prestatiemeting, PrestatiemetingQuestion

# Prestatiemeting Themes, questions and answers


def export_prestatiemeting(prestatiemeting_id):
    configs = PrestatiemetingConfig.objects.filter(prestatiemeting=Prestatiemeting.objects.get(id=prestatiemeting_id))
    questions = []

    for config in configs:
        if config.question.about == 'ON':
            questions.append(config.question)

    themes = []

    for question in questions:
        if question.theme not in themes:
            themes.append(question.theme)

    print(questions)

    # workbook in memory
    output = io.BytesIO()

    # Create workbook and add a worksheet
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Start of non static content
    row = 1
    col = 0

    # format options
    theme_format = workbook.add_format()
    theme_format.set_font_size(15)
    theme_format.set_font_color('white')
    theme_format.set_bg_color('#4e73df')
    theme_format.set_border(1)
    theme_format.set_border_color('white')

    title_format = workbook.add_format()
    title_format.set_font_size(20)
    title_format.set_font_color('white')
    title_format.set_bg_color('#4e73df')
    title_format.set_border(1)
    title_format.set_border_color('white')

    question_header = workbook.add_format()
    question_header.set_bold()
    question_header.set_font_color('white')
    question_header.set_bg_color('#4e73df')
    question_header.set_border(1)
    question_header.set_border_color('white')

    unlocked = workbook.add_format()
    unlocked.set_locked(False)
    unlocked.set_text_wrap()

    # format cols
    worksheet.set_column('A:C', 80, workbook.add_format({'text_wrap': True}))

    # Write static data to file
    worksheet.merge_range('A1:C1', 'BEOORDELING VAN OPDRACHTNEMER DOOR OPDRACHTGEVER', title_format)

    worksheet.protect()

    for theme in themes:
        worksheet.merge_range(row, col, row, col + 2, theme.theme.upper(), theme_format)
        worksheet.write(row + 1, col, 'Vraag', question_header)
        worksheet.write(row + 1, col + 1, 'Beoordeling', question_header)
        worksheet.write(row + 1, col + 2, 'Toelichting', question_header)
        row += 2
        for question in questions:
            if question.theme == theme:
                # inner row counter
                row_counter = row

                # write question
                worksheet.write(row_counter, col, f'{question.number}. {question.question}')

                # collect answers
                answers = question.prestatiemetinganswer_set.all()
                answer_amount = len(answers)

                # write answers
                for answer in answers:
                    # antwoorden fields
                    worksheet.write(row_counter + 1, col + 1, str(answer))

                    row_counter += 1
                worksheet.data_validation(row, col + 1, row, col + 1, {'validate': 'list',
                                                                       'source': f'=$B${row + 2}:$B${row + 5}'})
                # hide options
                for i in range(row + 1, row + 5):
                    worksheet.set_row(i, None, None, {'hidden': True})

                # toelichting field
                worksheet.write(row, col + 2, None, unlocked)

                # choice field
                worksheet.write(row, col + 1, 'Maak een keuze', unlocked)
                row += answer_amount + 1

    workbook.close()

    return output
