import logging

from string             import ascii_letters, digits

from django.conf        import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db          import DataError
from django.utils       import timezone
from core.utils_ebay    import getValueOffItemDict

from ebayinfo.utils     import dMarket2SiteID, getEbayCategoryHierarchies

from .models            import ItemFound, UserItemFound, SearchLog, Search
from .utilsearch        import ( storeEbayInfo, getPagination,
                                 getSearchResultGenerator )

from searching          import RESULTS_FILE_NAME_PATTERN

from File.Del           import DeleteIfExists
from File.Get           import getFilesMatchingPattern
from Numb.Get           import getHowManyDigitsNeeded



logger = logging.getLogger(__name__)

logging_level = logging.INFO

'''
logging.basicConfig(level=logging.loglevel)
this will print logging messages to the terminal
'''
#logging.basicConfig(
    #format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    #level=logging.INFO)

class SearchNotWorkingError( Exception ): pass
class SearchGotZeroResults(  Exception ): pass
class ItemAlreadyInTable(    Exception ): pass



def getHowManySearchDigitsNeeded( iID = None ):
    #
    if iID is None:
        try:
            iID = Search.objects.latest('pk').pk
        except ObjectDoesNotExist: # testing and no search objects yet
            return None
    #
    return getHowManyDigitsNeeded( iID )


def getIdStrZeroFilled( iID, iDigits ):
    #
    return str( iID ).zfill( iDigits )

def getSearchIdStr( iId ):
    #
    iNeedDigits = getHowManySearchDigitsNeeded()
    #
    if iNeedDigits is None: # testing and no search objects yet
        #
        iNeedDigits = getHowManyDigitsNeeded( iId )
        #
    #
    return getIdStrZeroFilled( iId, iNeedDigits )



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



def getPageNumbOffFileName( sFileName ):
    #
    lParts = sFileName.split( '_' )
    #
    #   0         1          2            3     4    5    6      7
    # ['Search', 'EBAY-US', 'username1', 'ID', '8', 'p', '000', '.json']
    #
    return int( lParts[6] )



def _doSearchStoreInFile( iSearchID = None, bUseSandbox = False ):
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
    oUser               = User.objects.get( id = oSearch.iUser.id )
    #
    oMarket = Market.objects.get( iEbaySiteID = oUser.iEbaySiteID_id )
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
    sFileName = (
            RESULTS_FILE_NAME_PATTERN %
                ( sMarket, sUserName, getSearchIdStr( oSearch.id ), '000') )
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
        iWantPages = min( dPagination["iPages"], 100 ) # ebay will do 100 max
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
    return sFileName, oSearch.cTitle



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
    elif not dItem.get( "itemId" ):
        #
        iSavedRowID = None
        #
    else:
        #
        iSavedRowID = storeEbayInfo(
                        dItem,
                        dItemFoundFields,
                        tSearchTime,
                        ItemFoundForm,
                        getValueOffItemDict,
                        iCatHeirarchy   = tCatHeirarchies[0],
                        i2ndCatHeirarchy= tCatHeirarchies[1],
                        iEbaySiteID     = iSiteID )
        #
    #
    return iSavedRowID




def _storeUserItemFound( dItem, iItemNumb, tSearchTime, oUser, iSearch ):
    #
    from .forms     import UserItemFoundUploadForm
    from searching  import dUserItemFoundUploadFields # in __init__.py
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
    return storeEbayInfo(
                dItem,
                dUserItemFoundUploadFields,
                tSearchTime,
                UserItemFoundUploadForm,
                _getValueUserOrOther,
                oUser       = oUser,
                iItemNumb   = iItemNumb,
                iSearch     = iSearch )



def trySearchCatchExceptStoreInFile( iSearchID ):
    #
    '''high level script, does a search, catches exceptions, logs errors,
    stores results in /tmp file'''
    #
    # ### sandbox returns zero items ### 
    # ### use bUseSandbox = False    ### 
    #
    tSearchStart = timezone.now()
    #
    oSearch = Search.objects.get( pk = iSearchID )
    oSearch.tBegSearch = tSearchStart # working
    oSearch.cLastResult= None
    oSearch.tEndSearch = None
    #
    oSearch.save()                    # working
    #
    sLastResult = 'tba'
    #
    sUserName   = oSearch.iUser.username
    sMarket     = oSearch.iUser.iEbaySiteID.cMarket
    #
    sFilePattern= (
            RESULTS_FILE_NAME_PATTERN %
                ( sMarket, sUserName, getSearchIdStr( iSearchID ), '*') )
    #
    lGotFiles   = getFilesMatchingPattern( '/tmp', sFilePattern )
    #
    for sFile in lGotFiles: DeleteIfExists( sFile )
    #
    try:
        #
        t = _doSearchStoreInFile( iSearchID = iSearchID )
        #
        # ### sandbox returns zero items ### 
        # ### use bUseSandbox = False    ### 
        #
        sLastFile, sSearchName = t
        #
        if sLastFile:
            sLastResult = 'Success'
        #
    except SearchNotWorkingError as e:
        # logger.error( 'SearchNotWorkingError: %s' % e )
        sLastResult = 'SearchNotWorkingError: %s' % e
    except SearchGotZeroResults as e:
        # logger.error( 'SearchGotZeroResults: %s' % e )
        sLastResult = 'SearchGotZeroResults: %s' % e
        # suggest sending an email to the owner
    except ConnectionResetError as e:
        # logger.error( 'SearchGotZeroResults: %s' % e )
        sLastResult = 'SearchGotZeroResults: %s' % e
        # maybe an error reading the results
    #
    tNow = timezone.now()
    #
    oSearch.tEndSearch  = tNow
    oSearch.cLastResult = sLastResult
    oSearch.save()
    #
    oSearchLog = SearchLog(
            iSearch_id  = iSearchID,
            tBegSearch  = tSearchStart,
            tEndSearch  = tNow,
            cResult     = sLastResult )
    #
    oSearchLog.save()
    #
    return sLastFile


def storeSearchResultsInDB( iLogID,
                            sMarket,
                            sUserName,
                            iSearchID,
                            sSearchName ):
    #
    '''high level script, accesses results in /tmp file(s)
    and stores indatabase'''
    #
    from django.contrib.auth    import get_user_model
    #
    tSearchTime = tBegStore = timezone.now()
    #
    sFilePattern = (
            RESULTS_FILE_NAME_PATTERN %
                ( sMarket, sUserName, getSearchIdStr( iSearchID ), '*') )
    #
    lGotFiles = getFilesMatchingPattern( '/tmp', sFilePattern )
    #
    lGotFiles.sort()
    #
    iLastPage = getPageNumbOffFileName( lGotFiles[-1] )
    #
    User = get_user_model()
    #
    oUser = User.objects.get( username = sUserName )
    #
    dEbayCatHierarchies = {}
    #
    iItems = iStoreItems = iStoreUsers = 0
    #
    for sThisFileName in lGotFiles:
        #
        oItemIter = getSearchResultGenerator( sThisFileName, iLastPage )
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
                #
                if iItemNumb is None and not settings.TESTING:
                    #
                    logger.warning( '%s -- %s' % 
                                ( '_storeItemFound() returned None',
                                  dItem['itemId'] ) )
                    #
                #
            except ItemAlreadyInTable:
                #
                iItemNumb      = int( dItem['itemId'] )
                #
            except ValueError as e:
                #
                sMsg = 'ValueError: %s | %s' % ( str(e), repr(dItem) )
                logger.error( sMsg)
                #
                print( sMsg )
                #
            #
            if iItemNumb is not None:
                #
                try:
                    #
                    _storeUserItemFound(
                            dItem, iItemNumb, tSearchTime, oUser, iSearchID )
                    #
                    iStoreUsers += 1
                    #
                except ItemAlreadyInTable:
                    pass
                #
            #
    #
    oSearchLog = SearchLog.objects.get( pk = iLogID )
    #
    oSearchLog.tBegStore   = tBegStore
    oSearchLog.tEndStore   = timezone.now()
    oSearchLog.iItems      = iItems
    oSearchLog.iStoreItems = iStoreItems
    oSearchLog.iStoreUsers = iStoreUsers
    #
    oSearchLog.save()
    #
    logger.info(
        'finished stroing records for "%s" search (ID %s) ...' %
        ( sSearchName, iSearchID ) )
    #
    return iItems, iStoreItems, iStoreUsers
