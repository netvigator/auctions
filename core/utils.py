# misc utils can go here
from datetime               import timedelta, timezone

from django.db.models       import ForeignKey
from django.utils           import timezone

from String.Find            import getFinderFindAll
from String.Eat             import eatFromWithin

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
    return getDateTimeObjFromString(
            sDateTime, EBAY_DATE_FORMAT, oTimeZone = timezone.utc )


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
    date/time of the last update will always be unique when it needs to.
    voila! browser lack-of-refresh problem solved!
    #'''
    #
    from Time.Output import getNowIsoDateTimeFileNameSafe
    #
    kwargs = kwargs.get( 'kwargs', {} ) # !!!
    #
    tModify = kwargs.pop( 'tModify' )
    #
    tUpdatted = { 'updated': _getIsoDateTimeOffDateTimeCol( tModify ) }
    #
    kwargs[ 'query' ] = tUpdatted
    #
    return _getReverseWithQuery( lookup_view, *args, **kwargs )


def getWhatsLeft( s ):
    #
    return eatFromWithin( s, oInParensFinder ).strip()



def getSeqStripped( l ): return ( s.strip() for s in l )



def updateMemoryTableUpdated( sTable, sField = None ):
    #
    if (    sTable == 'markets' and
            sField is not None  and sField == 'iCategoryVer' ):
        #
        import ebayinfo.utils
        #
        t = ebayinfo.utils._getDictMarket2SiteID()
        #
        dMarket2SiteID, dSiteID2Market, dSiteID2ListVers = t
        #
        ebayinfo.utils.dSiteID2ListVers = dSiteID2ListVers
        #


def getBegTime( bConsoleOut = False ):
    #
    tBeg = timezone.now()
    #
    if bConsoleOut:
        #
        print( 'Beg:', str( tBeg )[:19] )
        #
    #
    return tBeg



def sayDuration( tBeg ):
    #
    tEnd = timezone.now()
    #
    print( 'End:', str( tEnd )[:19] )
    #
    lDuration = str( tEnd - tBeg ).split( '.' )
    #
    print( 'Duration:', lDuration[0] )


def getShrinkItemURL( sURL ):
    #
    lParts = sURL.split( '/' )
    #
    if lParts[3] == 'itm':
        #
        lParts[4] = 'b'
        #
    #
    return ( '/' ).join( lParts )


def getOldRecordToRecycleGenerator( oModel, iHowOld, sDateTimeField ):
    #
    tOlderThan = timezone.now() - timedelta( days = iHowOld )
    #
    sDateTimeFilter = '%s__lte' % sDateTimeField
    #
    qsOldRecors = oModel.objects.filter(
                    **{ sDateTimeFilter : tOlderThan }
                    ).order_by( sDateTimeField )
    #
    for oRow in qsOldRecors:
        #
        yield oRow


def getDownloadFileWriteToDisk( sURL, sWriteToFile = None ):
    #
    '''utility for fetching ebay item pictures'''
    #
    from shutil     import copyfileobj
    from requests   import get
    #
    if sWriteToFile is None:
        #
        sWriteToFile = sURL.split('/')[-1]
        #
    #
    sResult = 'unknown'
    #
    with get( sURL, stream=True ) as r:
        #
        if 'X-EBAY-C-EXTENSION' in r.headers:
            #
            sResult = r.headers[ 'X-EBAY-C-EXTENSION' ]
            #
        elif r.status_code != 200:
            #
            sResult = r.status_code
            #
        elif r.headers.get( 'Content-Type', '' ).startswith( 'image' ):
            #
            with open( sWriteToFile, 'wb' ) as f:
                copyfileobj( r.raw, f )
            #
            sResult = sWriteToFile
            #
        #
    return sResult
