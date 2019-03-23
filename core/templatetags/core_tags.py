from django import template
from django.utils.safestring import mark_safe

from String.Find import oFinderCRorLF
from Time.Output import getIsoDateTimeFromDateTime

# ### if you add a tag, you must register it in config/settings.base!!! ###

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


@register.filter()
def getDashForReturn( s ):
    #
    '''html rendering ignores return characters, substitute dashes'''
    #
    if s:
        #
        l = oFinderCRorLF.split( s )
        #
        return ' - '.join( ( s for s in l if s ) )
        #
    else:
        return '' # run replace on None and you get an error



@register.filter()
def getDashForReturnButDropLast( s ):
    #
    '''html rendering ignores return characters, substitute dashes,
       but drop what is after the last return character'''
    #
    if s:
        #
        l = oFinderCRorLF.split( s )
        #
        return ' - '.join( l[:-1] )
        #
    else:
        #
        return '' # run replace on None and you get an error



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


@register.assignment_tag
def define(val=None):
    #
    '''set a variable on the fly in html
    from https://stackoverflow.com/questions/1070398/how-to-set-a-value-of-a-variable-inside-a-template-code'''
    #
    return val
