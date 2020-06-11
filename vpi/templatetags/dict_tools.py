from django.template.defaulttags import register


@register.filter
def highest(dictionary, key):
    values = []
    for item in dictionary:
        values.append(item[key])
    return max(values)


@register.filter
def lowest(dictionary, key):
    values = []
    for item in dictionary:
        values.append(item[key])
    return min(values)


@register.filter
def average(dictionary, key):
    total = 0
    for item in dictionary:
        total += item[key]
    return total / len(dictionary)
