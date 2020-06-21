import logging

from json                   import load, loads
from os                     import walk

from pprint                 import pprint

from django.conf            import settings
from django.utils           import timezone

from finders.models         import ItemFound
#
from ebayinfo.models        import EbayCategory, CategoryHierarchy

from searching              import SEARCH_FILES_ROOT

from pyPks.Dict.Get         import getAnyValue
from pyPks.Dict.Maintain    import getDictValuesFromSingleElementLists
from pyPks.File.Get         import getFileSpecHereOrThere
from pyPks.String.Find      import getRegExObj
from pyPks.String.Get       import getContentOutOfDoubleQuotes


logger = logging.getLogger(__name__)

''' prints logging messages to terminal
logging_level = logging.WARNING

logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.WARNING)
'''

class ItemAlreadyInTable(    Exception ): pass
class SearchGotZeroResults(  Exception ): pass

oLocationSqueezer = getRegExObj( ', *|\., *' )


_iLocationLen = ItemFound._meta.get_field('cLocation').max_length


def _getLocationShorter( sLocation ):
    #
    sMaybeShorter = ','.join( oLocationSqueezer.split( sLocation ) )
    #
    return sMaybeShorter[ : _iLocationLen - 1 ]



def storeItemInfo( dItem, dFields, Form, getValue, **kwargs ):
    #
    '''can store a row in either ItemFound or UserItemFound
    note that when testing against the live ebay api,
    form errors are common,
    not all real categories are in the test database'''
    #
    fBeforeForm         = kwargs.pop( 'fBeforeForm', None )
    dEbayCatHierarchies = kwargs.pop( 'dEbayCatHierarchies', {} )
    #
    dNewResult = { k: getValue( dItem, k, v, **kwargs )
                   for k, v in dFields.items() }
    #
    dNewResult.update( kwargs )
    #
    # ebay category info
    # iCategoryID is ebay's category number & it may not be unique
    # iCategoryID + iEbaySiteID are unique
    # hence bot's ebayinfo EbayCategory table has id column as primary key
    # EbayCategory table is slow (mptt heirarchical table)
    # bot needs string category heirarchy,
    # got that in bot's ebayinfo CategoryHierarchy table
    # bot does not need reference to ebayinfo EbayCategory table
    #
    dNewResult['iCategoryID'   ] = None
    dNewResult['i2ndCategoryID'] = None
    #
    # if 'cLocation' in dNewResult: # ItemFound
    #
    # ebay can return a string that is longer than the length of the field
    #
    sLocation = dNewResult.get( 'cLocation', '' )
    #
    if len(sLocation) > _iLocationLen:
        #
        dNewResult['cLocation'] = _getLocationShorter( sLocation )
        #
    #
    #
    dNewResult['tCreate'] = timezone.now()
    # 2019-03-25 cannot! auto_now_add, hope to get consistent index listings
    #
    if fBeforeForm: fBeforeForm( dNewResult )
    #
    form = Form( data = dNewResult )
    #
    iSavedRowID = None
    #
    if form.is_valid():
        #
        oForm = form.save()
        #
        iSavedRowID = oForm.pk
        #
    else:
        #
        if (    'iItemNumb' in form.errors and
                len( form.errors ) == 1 ):
            #
            raise ItemAlreadyInTable(
                'Item %s already in table' % dNewResult['iItemNumb'] )
            #
        else:
            #
            # ### form errors when testing are common,
            # ### not all real categories are in the test database
            #
            # print( 'dNewResult["iCategoryID"]:', dNewResult['iCategoryID'] )
            #
            if 'iItemNumb' in dNewResult:
                sMsg = ('form did not save for item %s' %
                        dNewResult['iItemNumb'] )
            else:
                sMsg = ('searching: form did not save' )
            logger.error( sMsg )
            #print( '' )
            #print( 'log this error, form did not save' )
            #
            if form.errors:
                for k, v in form.errors.items():
                    logger.warning( '%s -- %s' % ( k, str(v) ) )
                    # print( k, ' -- ', str(v) )
            else:
                logger.info( 'no form errors at bottom!' )
            #
            #tProblems = ( 'iItemNumb', 'cMarket', 'iCategoryID', 'cCategory',
            #            'iCat***Heirarchy', 'i2ndCategoryID', 'c2ndCategory',
            #            'i2nd***CatHeirarchy', 'cCountry' )
            #
            #print( '' )
            #print( 'fields with errors:' )
            #for sField in tProblems:
            #    print( 'dNewResult["%s"]:' % sField, dNewResult.get( sField ) )
    #
    return iSavedRowID





def getJsonFindingResponse( uContent ):
    #
    '''pass in the response
    returns the resonse dictionary dResponse
    which includes dPagination for convenience'''
    #
    try:
        dResults = load(  uContent ) # this is for file pointers
    except AttributeError:
        dResults = loads( uContent ) # this is for strings
    #
    lResponse = getAnyValue( dResults ) # should be only 1 value to get
    #
    if lResponse is None or len( lResponse ) != 1:
        #
        raise SearchNotWorkingError( 'content of "%s" invalid' % sFile )
        #
    #
    dResponse = lResponse[0]
    #
    if dResponse.get( "ack" ) != ["Success"]:
        #
        if "ack" in dResponse:
            #
            sMessage = 'ack returned "%s"' % dResponse[ "ack" ][0]
            #
        elif "error" in dResponse:
            #
            sMessage = 'error message, check file'
            #
        else:
            #
            sMessage = 'unknown error, check file'
            #
        raise SearchNotWorkingError( sMessage )
        #
    #
    dPagination = dResponse[ "paginationOutput" ][0]
    #
    # do not apply getDictValuesFromSingleElementLists directly to dResponse!
    #### if the search finds only one item, the function trashes it! ###
    #
    getDictValuesFromSingleElementLists( dPagination )
    #
    iTotalEntries   = int( dPagination[ "totalEntries" ] )
    #
    iPages          = int( dPagination[ "totalPages" ] )
    #
    iEntriesPP      = int( dPagination[ "entriesPerPage" ] )
    #
    iPageCount      = 0
    #
    lCount          = dResponse.get('searchResult', [] )
    #
    if lCount:
        #
        dCount      = lCount[0]
        #
        iPageCount  = int( dCount.get( '@count', 0 ) )
        #
    #
    dPagination['iTotalEntries'] = iTotalEntries
    dPagination['iPages'       ] = iPages
    dPagination['iEntriesPP'   ] = iEntriesPP
    dPagination['iPageCount'   ] = iPageCount
    #
    dResponse[  'dPagination'  ] = dPagination
    #
    return dResponse


def _getUpToDoubleQuote( s ):
    #
    return s.split( '"', maxsplit = 1 )[0]



def getSearchResult( sResponse ):
    #
    '''retrieve the ack value from the response text'''
    #
    lParts      = sResponse.split( '"ack":["' )
    #
    sSuccessOrNot = ''
    #
    if len( lParts ) > 1:
        #
        sSuccessOrNot = _getUpToDoubleQuote( lParts[1] )
        #
    else:
        #
        lParts = sResponse.split( '"errorMessage"' )
        #
        if len( lParts ) > 1:
            #
            sSuccessOrNot = getContentOutOfDoubleQuotes( lParts[1] )
            #
    #
    return sSuccessOrNot



def getSuccessOrNot( sResponse ):
    #
    '''determine whether the request was a success from the response text'''
    #
    return getSearchResult( sResponse ) == 'Success'



def getPagination( sResponse ):
    #
    '''get the "pagination" info such as total pages and number of this page
    from the response text, returns dPagination '''
    #
    sThisCount      = '0'
    #
    sEnd = sResponse[ -500 : ] # last 500 chars
    #
    lCountParts     = sEnd.split( '"@count":"' )
    lPageParts      = sEnd.split( '"paginationOutput":' )
    #
    if len( lCountParts ) == 1: # count can be either place
        #
        lCountParts = sResponse.split( '"@count":"' )
        #
    #
    if len( lCountParts ) > 1:
        #
        sThisCount  = _getUpToDoubleQuote( lCountParts[1] )
        #
    #
    if len( lPageParts ) == 1:
        #
        # try beginning
        #
        lPageParts  = sResponse.split( '"paginationOutput":' )
        #
    #
    if len( lPageParts ) > 1:
        #
        sContent        = lPageParts[1]
        #
        lPageParts      = sContent.split( '"pageNumber":["' )
        #
        sPageNumb       = _getUpToDoubleQuote( lPageParts[1] )
        #
        lPageParts      = sContent.split( '"entriesPerPage":["' )
        #
        sEntriesPP      = _getUpToDoubleQuote( lPageParts[1] )
        #
        lPageParts      = sContent.split( '"totalPages":["' )
        #
        sPages          = _getUpToDoubleQuote( lPageParts[1] )
        #
        lPageParts      = sContent.split( '"totalEntries":["' )
        #
        sTotalEntries   = _getUpToDoubleQuote( lPageParts[1] )
        #
        dPagination = dict(
            iPageCount      = int( sThisCount   ),
            iTotalEntries   = int( sTotalEntries),
            iPages          = int( sPages       ),
            iEntriesPP      = int( sEntriesPP   ),
            iPageNumb       = int( sPageNumb    ) )
        #
    else:
        #
        dPagination = dict(
            iPageCount      = int( sThisCount ),
            iTotalEntries   = None,
            iPages          = None,
            iEntriesPP      = None,
            iPageNumb       = None )
        #
    #
    return dPagination



''' not needed
def getItemSearchURL( sResponse ):
    #
    lParts = sResponse.split( 'itemSearchURL":["' )
    #
    sItemSearchURL = ''
    #
    if len( lParts ) > 1:
        #
        sItemSearchURL = _getUpToDoubleQuote( lParts[1] )
        #
    #
    return sItemSearchURL
'''


def _getSplitters():
    #
    tTopLevelSplitters = (
            '"itemId":["',
            '"title":["',
            '"globalId":["',
            '"location":["',
            '"country":["',
            '"postalCode":["',
            '"galleryURL":["',
            '"viewItemURL":["' )
    #
    dSplits = {}
    #
    for sSplitter in tTopLevelSplitters:
        #
        dSplits[ sSplitter ] = None
        #
    #
    dSplits['"listingInfo":[' ] = (
            '"listingType":["',
            '"gift":["',
            '"bestOfferEnabled":["',
            '"startTime":["',
            '"buyItNowAvailable":["',
            '"watchCount":["',
            '"endTime":["' )
    #
    dSplits['"primaryCategory":['] = (
            '"categoryId":["',
            '"categoryName":["' )
    #
    dSplits['"secondaryCategory":['] = (
            '"categoryId":["',
            '"categoryName":["' )
    #
    dSplits['"condition":['] = (
            '"conditionId":["',
            '"conditionDisplayName":["' )
    #
    dSelling = {}
    #
    dSelling['"currentPrice":['] = (
            '"@currencyId":"',
            '"__value__":"' )
    dSelling['"convertedCurrentPrice":['] = (
            '"@currencyId":"',
            '"__value__":"' )
    dSelling['"sellingState":["'] = None
    dSelling['"bidCount":["']     = None
    dSelling['"timeLeft":["']     = None
    #
    dSplits['"sellingStatus":['] = dSelling
    #
    return dSplits


_dSplitters = _getSplitters()


def _getReponseKeyValue( sContent, sSplitOn, uSplitterValue ):
    #
    uValue = sValueName = ''
    #
    lParts = sContent.split( sSplitOn )
    #
    if len( lParts ) == 1:
        #
        # must be an optional field not in this record
        #
        sValueName, uValue = '', ''
        #
    else:
        #
        lNameParts  = sSplitOn.split( '"' )
        #
        sValueName  = lNameParts[1]
        #
        if uSplitterValue is None:
            #
            uValue  = _getUpToDoubleQuote( lParts[1] )
            #
        elif isinstance( uSplitterValue, dict ):
            #
            dSub = {}
            #
            for sSplit, uSubValue in uSplitterValue.items():
                #
                sSubValueName, sValue = _getReponseKeyValue( sContent, sSplit, uSubValue )
                #
                dSub[ sSubValueName ] = sValue
                #
            #
            uValue = dSub
            #
        elif isinstance( uSplitterValue, tuple ):
            #
            dSub = {}
            #
            for sSplit in uSplitterValue:
                #
                sSubValueName, sValue = _getReponseKeyValue( sContent, sSplit, None )
                #
                dSub[ sSubValueName ] = sValue
                #
            #
            uValue = dSub
            #
        #
    #
    return sValueName, uValue



def _getFindingResponseGenerator( sResponse ): # json.load is faster
    #
    '''lazy finding response getter
    json way proved to be faster'''
    #
    sRest = sResponse # will eat sRest
    #
    lParts = sRest.split( '"itemId":["', maxsplit = 1 )
    #
    if len( lParts ) == 1:
        #
        raise StopIteration
        #
    #
    bStillMore = True
    #
    while True:
        #
        if not bStillMore: raise StopIteration
        #
        lParts = sRest.split( '},{', maxsplit = 1 )
        #
        if len( lParts ) == 1:
            #
            bStillMore = False
            #
        else:
            #
            sRest = lParts[1]
            #
        #
        dItem = {}
        #
        sThis = lParts[0]
        #
        for sSplit, uSplitValue in _dSplitters.items():
            #
            sValueName, uValue = _getReponseKeyValue( sThis, sSplit, uSplitValue )
            #
            if sValueName:
                dItem[ sValueName ] = uValue
            #
        #

        yield dItem



def getSearchResultGenerator( sFile, iLastPage, sContent = None ):
    #
    ''' search saves results to file, this returns an interator to set through
    in __init__.py: RESULTS_FILE_NAME_PATTERN = 'Search_%s_%s_ID_%s.json'
    '''
    #
    # circular import problem, this must be here not at top
    from .utils import getPageNumbOffFileName
    #
    if sContent is None:
        #
        iThisPage   = getPageNumbOffFileName( sFile )
        #
        sFile       = getFileSpecHereOrThere( sFile )
        #
        dResponse   = getJsonFindingResponse( open( sFile ) )
        #
    else:
        #
        dResponse   = getJsonFindingResponse( sContent )
        #
    #
    dPagination     = dResponse[  'dPagination'  ]
    #
    iTotalEntries   = dPagination['iTotalEntries']
    #
    iPages          = dPagination['iPages'       ]
    #
    iPageCount      = dPagination['iPageCount'   ]
    #
    if iPages > 1:
        #
        # actually iTotalEntries is a minimum, the actual number of entries is more
        #
        iTotalEntries = (
            1 + ( iPages - 1 ) * dPagination[ "iEntriesPP" ] )
        #
    #
    if iTotalEntries == 0:
        #
        if iLastPage > 0 and iThisPage == iLastPage:
            #
            # ebay sometimes gives zero results on the last of several pages
            #
            lResults = () # empty tuple will raise StopIteration
            #
        else:
            #
            ## FixMe! zero results are more common now
            #
            # raise SearchGotZeroResults(
            #            "search executed OK but returned zero items, "
            #            "try this and look carefully: %s" %
            #        dResponse["itemSearchURL"][0] )
            #
            lResults = () # empty tuple will raise StopIteration
            #
        #
    elif iPageCount == 0:
            #
            lResults = () # empty tuple will raise StopIteration
            #
    else: # iTotalEntries > 0
        #
        dResultDict = dResponse[ "searchResult" ][0]
        #
        lResults = dResultDict.get('item')
        #
    #
    iThisItem = 0
    #
    for dItem in lResults:
        #
        iThisItem += 1
        #
        getDictValuesFromSingleElementLists( dItem )
        #
        dPagination["thisEntry"] = str( iThisItem )
        #
        dItem["paginationOutput"]= dPagination
        #
        yield dItem



def getSearchRootFolders():
    #
    '''get the list of directories under SEARCH_FILES_ROOT'''
    #
    return next( t[1] for t in walk( SEARCH_FILES_ROOT ) if t[1] )



