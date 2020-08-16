from django             import template
from core.dj_import     import mark_safe
from core.utils         import getSubstituteForReturn


# ### if you add a tag, you must register it in config/settings.base!!! ###
# ### if you add a tag, you must register it in config/settings.base!!! ###
# ### if you add a tag, you must register it in config/settings.base!!! ###
# ### if you add a tag, you must register it in config/settings.base!!! ###

register = template.Library()


@register.filter()
def sayListingType( sListType ):
    #
    '''in results, ebay API calls auctions Chinese'''
    #
    if sListType == 'Chinese':
        sListType = 'Auction'
    elif sListType == 'FixedPriceItem':
        sListType = 'FixedPrice'
    #
    return sListType



@register.filter()
def getDashForReturn( s ):
    #
    '''html rendering ignores return characters, substitute dashes'''
    #
    return getSubstituteForReturn( s )



@register.filter()
def getDashForReturnButDropLast( s ):
    #
    '''html rendering ignores return characters, substitute dashes,
       but drop what is after the last return character'''
    #
    return getSubstituteForReturn( s, bOmitLast = True )



@register.filter()
def getLineBreakForReturn( s ):
    #
    '''html rendering ignores return characters, substitute <BR>'''
    #
    return mark_safe( getSubstituteForReturn( s, '<BR>' ) )



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

