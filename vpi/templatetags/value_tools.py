from django.template.defaulttags import register
from vpi.models import VPI


@register.filter
def color(vpi, value):
    return vpi.get_color(value)
