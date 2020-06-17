from django.template.defaulttags import register
from vpi.models import VPI


@register.filter
def color(vpi, value):
    """
    Get color to reflect the status of a VPI
    @param vpi: VPI object
    @param value: value for VPI
    @return: color ('danger'/'warning'/'success')
    """
    return vpi.get_color(value)
