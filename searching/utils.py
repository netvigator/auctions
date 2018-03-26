from logging                import getLogger

from core.utils_ebay        import getValueOffItemDict

from django.conf            import settings
from django.db              import DataError
from django.utils           import timezone

from ebayinfo.utils         import dMarket2SiteID, getEbayCategoryHierarchies

from .models                import ItemFound, UserItemFound, SearchLog

logger = getLogger(__name__)

class SearchNotWorkingError( Exception ): pass
class SearchGotZeroResults(  Exception ): pass
class ItemAlreadyInTable(    Exception ): pass



def _storeEbayInfo( dItem, dFields, tSearchTime, Form, getValue, **kwargs ):
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
                logger.error( '%s -- %s' % ( k, str(v) ) )
                #print( k, ' -- ', str(v) )
        else:
            logger.info( 'no form errors at bottom!' )
        #
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



def getSearchResultGenerator( sFile ):
    #
    ''' search saves results to file, this returns an interator to set through
    in __init__.py: RESULTS_FILE_NAME_PATTERN = 'Search_%s_%s_ID_%s.json'
    '''
    #
    from Dict.Maintain  import getDictValuesFromSingleElementLists
    from File.Get       import getFileSpecHereOrThere
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
    if not iEntries:
        #
        raise SearchGotZeroResults( "search executed OK but returned no items" )
        #
    #
    dResultDict = dResponse[ "searchResult" ][0]
    #
    iThisItem = 0
    #
    lResults = dResultDict.get('item')
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



def _putPageNumbInFileName( sFileName, iThisPage ):
    #
    lParts = sFileName.split( '_' )
    #
    #   0         1          2            3     4    5    6      7
    # ['Search', 'EBAY-US', 'username1', 'ID', '8', 'p', '000', '.json']
    #
    sThisPage = str( iThisPage ).zfill( 3 )
    #
    lParts[6] = sThisPage
    #
    return '_'.join( lParts )




def _getSearchResults( iSearchID = None, bUseSandbox = False ):
    #
    '''sends search request to the ebay API, stores the response in /tmp'''
    #
    from os.path                import join
    from time                   import sleep
    #
    from django.contrib.auth    import get_user_model
    #
    from core.ebay_api_calls    import findItems
    #
    from searching              import RESULTS_FILE_NAME_PATTERN
    from .models                import Search
    from ebayinfo.models        import Market
    #
    from File.Write             import QuietDump
    from String.Split           import getWhiteCleaned
    #
    User = get_user_model()
    #
    if iSearchID is None:
        #
        oSearch = Search.objects.filter( iUser_id = 1 ).first()
        #
    else:
        #
        # Two Sccops recommends AGAINST passin objects to async processes
        # instead, only pass json serializable values
        # (integers, floats, strings, lists, tuples and dictionaries)
        # so passing a user object is not good.
        #
        oSearch = Search.objects.get( pk = iSearchID )
        #
    #
    oUser       = User.objects.get( id = oSearch.iUser.id )
    #
    oMarket = Market.objects.get( iEbaySiteID = oUser.iMarket_id )
    #
    sMarket             = oMarket.cMarket
    #
    sUserName           = oUser.username
    #
    sKeyWords           = ''
    #
    if oSearch.cKeyWords:
        sKeyWords       = getWhiteCleaned( oSearch.cKeyWords )
    #
    sEbayCategory       = ''
    #
    if oSearch.iEbayCategory:
        sEbayCategory   = str( oSearch.iEbayCategory.iCategoryID )
    #
    tSearch = ( oSearch.cTitle, str( oSearch.id ) )
    #
    # getJsonFindingResponse
    # pass in the response
    # returns the resonse dictionary dResponse
    # which includes dPagination for convenience
    #
    sFileName           = (
            RESULTS_FILE_NAME_PATTERN %
                ( sMarket, sUserName, oSearch.id, '000') )
    #  'Search_%s_%s_ID_%s.json'
    #
    if sKeyWords and sEbayCategory:
        #
        logger.info(
            'executing "%s" search (ID %s) for keywords in category ...' %
            tSearch )
        #
    elif sKeyWords:
        #
        logger.info(
            'executing "%s" search (ID %s) for keywords '
            '(in all categories) ...' % tSearch )
        #
    elif sEbayCategory:
        #
        logger.info(
            'executing "%s" search (ID %s) in category '
            '(without key words) ...' % tSearch )
        #
    #
    iThisPage  = 0
    iWantPages = 1
    #
    while iThisPage <= iWantPages:
        #
        sResponse = findItems(
                        sKeyWords   = sKeyWords,
                        sCategoryID = sEbayCategory,
                        sMarketID   = sMarket,
                        iPage       = iThisPage, # will ignore if < 1
                        bUseSandbox = bUseSandbox )
        #
        dPagination = getPagination( sResponse )
        #
        '''
        dPagination = dict(
            iCount      = int( sCount     ),
            iEntries    = int( sEntries   ),
            iPages      = int( sPages     ),
            iEntriesPP  = int( sEntriesPP ),
            iPageNumb   = int( sPageNumb  ) )
        '''
        #
        if dPagination["iPages"] > 1 and iThisPage == 0:
            #
            iThisPage = dPagination["iPageNumb"]
            #
        #
        if iThisPage > 0:
            sFileName = _putPageNumbInFileName( sFileName, iThisPage )
        #
        QuietDump( sResponse, sFileName )
        #
        iWantPages = dPagination["iPages"]
        #
        iThisPage += 1
        #
        if iThisPage <= iWantPages: sleep(1)
        #
    #
    logger.info(
        'completed without error "%s" search (ID %s)' % tSearch )
    #
    sFileName = join( '/tmp', sFileName )
    #
    return sFileName



'''
oIter = getSearchResultGenerator( sFullFileSpec )




#
sGot = eatFromWithin( 'This is for real (but not yet)', oInParensFinder )
#
'''


def _getValueUserOrOther( k, dItem, dFields, oUser = None, **kwargs ):
    #
    if k == 'iUser':
        return oUser.id
    elif k in kwargs:
        return kwargs[ k ]
    else:
        return getValueOffItemDict( k, dItem, dFields )







def _storeItemFound( dItem, tSearchTime, dEbayCatHierarchies = {} ):
    #
    from .forms         import ItemFoundForm
    #
    from searching      import dItemFoundFields # in __init__.py
    #
    from ebayinfo.models import CategoryHierarchy
    #
    #
    iItemID         = int(            dItem['itemId'  ] )
    iSiteID         = dMarket2SiteID[ dItem['globalId'] ]
    #
    bAlreadyInTable = ItemFound.objects.filter( iItemNumb = iItemID ).exists()
    #
    if bAlreadyInTable:
        #
        raise ItemAlreadyInTable(
                'ItemID %s is already in the ItemFound table' % iItemID )
        #
    #
    iCount = CategoryHierarchy.objects.all().count()
    #
    tCatHeirarchies = getEbayCategoryHierarchies( dItem, dEbayCatHierarchies )
    #
    if settings.TESTING and isinstance( tCatHeirarchies[0], str ):
        #
        # test database does not have all categories
        #
        # skip this one
        #
        iSavedRowID = None
        #
    else:
        #
        iSavedRowID = _storeEbayInfo(
                        dItem,
                        dItemFoundFields,
                        tSearchTime,
                        ItemFoundForm,
                        getValueOffItemDict,
                        iCatHeirarchy   = tCatHeirarchies[0],
                        i2ndCatHeirarchy= tCatHeirarchies[1],
                        iMarket         = iSiteID )
        #
    #
    return iSavedRowID




def _storeUserItemFound( dItem, iItemNumb, tSearchTime, oUser, iSearch ):
    #
    from .forms     import UserItemFoundForm
    from searching  import dUserItemFoundFields # in __init__.py
    #
    bAlreadyInTable = UserItemFound.objects.filter(
                            iItemNumb   = iItemNumb,
                            iUser       = oUser ).exists()
    #
    if bAlreadyInTable:
        #
        raise ItemAlreadyInTable(
                'ItemFound %s is already in the UserItemFound table for %s' %
                ( iItemNumb, oUser.username ) )
        #
    #
    return _storeEbayInfo(
                dItem,
                dUserItemFoundFields,
                tSearchTime,
                UserItemFoundForm,
                _getValueUserOrOther,
                oUser       = oUser,
                iItemNumb   = iItemNumb,
                iSearch     = iSearch )



def _doSearchStoreResults( iSearchID     = None,
                           sFileName     = None,
                           tSearchTime   = None,
                           bUseSandbox   = False ):
    #
    '''put search results in the database
    can do a search, or use the results file from completed ebay API request
    pass Search ID to search ebay via the api, or pass
    a file name to process the results of a prior search'''
    #
    from django.contrib.auth import get_user_model
    #
    from String.Get import getTextBefore
    #
    User = get_user_model()
    #
    if sFileName is None:
        #
        sFileName = _getSearchResults( iSearchID, bUseSandbox = bUseSandbox )
        #
    #
    # 'Search_%s_%s_ID_%s_p_%s_.json' % ( sMarket, sUserName, oSearch.id, iPageNumb ) )
    #
    lFileNameParts = sFileName.split( '_' )
    #
    sUserName   =      lFileNameParts[2]
    iSearch     = int( lFileNameParts[4] )
    iLastPage   = int( lFileNameParts[6] )
    #
    iStartPage  = int( bool( iLastPage > 0 ) ) # 0 if iLastPage == 0, else 1
    #
    tRangeArgs  = ( iStartPage, iLastPage + 1 )
    #
    iItems = iStoreItems = iStoreUsers = 0
    #
    oUser = User.objects.get( username = sUserName )
    #
    for iThisPage in range( *tRangeArgs ):
        #
        sThisPage           = str( iThisPage ).zfill( 3 )
        #
        lFileNameParts[6]   = sThisPage
        #
        sThisFileName       = '_'.join( lFileNameParts )
        #
        # if iLastPage > 0:
        #     print( 'doing %s, page %s of %s' %
        #             ( sFileName, sThisPage, iLastPage ) )
        #
        oItemIter = getSearchResultGenerator( sThisFileName )
        #
        dEbayCatHierarchies = {}
        #
        for dItem in oItemIter:
            #
            iItems += 1
            #
            iItemNumb = None
            #
            try:
                iItemNumb = _storeItemFound(
                                dItem, tSearchTime, dEbayCatHierarchies )
                iStoreItems += 1
            except ItemAlreadyInTable:
                #
                iItemNumb      = int( dItem['itemId'] )
                #
            except ValueError as e:
                #
                logger.error( 'ValueError: %s | %s' %
                            ( str(e), repr(dItem) ) )
            #
            if iItemNumb is not None:
                #
                try:
                    _storeUserItemFound(
                            dItem, iItemNumb, tSearchTime, oUser, iSearch )
                    iStoreUsers += 1
                except ItemAlreadyInTable:
                    pass
                #
            #
        #
    #
    return iItems, iStoreItems, iStoreUsers



def trySearchCatchExceptions(
            iSearchID   = None,
            sFileName   = None,
            bUseSandbox = False ):
    #
    '''high level script, does a search, catches exceptions, logs errors'''
    #
    # ### sandbox returns zero items ### 
    # ### use bUseSandbox = False    ### 
    #
    iItems = iStoreItems = iStoreUsers = 0
    #
    tSearchStart = timezone.now()
    #
    try:
        t = _doSearchStoreResults(
                    iSearchID   = iSearchID,
                    sFileName   = sFileName,
                    tSearchTime = tSearchStart,
                    bUseSandbox = bUseSandbox )
        #
        # ### sandbox returns zero items ### 
        # ### use bUseSandbox = False    ### 
        #
        iItems, iStoreItems, iStoreUsers = t
        #
    except SearchNotWorkingError as e:
        logger.error( 'SearchNotWorkingError: %s' % e )
    except SearchGotZeroResults as e:
        logger.error( 'SearchGotZeroResults: %s' % e )
    #
    if iSearchID is None:
        #
        lFileNameParts = sFileName.split( '_' )
        #
        iSearchID = int( lFileNameParts[4] )
        #
    #
    oSearchLog = SearchLog(
            iSearch_id  = iSearchID,
            tSearchTime = tSearchStart,
            iItems      = iItems,
            iStoreItems = iStoreItems,
            iStoreUsers = iStoreUsers )
    #
    oSearchLog.save()
    #
    return iItems, iStoreItems, iStoreUsers



