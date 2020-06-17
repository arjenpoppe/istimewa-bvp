from django.template.defaulttags import register


@register.filter
def highest(dictionary, key):
    """
    Get highest value from a dictionary in a template
    @param dictionary: dictionary
    @param key: what key to look for
    @return: value
    """
    values = []
    for item in dictionary:
        values.append(item[key])
    return max(values)


@register.filter
def lowest(dictionary, key):
    """
    Get lowest value from a dictionary in a template
    @param dictionary: dictionary
    @param key: what key to look for
    @return: value
    """
    values = []
    for item in dictionary:
        values.append(item[key])
    return min(values)


@register.filter
def average(dictionary, key):
    """
    Get average value from a dictionary in a template
    @param dictionary: dictionary
    @param key: what key to look for
    @return: value
    """
    total = 0
    for item in dictionary:
        total += item[key]
    return total / len(dictionary)
