import io

import xlsxwriter

from data.models.prestatiemeting import PrestatiemetingConfig, Prestatiemeting, PrestatiemetingQuestion


def export_prestatiemeting(prestatiemeting_id):
    configs = PrestatiemetingConfig.objects.filter(prestatiemeting=Prestatiemeting.objects.get(id=prestatiemeting_id))
    questions = []

    for config in configs:
        if config.question.about == config.question.OPDRACHTNEMER:
            questions.append(config.question)

    themes = []

    for question in questions:
        if question.theme not in themes:
            themes.append(question.theme)

    print(questions)

    meta_data_rows_required = len(questions) + 1

    # workbook in memory
    output = io.BytesIO()

    # Create workbook and add a worksheet
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # counters
    row = 1 + meta_data_rows_required
    col = 0
    meta_data_counter = 1
    question_rows = []

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
    worksheet.merge_range(row - 1, col, row - 1, col + 2, 'BEOORDELING VAN OPDRACHTNEMER DOOR OPDRACHTGEVER', title_format)

    worksheet.protect()

    # create visual data
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
                question_rows.append(row)
                row += answer_amount + 1

    # create metadata
    worksheet.write(0, 0, f'prestatiemeting_id={prestatiemeting_id}')
    worksheet.write(0, 1, f'question_amount={len(questions)}')
    worksheet.set_row(0, None, None, {'hidden': True})

    for question in questions:
        worksheet.write(meta_data_counter, 0, question.number)
        worksheet.write(meta_data_counter, 1, f'=B{question_rows[meta_data_counter - 1] + 1}')
        worksheet.set_row(meta_data_counter, None, None, {'hidden': True})
        meta_data_counter += 1

    print(question_rows)

    workbook.close()

    return output
