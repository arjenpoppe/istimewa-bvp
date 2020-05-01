from data.models.prestatiemeting import Prestatiemeting, PrestatiemetingResult


def calc_prestatiemeting(pm_id=1, about='ON'):
    pm = Prestatiemeting.objects.get(id=pm_id)
    result_list = PrestatiemetingResult.objects.filter(prestatiemeting=pm).filter(question__about=about)

    total = 0
    for result in result_list:
        rw = result.question.weight / 100
        total += rw * result.answer.gradation.score
        print(rw * result.answer.gradation.score)

    return total
