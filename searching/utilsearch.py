import logging

from string     import ascii_uppercase, digits

# avoiding circular import problems!

logger = logging.getLogger(__name__)

logging_level = logging.INFO

class SearchGotZeroResults(  Exception ): pass

def getPriorityChoices( oModel = None, oUser = None, sInclude = None ):
    #
    '''get list of priorities for Search.cPriority'''
    #
    tAlpha = tuple( ascii_uppercase )
    tNums  = tuple( digits )[1:]
    #
    iterAll = ( '%s%s' % (A, N) for N in tNums for A in tAlpha )
    #
    setAll = set( iterAll )
    #
    if sInclude:
        def doOmitFromChoices( s ): return s != sInclude
    else:
        def doOmitFromChoices( s ): return True
    #
    if oUser is not None and oModel is not None:
        #
        oSearches = oModel.objects.filter( iUser = oUser )
        #
        setAll.difference_update( ( oSearch.cPriority
                                    for oSearch in oSearches
                                    if doOmitFromChoices( oSearch.cPriority ) ) )
        #
    #
    lAll = list( setAll )
    #
    lAll.sort()
    #
    return tuple( ( ( s, s ) for s in lAll ) )
 

ALL_PRIORITIES = getPriorityChoices()




def storeEbayInfo( dItem, dFields, tSearchTime, Form, getValue, **kwargs ):
    #
    '''can store a row in either ItemFound or UserItemFound
    note that when testing against the live ebay api,
    form errors are common,
    not all real categories are in the test database'''
    #
    from ebayinfo.models import CategoryHierarchy
    #
    dNewResult = { k: getValue( k, dItem, dFields, **kwargs ) for k in dFields }
    #
    dNewResult.update( kwargs )
    #
    dNewResult['tCreate'] = tSearchTime
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
        # ### form errors are common,
        # ### not all real categories are in the test database
        #
        #
        sMsg = ('form did not save' )
        #
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
                      #'iCatHeirarchy', 'i2ndCategoryID', 'c2ndCategory',
                      #'i2ndCatHeirarchy', 'cCountry' )
        ##
        #print( '' )
        #print( 'fields with errors:' )
        #for sField in tProblems:
            #print( 'dNewResult["%s"]:' % sField, dNewResult.get( sField ) )
    #
    return iSavedRowID





def getJsonFindingResponse( uContent ):
    #
    '''pass in the response
    returns the resonse dictionary dResponse
    which includes dPagination for convenience'''
    #
    from json           import load, loads
    #
    from Dict.Get       import getAnyValue
    from Dict.Maintain  import getDictValuesFromSingleElementLists
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
    iEntries    = int( dPagination[ "totalEntries" ] )
    #
    iPages      = int( dPagination[ "totalPages" ] )
    #
    iEntriesPP  = int( dPagination[ "entriesPerPage" ] )
    #
    dPagination['iEntries'    ] = iEntries
    dPagination['iPages'      ] = iPages
    dPagination['iEntriesPP'  ] = iEntriesPP
    #
    dResponse[  'dPagination' ] = dPagination
    #
    return dResponse


def _getUpToDoubleQuote( s ):
    #
    return s.split( '"', maxsplit = 1 )[0]



def getSuccessOrNot( sResponse ):
    #
    '''determine whether the request was a success from the response text'''
    #
    lParts      = sResponse.split( '"ack":["' )
    #
    sSuccessOrNot = ''
    #
    if len( lParts ) > 1:
        #
        sSuccessOrNot = _getUpToDoubleQuote( lParts[1] )
        #
    #
    return sSuccessOrNot == 'Success'


def getPagination( sResponse ):
    #
    '''get the "pagination" info such as total pages and number of this page
    from the response text, returns dPagination '''
    #
    sCount          = '0'
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
        sCount      = _getUpToDoubleQuote( lCountParts[1] )
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
        sContent    = lPageParts[1]
        #
        lPageParts  = sContent.split( '"pageNumber":["' )
        #
        sPageNumb   = _getUpToDoubleQuote( lPageParts[1] )
        #
        lPageParts  = sContent.split( '"entriesPerPage":["' )
        #
        sEntriesPP  = _getUpToDoubleQuote( lPageParts[1] )
        #
        lPageParts  = sContent.split( '"totalPages":["' )
        #
        sPages      = _getUpToDoubleQuote( lPageParts[1] )
        #
        lPageParts  = sContent.split( '"totalEntries":["' )
        #
        sEntries    = _getUpToDoubleQuote( lPageParts[1] )
        #
        dPagination = dict(
            iCount      = int( sCount     ),
            iEntries    = int( sEntries   ),
            iPages      = int( sPages     ),
            iEntriesPP  = int( sEntriesPP ),
            iPageNumb   = int( sPageNumb  ) )
        #
    else:
        #
        dPagination = dict(
            iCount      = int( sCount ),
            iEntries    = None,
            iPages      = None,
            iEntriesPP  = None,
            iPageNumb   = None )
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



def getSearchResultGenerator( sFile, iLastPage ):
    #
    ''' search saves results to file, this returns an interator to set through
    in __init__.py: RESULTS_FILE_NAME_PATTERN = 'Search_%s_%s_ID_%s.json'
    '''
    #
    from .utils         import getPageNumbOffFileName
    #
    from Dict.Maintain  import getDictValuesFromSingleElementLists
    from File.Get       import getFileSpecHereOrThere
    #
    iThisPage = getPageNumbOffFileName( sFile )
    #
    sFile = getFileSpecHereOrThere( sFile )
    #
    # findItemsAdvancedResponse
    # findItemsByCategoryResponse
    # findItemsByKeywordsResponse
    #
    dResponse = getJsonFindingResponse( open( sFile ) )
    #
    dPagination = dResponse[  'dPagination']
    #
    iEntries    = dPagination['iEntries'   ]
    #
    iPages      = dPagination['iPages'     ]
    #
    if iPages > 1:
        #
        # actually iEntries is a minimum, the actual number of entries is more
        #
        iEntries = (
            1 + ( iPages - 1 ) * dPagination[ "iEntriesPP" ] )
        #
    #
    if iEntries == 0:
        #
        if iLastPage > 0 and iThisPage == iLastPage:
            #
            # ebay sometimes gives zero results on the last of several pages
            #
            lResults = () # empty tuple will raise StopIteration
            #
        else:
            #
            raise SearchGotZeroResults(
                        "search executed OK but returned zero items, "
                        "try this and look carefully: %s" %
                    dResponse["itemSearchURL"][0] )
            #
        #
    else: # iEntries > 0
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

