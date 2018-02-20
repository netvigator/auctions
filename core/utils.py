# misc utils can go here
from django.db.models       import ForeignKey

from String.Find            import getFinderFindAll

#                "2017-12-15T05:22:47.000Z"
EBAY_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'

oInParensFinder = getFinderFindAll( '\(.*\)' )

def getNamerSpacer( sRootTag, sXmlNameSpace = 'urn:ebay:apis:eBLBaseComponents' ):
    #
    '''for extracting values from xml files returned by ebay'''
    #
    sNameSpaceTag   = '{%s}%s'
    #
    sNamerSpacer    = sNameSpaceTag % ( sXmlNameSpace, '%s' )
    #
    sRootNameSpTag  =  sNameSpaceTag % ( sXmlNameSpace, sRootTag )
    #
    return sNamerSpacer, sRootNameSpTag


def getDateTimeObjGotEbayStr( sDateTime ):
    #
    '''convert ebay string dates into python datetime objects'''
    #
    from Time.Convert import getDateTimeObjFromString
    #
    #
    return getDateTimeObjFromString( sDateTime, EBAY_DATE_FORMAT )


def getLastDictFromResponse( oResponse ):
    #
    l = oResponse.__dict__['context']
    #
    oLast = l[-1]
    #
    return oLast.dicts[-1]


def getExceptionMessageFromResponse( oResponse ):
    #
    '''
    exception message is burried in the response object,
    here is my struggle to get it out
    '''
    #
    dLast = getLastDictFromResponse( oResponse )
    #
    return dLast.get( 'exception' )


# Iterate over model instance field names and values in template
# https://stackoverflow.com/a/14625776/6366075
def model_to_dict(instance):
    dObj = {}
    for field in instance._meta.fields:
        dObj[field.name] = field.value_from_object(instance)
        if isinstance(field, ForeignKey):
            dObj[field.name] = field.rel.to.objects.get(pk=dObj[field.name])
    return dObj


def _getReverseWithQuery( lookup_view, *args, **kwargs ):
    #
    from django.core.urlresolvers   import reverse
    from django.utils.http          import urlencode
    #
    query = kwargs.pop( 'query' )
    #
    url = reverse( lookup_view, kwargs = kwargs )
    #
    if query:
        #
        url = '%s%s%s' % ( url, '?', urlencode( query ) )
        #
    #
    return url


def _getIsoDateTimeOffDateTimeCol( tDateTime ):
    #
    from Time           import sFormatISOdateTimeNoColon
    from Time.Output    import getIsoDateTimeFromDateTime
    #
    return tDateTime.strftime( sFormatISOdateTimeNoColon )


def getReverseWithUpdatedQuery( lookup_view, *args, **kwargs ):
    #
    '''solution to browser lack-of-refresh problem!!
    browser lack-of-refresh problem:
    update a record, go back to detail view, and edits do not show up
    because browser is displaying cached version of page
    solution:
    append a unique query string onto the end of the detail page URL
    UTC date/time of the moment will always be unique.
    voila! browser lack-of-refresh problem solved!
    #'''
    #
    from Time.Output import getNowIsoDateTimeFileNameSafe
    #
    kwargs = kwargs.get( 'kwargs', {} ) # !!!
    #
    tModify = kwargs.pop( 'tModify' )
    #
    dUTC = { 'updated': _getIsoDateTimeOffDateTimeCol( tModify ) }
    #
    kwargs[ 'query' ] = dUTC
    #
    return _getReverseWithQuery( lookup_view, *args, **kwargs )


