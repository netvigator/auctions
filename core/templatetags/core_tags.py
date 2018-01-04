from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def getNbsp(value):
    #
    '''substitute &nbsp; for spaces'''
    #
    return mark_safe("&nbsp;".join(value.split(' ')))
 
