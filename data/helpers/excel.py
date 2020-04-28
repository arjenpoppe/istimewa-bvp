import xlsxwriter

from data.models import PrestatiemetingConfig, Prestatiemeting, PrestatiemetingQuestion

# Prestatiemeting Themes, questions and answers


def export_prestatiemeting(prestatiemeting_id=1):
    print('Method called')
    configs = PrestatiemetingConfig.objects.filter(prestatiemeting=Prestatiemeting.objects.get(id=prestatiemeting_id))
    questions = []

    for config in configs:
        if config.question.about == 'ON':
            questions.append(config.question)

    print(questions)

    # Create workbook and add a worksheet
    workbook = xlsxwriter.Workbook('prestatiemeting.xlsx')
    worksheet = workbook.add_worksheet()

    # Start of non static content
    row = 3
    col = 0

    # Write static data to file
    worksheet.merge_range('A1:C1', 'BEOORDELING VAN OPDRACHTNEMER DOOR OPDRACHTGEVER')
    worksheet.write(row - 1, col, 'Vraag')
    worksheet.write(row - 1, col + 1, 'Beoordeling')
    worksheet.write(row - 1, col + 2, 'Toelichting')

    # format options
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()

    # format cols
    worksheet.set_column('A:C', 80, cell_format)

    for question in questions:
        # inner row counter
        row_counter = row

        # write question
        worksheet.write(row_counter, col, f'{question.number}. {question.question}')

        answers = question.prestatiemetinganswer_set.all().values_list('answer', flat=True)
        answer_amount = len(answers)

        for answer in answers:
            worksheet.write(row_counter + 1, col + 1, answer)
            row_counter += 1
        worksheet.data_validation(row , col + 1, row, col + 1, {'validate': 'list',
                                                                'source': f'=$B${row + 2}:$B${row + 5}'})
        for i in range(row + 1, row + 5):
            worksheet.set_row(i, None, None, {'hidden': True})
        row += answer_amount + 1









    workbook.close()