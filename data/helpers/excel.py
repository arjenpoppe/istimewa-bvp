import io

import xlsxwriter
from django.shortcuts import get_object_or_404

from data.models.prestatiemeting import PrestatiemetingConfig, Prestatiemeting, PrestatiemetingResult, \
    PrestatiemetingTheme, PrestatiemetingQuestion


def export_prestatiemeting(prestatiemeting_id):
    """
    Excel generator for prestatiemeting forms
    @param prestatiemeting_id: id of the prestatiemeting
    @return: Excel workbook
    """
    pm = get_object_or_404(Prestatiemeting, id=prestatiemeting_id)
    questions = pm.get_questions_on()
    themes = pm.get_distinct_themes_on()

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
    worksheet.merge_range(row - 1, col, row - 1, col + 2, 'BEOORDELING VAN OPDRACHTNEMER DOOR OPDRACHTGEVER',
                          title_format)

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
        worksheet.write(meta_data_counter, 2, f'=C{question_rows[meta_data_counter - 1] + 1}')
        worksheet.set_row(meta_data_counter, None, None, {'hidden': True})
        meta_data_counter += 1

    print(question_rows)

    workbook.close()

    return output


def prestatiemeting_report(prestatiemeting_id):
    """
    Method to generate Excel report for a prestatiemeting
    @param prestatiemeting_id: the id of the prestatiemeting
    @return: Excel workbook
    """
    # required data
    prestatiemeting = Prestatiemeting.objects.get(pk=prestatiemeting_id)
    results_on = PrestatiemetingResult.objects.filter(prestatiemeting=prestatiemeting, question__about='ON')
    results_og = PrestatiemetingResult.objects.filter(prestatiemeting=prestatiemeting, question__about='OG')

    themes = PrestatiemetingTheme.objects.exclude(theme='Open vraag')

    # workbook in memory
    output = io.BytesIO()

    # Create workbook and add a worksheet
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Style formats
    theme_color_list = ['#ffff00', '#cfc', '#f90', '#9cf', '#008000', '#800080']

    header_format = workbook.add_format()
    header_format.set_font_size(20)
    header_format.set_bg_color('#969696')
    header_format.set_border(2)

    about_header = workbook.add_format()
    about_header.set_font_size(13)
    about_header.set_font_color('white')
    about_header.set_bg_color('#ff8080')
    about_header.set_border(2)
    about_header.set_bold()

    comp_format = workbook.add_format()
    comp_format.set_border(1)

    eindscore_header = workbook.add_format()
    eindscore_header.set_font_size(15)
    eindscore_header.set_bg_color('#c0c0c0')
    eindscore_header.set_border(2)

    score_format = workbook.add_format()
    score_format.set_border(1)
    score_format.set_italic()

    # add static data
    worksheet.merge_range(0, 0, 0, 4, 'Samenvatting beoordeling', header_format)
    worksheet.merge_range(1, 0, 1, 1, 'Beoordeling van opdrachtnemer door opdrachtgever', about_header)
    worksheet.merge_range(1, 3, 1, 4, 'Beoordeling van opdrachtgever door opdrachtnemer', about_header)

    worksheet.merge_range(2, 0, 2, 1, 'Naam beoordeelde opdrachtnemer', comp_format)
    worksheet.merge_range(2, 3, 2, 4, 'Naam beoordeelde opdrachtgever', comp_format)

    worksheet.merge_range(3, 0, 3, 1, 'Istimewa Elektro', comp_format)
    worksheet.merge_range(3, 3, 3, 4, str(prestatiemeting.project.opdrachtgever), comp_format)

    worksheet.write(4, 0, 'Eindscore opdrachtnemer', eindscore_header)
    worksheet.write_number(4, 1, prestatiemeting.get_score_on(), eindscore_header)

    worksheet.write(4, 3, 'Eindscore opdrachtgever', eindscore_header)
    worksheet.write_number(4, 4, prestatiemeting.get_score_og(), eindscore_header)

    # add dyanmic data
    theme_on_start = 6

    for i, theme in enumerate(themes):
        # theme formats
        theme_header = workbook.add_format()
        theme_header.set_font_size(12)
        theme_header.set_bg_color(theme_color_list[i])
        theme_header.set_border(2)
        theme_header.set_border_color('black')

        worksheet.merge_range(theme_on_start, 0, theme_on_start, 1, theme.theme, theme_header)
        worksheet.merge_range(theme_on_start, 3, theme_on_start, 4, theme.theme, theme_header)
        theme_on_start += 1

        on_counter = theme_on_start
        og_counter = theme_on_start

        questions_on = PrestatiemetingQuestion.objects.filter(theme=theme, about='ON', number__in=PrestatiemetingResult
                                                              .objects.filter(prestatiemeting_id=prestatiemeting_id)
                                                              .values_list('question', flat=True))
        questions_og = PrestatiemetingQuestion.objects.filter(theme=theme, about='OG', number__in=PrestatiemetingResult
                                                              .objects.filter(prestatiemeting_id=prestatiemeting_id)
                                                              .values_list('question', flat=True))

        if len(questions_on) > len(questions_og):
            question_amount = len(questions_on)
        else:
            question_amount = len(questions_og)

        for question in questions_on:
            worksheet.write(on_counter, 0, question.description, score_format)
            worksheet.write_number(on_counter, 1, results_on.get(question=question).answer.gradation.score, score_format)
            on_counter += 1

        for question in questions_og:
            worksheet.write(og_counter, 3, question.description, score_format)
            worksheet.write_number(og_counter, 4, results_og.get(question=question).answer.gradation.score, score_format)
            og_counter += 1

        theme_on_start += question_amount

    worksheet.set_column("A:A", 50)
    worksheet.set_column("B:B", 5)
    worksheet.set_column("D:D", 50)
    worksheet.set_column("E:E", 5)

    workbook.close()

    return output









