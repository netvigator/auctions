from builtins               import ConnectionResetError
from datetime               import timedelta
from urllib3.exceptions     import ProtocolError

from django.conf            import settings
from django.db.models       import ForeignKey
from django.utils           import timezone
from django.urls            import reverse
from django.utils.http      import urlencode

from requests.exceptions    import ConnectionError

from pyPks.Collect.Output   import getTextSequence
from pyPks.String.Find      import getFinderFindAll
from pyPks.String.Find      import oFinderCRorLFnMore as oFinderCRorLF
from pyPks.String.Eat       import eatFromWithin
from pyPks.Time             import _sFormatISOdateTimeNoColon
from pyPks.Time.Convert     import ( getDateTimeObjFromString,
                                     getIsoDateTimeFromObj )
from pyPks.Time.Output      import getNowIsoDateTimeFileNameSafe

#                "2017-12-15T05:22:47.000Z"
EBAY_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'

oInParensFinder = getFinderFindAll( '\(.*\)|\[.*\]|\{.*\}' )

if settings.COVERAGE: # ### server crashes if this is in utils_test ###
    #
    # want to test all lines without printing anything
    #
    def maybePrint(   *args ): pass
    def maybePrettyP( *args ): pass
    #
else:
    #
    from pprint import pprint
    #
    maybePrint   = print
    maybePrettyP = pprint
    #

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
    return getDateTimeObjFromString(
            sDateTime, EBAY_DATE_FORMAT, oTimeZone = timezone.utc )



def getEbayStrGotDateTimeObj( oDateTime ):
    #
    '''convert python datetime object into ebay string date'''
    #
    return getIsoDateTimeFromObj( oDateTime, EBAY_DATE_FORMAT )




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
    return tDateTime.strftime( _sFormatISOdateTimeNoColon )


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
    kwargs = kwargs.get( 'kwargs', {} ) # !!!
    #
    tModify = kwargs.pop( 'tModify' )
    #
    tUpdatted = { 'updated': _getIsoDateTimeOffDateTimeCol( tModify ) }
    #
    kwargs[ 'query' ] = tUpdatted
    #
    return _getReverseWithQuery( lookup_view, *args, **kwargs )


def getWhatsNotInParens( s ):
    #
    return eatFromWithin( s, oInParensFinder ).strip()




def updateMemoryTableUpdated( sTable, sField = None ):
    #
    '''
    the idea was to update a live server after ebay categories were update
    but this idea is obsolete, now that
    ebay categories are updated on a separate machine
    the server is taken down, and the new categories are copied in
    '''
    #
    import ebayinfo.utils
    #
    if ( sTable == 'markets' and sField and sField == 'iCategoryVer' ):
        #
        t = ebayinfo.utils._getDictMarket2SiteID()
        #
        dMarket2SiteID, dSiteID2Market, dSiteID2ListVers = t
        #
        ebayinfo.utils.dSiteID2ListVers = dSiteID2ListVers
        #


def sayIsoDateTimeNoTimeZone( tDateTime ):
    #
    return str( tDateTime )[:19]


def getBegTime( bConsoleOut = False ):
    #
    tBeg = timezone.now()
    #
    if bConsoleOut:
        #
        print( 'Beg:', sayIsoDateTimeNoTimeZone( tBeg ) )
        #
    #
    return tBeg



def sayDuration( tBeg ):
    #
    tEnd = timezone.now()
    #
    print( 'End:', sayIsoDateTimeNoTimeZone( tEnd ) )
    #
    lDuration = str( tEnd - tBeg ).split( '.' )
    #
    print( 'Duration:', lDuration[0] )


def getPriorDateTime( iDaysAgo = 1 ):
    #
    return timezone.now() - timezone.timedelta( iDaysAgo )


def getShrinkItemURL( sURL ):
    #
    lParts = sURL.split( '/' )
    #
    if lParts[3] == 'itm':
        #
        # lParts[4] = 'b'
        del lParts[4]
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
    try:
        #
        with get( sURL, stream=True ) as r:
            #
            if 'X-EBAY-C-EXTENSION' in r.headers: # error, returns dict like str
                #
                sResult = r.headers[ 'X-EBAY-C-EXTENSION' ]
                #
            elif r.status_code != 200: # error, catch others?
                #
                sResult = str( r.status_code )
                #
            elif r.headers.get( 'Content-Type', '' ).startswith( 'image' ):
                #
                with open( sWriteToFile, 'wb' ) as f:
                    copyfileobj( r.raw, f )
                #
                sResult = sWriteToFile # file spec
                #
            #
        #
    except ConnectionResetError as e:
        #
        sResult = 'ConnectionResetError: %s' % e
        #
    except ConnectionError as e:
        #
        sResult = 'ConnectionError: %s' % e
        #
    except ProtocolError as e:
        #
        sResult = 'ProtocolError: %s' % e
        #
    #
    return sResult # file spec, dict as str or integer code as str



def getLink( o ):
    #
    if o is None:
        #
        sReturn = 'None'
        #
    else:
        #
        sReturn = '<a href="%s">%s</a>' % ( o.get_absolute_url(), o.cTitle )
        #
    #
    return sReturn


def getSaySequence( l ):
    #
    return getTextSequence( l, sAnd = '&' )


def getSubstituteForReturn( s, sSub = ' - ', bOmitLast = False ):
    #
    if s:
        #
        l = [ s for s in oFinderCRorLF.split( s ) if s ]
        #
        if bOmitLast and len( l ) > 1:
            #
            del l[-1]
            #
        #
        return sSub.join( l )
        #
    else:
        return '' # run replace on None and you get an error

