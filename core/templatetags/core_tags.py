from django import template
from django.utils.safestring import mark_safe

from Time.Output import getIsoDateTimeFromDateTime

register = template.Library()


@register.filter()
def getIsoDateTime( tDT ):
    #
    '''return non ambigious ISO date time format'''
    #
    return getIsoDateTimeFromDateTime( tDT )


@register.filter()
def getNbsp(value):
    #
    '''substitute &nbsp; for spaces'''
    #
    return mark_safe("&nbsp;".join(value.split(' ')))
 


@register.simple_tag
def model_name(value):
    '''
    Django template tag which returns the verbose name of a model.
    '''
    if hasattr(value, 'model'):
        value = value.model
    
    return value._meta.verbose_name.title()

@register.simple_tag
def model_name_plural(value):
    '''
    Django template tag which returns the plural verbose name of a model.
    '''
    if hasattr(value, 'model'):
        value = value.model
    
    return value._meta.verbose_name_plural.title()

@register.simple_tag
def field_name(value, field):
    '''
    Django template tag which returns the verbose name of an object's,
    model's or related manager's field.
    '''
    if hasattr(value, 'model'):
        value = value.model
    
    return value._meta.get_field(field).verbose_name.title()