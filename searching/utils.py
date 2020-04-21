import logging

from builtins               import ConnectionResetError
from string                 import ascii_letters, digits
from os.path                import join
from urllib3.exceptions     import ConnectTimeoutError, ReadTimeoutError
from time                   import sleep

from requests.exceptions    import ConnectTimeout, ReadTimeout, ConnectionError

from django.conf            import settings

from django.db              import DataError, IntegrityError
from django.db.models       import Max
from django.utils           import timezone

from core.dj_import         import ObjectDoesNotExist, get_user_model

from core.utils_ebay        import getValueOffItemDict
from core.ebay_api_calls    import findItems

from ebayinfo               import dMarketsRelated
from ebayinfo.models        import Market, CategoryHierarchy
from ebayinfo.utils         import ( dMarket2SiteID,
                                     getEbayCategoryHierarchies,
                                     setShippingTypeLocalPickupOptional )

from finders                import dItemFoundFields, dUserItemFoundUploadFields
from finders.forms          import ItemFoundForm, UserItemFoundUploadForm
from finders.models         import ItemFound, UserItemFound

from keepers.utils          import ITEM_PICS_ROOT, getItemPicsSubDir

from .models                import SearchLog, Search
from .utilsearch            import ( ItemAlreadyInTable, getSearchResult,
                                     getSuccessOrNot, storeItemInfo,
                                     getPagination, SearchGotZeroResults,
                                     getSearchResultGenerator )

from searching              import ( RESULTS_FILE_NAME_PATTERN,
                                     SEARCH_FILES_FOLDER )

from pyPks.Collect.Output   import getTextSequence
from pyPks.Dir.Get          import getMakeDir
from pyPks.File.Del         import DeleteIfExists
from pyPks.File.Get         import getFilesMatchingPattern
from pyPks.File.Write       import QuietDump
from pyPks.Numb.Get         import getHowManyDigitsNeeded
from pyPks.String.Split     import getWhiteCleaned
from pyPks.Utils.Both2n3    import getStrGotBytes

logger = logging.getLogger(__name__)

logging_level = logging.WARNING

'''
logging.basicConfig(level=logging.loglevel)
this will print logging messages to the terminal
'''
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)

class SearchNotWorkingError( Exception ): pass

getMakeDir( SEARCH_FILES_FOLDER )

def getHowManySearchDigitsNeeded( iID = None ):
    #
    iNeedDigits = iID = None
    #
    if iID is None:
        try:
            iID = Search.objects.all().aggregate(Max('id'))['id__max']
        except ObjectDoesNotExist: # testing and no search objects yet
            pass
    #
    if iID:
        #
        iNeedDigits = getHowManyDigitsNeeded( iID )
        #
    #
    return iNeedDigits


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



def _doSearchStoreInFile(
                    iSearchID       = None,
                    bGetBuyItNows   = False,
                    bInventory      = False,
                    bUseSandbox     = False ):
    #
    '''sends search request to the ebay API, stores the response'''
    #
    User = get_user_model()
    #
    if iSearchID is None:
        #
        oSearch = Search.objects.filter( iUser_id = 1 ).first()
        #
    else:
        #
        # Two Sccops recommends AGAINST passing objects to async processes
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
    lListingTypes       = [ 'Auction', 'AuctionWithBIN' ]
    sSayGetMore         = ''
    lSayGetMore         = []
    #
    if bGetBuyItNows:
        #
        lListingTypes.append( 'FixedPrice' )
        lSayGetMore     = [ 'BuyItNows' ]
        #
    if bInventory:
        #
        lListingTypes.append( 'StoreInventory' )
        lSayGetMore.append( 'Store Inventory' )
        #
    #
    tListingTypes       = tuple( lListingTypes )
    #
    if lSayGetMore:
        #
        sSayGetMore     = ( '(also getting %s) ' %
                            getTextSequence( lSayGetMore, sAnd = '&' ) )
        #
    #
    if oSearch.iEbayCategory:
        sEbayCategory   = str( oSearch.iEbayCategory.iCategoryID )
    #
    tSearch = ( oSearch.cTitle, str( oSearch.id ), sSayGetMore )
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
    sErrorFile = sFileName.replace( 'Search_', 'Search_ERROR_' )
    #
    if settings.TESTING:
        #
        logging.disable(logging.CRITICAL)
        #
    #
    sSayInfo = 'not defined!'
    #
    if sKeyWords and sEbayCategory:
        #
        sSayInfo = (
            'doing "%s" search (ID %s) for keywords in category %s...' %
            tSearch )
        #
    elif sKeyWords:
        #
        sSayInfo = (
            'doing "%s" search (ID %s) for keywords '
            '(in all categories) %s...' % tSearch )
        #
    elif sEbayCategory:
        #
        sSayInfo = (
            'doing "%s" search (ID %s) in category '
            '(without key words) %s...' % tSearch )
        #
    #
    logger.info( sSayInfo )
    #
    iThisPage  = 0
    iWantPages = 1
    #
    bHitErrorCancel = False
    #
    sResponse = None # need to initialize if internet not working
    #
    while iThisPage <= iWantPages:
        #
        iRetries    = 0
        #
        while iRetries < 5:
            #
            dPagination = {}
            #
            try:
                #
                sResponse = findItems(
                                sKeyWords       = sKeyWords,
                                sCategoryID     = sEbayCategory,
                                tListingTypes   = tListingTypes,
                                sMarketID       = sMarket,
                                iPage           = iThisPage, # will ignore if < 1
                                bUseSandbox     = bUseSandbox )
                #
            except ConnectionResetError as e:
                sResponse = 'ConnectionResetError: %s'  % e
            except ConnectTimeoutError as e:
                sResponse = 'ConnectTimeoutError: %s'   % e
            except ReadTimeoutError as e:
                sResponse = 'ReadTimeoutError: %s'      % e
            except ConnectTimeout as e:
                sResponse = 'ConnectTimeout: %s'        % e
            except ReadTimeout as e:
                sResponse = 'ReadTimeout: %s'           % e
            except ConnectionError as e:
                sLastResult = 'ConnectionError: %s'     % e
            #
            else:
                #
                dPagination = getPagination( sResponse )
                '''
                dPagination = dict(
                    iCount          = int( sCount       ),
                    iTotalEntries   = int( sTotalEntries),
                    iPages          = int( sPages       ),
                    iEntriesPP      = int( sEntriesPP   ),
                    iPageNumb       = int( sPageNumb    ) )
                if ebay returns an error message instead of a finding response,
                getPagination( sResponse ) returns a dictionary,
                iCount = 0, & all other values are None
                actual example error message in core.tests.__init__.py
                '''
                #

                if dPagination.get( "iPages" ) or getSuccessOrNot( sResponse ):
                    #
                    break
                    #
                #
            #
            iRetries += 1
            #
            if (    iRetries == 5 or
                    ( sResponse and
                      getSearchResult(
                          getStrGotBytes(
                              sResponse ) ) in ( 'Error', 'error' ) ) ):
                #
                sErrorFile = _putPageNumbInFileName( sErrorFile, iRetries )
                #
                QuietDump( sResponse, '/tmp', sErrorFile )
                #
                if iRetries == 5:
                    #
                    sMsg = 'ebay api repeated failure error in tmp file "%s"'
                    #
                else:
                    #
                    sMsg = 'ebay api hit explicit error, in tmp file "%s"'
                    #
                #
                logger.error( sMsg % sErrorFile )
                #
                bHitErrorCancel = True
                #
                break
                #
            #
            sleep( 1 + iRetries )
            #
        #
        if dPagination.get( "iPages" ):
            #
            if dPagination["iPages"] > 1 and iThisPage == 0:
                #
                iThisPage = dPagination["iPageNumb"]
                #
            #
            iWantPages = min( dPagination["iPages"], 100 ) # ebay will do 100 max
            #
        #
        if iThisPage > 0 and iWantPages > 1:
            sFileName = _putPageNumbInFileName( sFileName, iThisPage )
        #
        if sFileName:
            #
            QuietDump( sResponse, SEARCH_FILES_FOLDER, sFileName )
            #
        #
        iThisPage += 1
        #
        if iThisPage <= iWantPages: sleep(1)
        #
    #
    if bHitErrorCancel:
        #
        sFileName = sErrorFile
        #
    else:
        #
        logger.info(
            'completed "%s" search (ID %s) %swithout error' % tSearch )
        #
    #
    if settings.TESTING:
        #
        logging.disable(logging.NOTSET)
        #
    #
    sFileName = join( SEARCH_FILES_FOLDER, sFileName )
    #
    return sFileName, oSearch.cTitle



def _getValueUserOrOther( dItem, k, dThisField, oUser = None, **kwargs ):
    #
    if k == 'iUser':
        return oUser.id
    elif k in kwargs:
        return kwargs[ k ]
    else:
        return getValueOffItemDict( dItem, k, dThisField )




def _storeItemFound( dItem, dEbayCatHierarchies ):
    #
    # dEbayCatHierarchies is now a required parameter !!!
    # but can pass {} for testing
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
        setShippingType = setShippingTypeLocalPickupOptional # too long!
        #
        iSavedRowID = storeItemInfo(
                        dItem,
                        dItemFoundFields,
                        ItemFoundForm,
                        getValueOffItemDict,
                        iCatHeirarchy       = tCatHeirarchies[0],
                        i2ndCatHeirarchy    = tCatHeirarchies[1],
                        iEbaySiteID         = iSiteID,
                        fBeforeForm         = setShippingType,
                        dEbayCatHierarchies = dEbayCatHierarchies )
        #
    #
    return iSavedRowID




def _storeUserItemFound( dItem, iItemNumb, oUser, iSearch ):
    #
    # calling for UserItemFound
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
    sListingType = dItem.get( 'listingInfo' ).get( 'listingType' )
    #
    bAuction = sListingType.startswith( 'Auction' )
    #
    iSavedRowID = storeItemInfo(
                dItem,
                dUserItemFoundUploadFields,
                UserItemFoundUploadForm,
                _getValueUserOrOther,
                oUser       = oUser,
                iItemNumb   = iItemNumb,
                iSearch     = iSearch,
                bAuction    = bAuction )
    #
    # ### store userfinder in utils_stars.findSearchHits() ###
    #
    return iSavedRowID



def trySearchCatchExceptStoreInFile( iSearchID ):
    #
    '''high level script, does a search, catches exceptions, logs errors,
    stores results in file'''
    #
    # ### sandbox returns zero items ###
    # ### use bUseSandbox = False    ###
    #
    tSearchStart = timezone.now()
    #
    oSearch = Search.objects.get( pk = iSearchID )
    #
    oSearch.tBegSearch  = tSearchStart # working
    oSearch.cLastResult = None
    oSearch.tEndSearch  = None
    #
    oSearch.save()                    # working
    #
    oSearchLog = SearchLog(
            iSearch_id  = iSearchID,
            tBegSearch  = tSearchStart )
    #
    oSearchLog.save()
    #
    sLastResult         = 'unknown'
    #
    sUserName           = oSearch.iUser.username
    sMarket             = oSearch.iUser.iEbaySiteID.cMarket
    #
    sFilePattern= (
            RESULTS_FILE_NAME_PATTERN %
                ( sMarket, sUserName, getSearchIdStr( iSearchID ), '*') )
    #
    lGotFiles   = getFilesMatchingPattern( SEARCH_FILES_FOLDER, sFilePattern )
    #
    for sFile in lGotFiles: DeleteIfExists( sFile )
    #
    try:
        #
        t = _doSearchStoreInFile(
                iSearchID       = iSearchID,
                bGetBuyItNows   = oSearch.bGetBuyItNows,
                bInventory      = oSearch.bInventory )
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
    except ReadTimeoutError as e:
        sLastResult = 'ReadTimeoutError: %s'    % e
    #
    tNow = timezone.now()
    #
    oSearch.tEndSearch  = tNow
    oSearch.cLastResult = sLastResult
    oSearch.save()
    #
    oSearchLog.tEndSearch  = tNow
    oSearchLog.cResult     = sLastResult
    #
    oSearchLog.save()
    #
    return sLastFile



def storeSearchResultsInFinders(
            iLogID,
            sMarket,
            sUserName,
            iSearchID,
            sSearchName,
            setTestCategories    = None,
            bCleanUpFiles        = False,
            bDoNotMentionAny     = False ):
    #
    '''high level script, accesses results in file(s)
    and stores in database'''
    #
    tBegStore = timezone.now()
    #
    sFilePattern = (
            RESULTS_FILE_NAME_PATTERN %
                ( sMarket, sUserName, getSearchIdStr( iSearchID ), '*') )
    #
    lGotFiles = getFilesMatchingPattern( SEARCH_FILES_FOLDER, sFilePattern )
    #
    if not lGotFiles:
        #
        logger.warning(
                'storeSearchResultsInFinders() did not find file "%s"!'
                % join( SEARCH_FILES_FOLDER, sFilePattern ) )
        #
        return 0, 0, 0
        #
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
            iItemNumb = int( dItem.get( 'itemId' ) )
            #
            if setTestCategories:
                #
                # when testing, will skip items with categories
                # not in the abbreviated category table
                #
                iEbaySiteID     = dMarket2SiteID[ dItem.get( 'globalId' ) ]
                iCategoryID     = int( dItem.get( 'primaryCategory'       )
                                            .get( 'categoryId' ) )
                u2ndCategoryID  =    ( dItem.get( 'secondaryCategory', {} )
                                            .get( 'categoryId' ) )
                #
                if ( iEbaySiteID, iCategoryID ) not in setTestCategories:
                    #
                    if bDoNotMentionAny:
                        #
                        bSayDiscarded = False
                        #
                    else:
                        #
                        bSayDiscarded = True
                        #
                    #
                    if bSayDiscarded:
                        #
                        print('')
                        print('discarded %s, category %s' %
                                ( iItemNumb,
                                  str( ( iEbaySiteID, iCategoryID ) ) ) )
                        #
                    #
                    continue
                    #
                #
                i2ndCategoryID = ( int( u2ndCategoryID )
                                   if u2ndCategoryID is not None
                                   else None )
                #
                tRelatedSites = dMarketsRelated.get( iEbaySiteID, () )
                #
                iOtherSite0 = ( tRelatedSites[0]
                                if tRelatedSites
                                else iEbaySiteID )
                #
                iOtherSite1 = ( tRelatedSites[-1]
                                if tRelatedSites
                                else iEbaySiteID )
                #
                bTest2ndaryCategory = False
                #
                for iSiteID in frozenset( ( iOtherSite0, iOtherSite1 ) ):
                    #
                    if ( iSiteID, i2ndCategoryID ) in setTestCategories:
                        #
                        bTest2ndaryCategory = True
                        #
                        i2ndCategorySiteID = iSiteID
                #
                if 'secondaryCategory' in dItem and not bTest2ndaryCategory:
                    #
                    if iItemNumb == 233420619849:
                        #
                        #
                        print( "will del dItem[ 'secondaryCategory' ]" )
                    #
                    del dItem[ 'secondaryCategory' ] # 2nd category optional
                    #
                #
            #
            bGotItem = ItemFound.objects.filter( pk = iItemNumb ).exists()
            #
            if not bGotItem:
                #
                try:
                    #
                    iItemNumb = _storeItemFound( dItem, dEbayCatHierarchies )
                    #
                    iStoreItems += 1
                    #
                    if iItemNumb is None and not settings.TESTING:
                        #
                        logger.warning( '%s -- %s' %
                                    ( '_storeItemFound() returned None',
                                    dItem['itemId'] ) )
                        #
                    #
                except ( IntegrityError, ItemAlreadyInTable ):
                    #
                    iItemNumb      = int( dItem.get( 'itemId' ) )
                    #
                except ValueError as e:
                    #
                    sMsg = 'ValueError: %s | %s' % ( str(e), repr(dItem) )
                    logger.error( sMsg)
                    #
                    #
                #
            #
            if iItemNumb is None: iItemNumb = int( dItem.get( 'itemId' ) )
            #
            bGotUserItem = ( UserItemFound.objects.filter(
                                iItemNumb   = iItemNumb,
                                iUser       = oUser ).exists() )
            #
            if not bGotUserItem:
                #
                try:
                    #
                    _storeUserItemFound( dItem, iItemNumb, oUser, iSearchID )
                    #
                    iStoreUsers += 1
                    #
                except ( IntegrityError, ItemAlreadyInTable ):
                    #
                    pass
                    #
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
    #logger.info(
        #'finished stroing records for "%s" search (ID %s) ...' %
        #( sSearchName, iSearchID ) )
    #
    if bCleanUpFiles:
        #
        for sThisFileName in lGotFiles:
            #
            DeleteIfExists( sThisFileName ) # may include Example file!
            #
        #
    #
    return iItems, iStoreItems, iStoreUsers



