from django     import template

from ..utils    import getLastDropped

# ### if you add a tag, you must register it in config/settings.base!!! ###
# ### if you add a tag, you must register it in config/settings.base!!! ###
# ### if you add a tag, you must register it in config/settings.base!!! ###
# ### if you add a tag, you must register it in config/settings.base!!! ###

register = template.Library()


@register.filter()
def getLastDroppedFromCommaSeparatedString( s ):
    #
    return getLastDropped( s )




