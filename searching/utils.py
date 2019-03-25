import logging

from builtins           import ConnectionResetError
from string             import ascii_letters, digits
from urllib3.exceptions import ConnectTimeoutError, ReadTimeoutError

from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError

from django.conf        import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db          import DataError, IntegrityError
from django.db.models   import Max
from django.utils       import timezone

from core.utils_ebay    import getValueOffItemDict

from ebayinfo.utils     import dMarket2SiteID, getEbayCategoryHierarchies

from keepers.utils      import ITEM_PICS_ROOT, getItemPicsSubDir

from .models            import ItemFound, UserItemFound, SearchLog, Search
from .utilsearch        import ( getSearchResultGenerator, getPagination,
                                 storeItemInfo, SearchGotZeroResults,
                                 ItemAlreadyInTable, getSearchResult,
                                 getSuccessOrNot )

from searching          import ( RESULTS_FILE_NAME_PATTERN,
                                 SEARCH_FILES_FOLDER )

from Dir.Get            import getMakeDir
from File.Del           import DeleteIfExists
from File.Get           import getFilesMatchingPattern
from File.Write         import QuietDump
from Numb.Get           import getHowManyDigitsNeeded
from Utils.Both2n3      import getStrGotBytes


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
    if iID is not None:
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



def _doSearchStoreInFile( iSearchID = None, bUseSandbox = False ):
    #
    '''sends search request to the ebay API, stores the response'''
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
    sErrorFile = sFileName.replace( 'Search_', 'Search_ERROR_' )
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
                sResponse   = findItems(
                                sKeyWords   = sKeyWords,
                                sCategoryID = sEbayCategory,
                                sMarketID   = sMarket,
                                iPage       = iThisPage, # will ignore if < 1
                                bUseSandbox = bUseSandbox )
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
        if sFileName is not None:
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
            'completed without error "%s" search (ID %s)' % tSearch )
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







def _storeItemFound( dItem, dEbayCatHierarchies = {} ):
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
        iSavedRowID = storeItemInfo(
                        dItem,
                        dItemFoundFields,
                        ItemFoundForm,
                        getValueOffItemDict,
                        iCatHeirarchy   = tCatHeirarchies[0],
                        i2ndCatHeirarchy= tCatHeirarchies[1],
                        iEbaySiteID     = iSiteID )
        #
    #
    return iSavedRowID




def _storeUserItemFound( dItem, iItemNumb, oUser, iSearch ):
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
    sListingType = dItem.get( 'listingInfo' ).get( 'listingType' )
    #
    bAuction = sListingType.startswith( 'Auction' )
    #
    return storeItemInfo(
                dItem,
                dUserItemFoundUploadFields,
                UserItemFoundUploadForm,
                _getValueUserOrOther,
                oUser       = oUser,
                iItemNumb   = iItemNumb,
                iSearch     = iSearch,
                bAuction    = bAuction )



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
    oSearch.tBegSearch = tSearchStart # working
    oSearch.cLastResult= None
    oSearch.tEndSearch = None
    #
    oSearch.save()                    # working
    #
    oSearchLog = SearchLog(
            iSearch_id  = iSearchID,
            tBegSearch  = tSearchStart )
    #
    oSearchLog.save()
    #
    sLastResult = 'unknown'
    #
    sUserName   = oSearch.iUser.username
    sMarket     = oSearch.iUser.iEbaySiteID.cMarket
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



def storeSearchResultsInDB( iLogID,
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
    from django.contrib.auth    import get_user_model
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
                'storeSearchResultsInDB() did not find file "%s"!'
                % sFilePattern )
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
            if setTestCategories is not None:
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
                if ( u2ndCategoryID is not None and
                            ( iEbaySiteID, int( u2ndCategoryID ) )
                            not in setTestCategories ):
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



