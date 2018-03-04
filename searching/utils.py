from logging            import getLogger

from django.test.client import Client, RequestFactory
from django.utils       import timezone

from core.utils_ebay    import getValueOffItemDict, storeEbayInfo

logger = getLogger(__name__)

class SearchNotWorkingError( Exception ): pass
class SearchGotZeroResults(  Exception ): pass
class ItemAlreadyInTable(    Exception ): pass


def getSearchResultGenerator( sFile ):
    #
    from json           import load
    #
    from Dict.Get       import getAnyValue
    from Dict.Maintain  import getDictValuesFromSingleElementLists
    from File.Get       import getFileSpecHereOrThere
    #
    sFile = getFileSpecHereOrThere( sFile )
    #
    dResults = load( open( sFile ) )
    #
    # findItemsAdvancedResponse
    # findItemsByCategoryResponse
    # findItemsByKeywordsResponse
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
        sMessage = 'ack returned "%s"' % dResponse[ "ack" ][0]
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
    if iPages > 1:
        #
        # actually iEntries is a minimum, the actual number of entries is more
        #
        iEntries = (
            1 + ( iPages - 1 ) * int( dPagination[ "entriesPerPage" ] ) )
        #
    #
    if not iEntries:
        #
        raise SearchGotZeroResults( "search executed OK but returned no items" )
        #
    #
    dPagination[ "totalEntries" ] = dPagination[ "totalEntries" ]
    #
    dResultDict = dResponse[ "searchResult" ][0]
    #
    # print( 'dResultDict.keys():', list( dResultDict.keys() ) )
    #
    iThisItem = 0
    #
    lResults = dResultDict.get('item')
    #
    # print( 'lResults:', lResults )
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


def getSearchResults( iSearchID = None ):
    #
    from os.path                import join
    #
    from django.contrib.auth    import get_user_model
    #
    from core.ebay_wrapper  import (
                    getItemsByKeyWords, getItemsByCategory, getItemsByBoth )
    #
    from searching          import sResultFileNamePattern
    from .models            import Search
    from ebayinfo.models    import Market
    #
    from File.Write         import QuietDump
    from String.Split       import getWhiteCleaned
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
    oMarket = Market.objects.get( id = oUser.iMarket_id )
    #
    sMarket = oMarket.cMarket
    #
    sUserName   = oUser.username
    #
    sKeyWords       = getWhiteCleaned( oSearch.cKeyWords )
    iEbayCategory   = oSearch.iEbayCategory
    #
    sFileName       = (
        sResultFileNamePattern % ( sMarket, sUserName, oSearch.id ) )
    #  'Search_%s_%s_ID_%s.json'
    #
    tSearch = ( oSearch.cTitle, str( oSearch.id ) )
    #
    if sKeyWords and iEbayCategory:
        #
        logger.info(
            'executing "%s" search (ID %s) for keywords in category ...' %
            tSearch )
        #
        QuietDump(
            getItemsByBoth( sKeyWords, iEbayCategory, sMarketID = sMarket ),
            sFileName )
        #
    elif sKeyWords:
        #
        logger.info(
            'executing "%s" search (ID %s) for keywords '
            '(in all categories) ...' % tSearch )
        #
        QuietDump(
            getItemsByKeyWords( sKeyWords, sMarketID = sMarket ),
            sFileName )
        #
    elif iEbayCategory:
        #
        logger.info(
            'executing "%s" search (ID %s) in category '
            '(without key words) ...' % tSearch )
        #
        QuietDump(
            getItemsByCategory( iEbayCategory, sMarketID = sMarket ),
            sFileName )
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



def getRegExpFinder(
        sOrig           = '',
        dSub1st         = dSub1st,
        dSub2nd         = dSub2nd,
        tSubLast        = tSubLast,
        fDoThisFirst    = None,
        cSeparator      = '\r',
        bPermutate      = False ):


#
sGot = eatFromWithin( 'This is for real (but not yet)', oInParensFinder )
#
'''


def _getValueOrUser( k, dItem, dFields, oUser = None, iSearch = None ):
    #
    if k == 'iUser':
        return oUser.id
    elif k == 'iSearch':
        return iSearch
    else:
        return getValueOffItemDict( k, dItem, dFields )

    
def storeItemFound( dItem ):
    #
    from .forms     import ItemFoundForm
    from .models    import ItemFound
    from searching  import dItemFoundFields # in __init__.py
    #
    sItemID  = dItem['itemId']
    #
    bAlreadyInTable = ( ItemFound.objects
                        .filter( iItemNumb = int( sItemID ) ).exists() )
    #
    if bAlreadyInTable:
        #
        raise ItemAlreadyInTable(
                'ItemID %s is already in the ItemFound table' % sItemID )
        #
    #
    return storeEbayInfo( dItem, dItemFoundFields, ItemFoundForm, getValueOffItemDict )


def storeUserItemFound( dItem, oUser, iSearch ):
    #
    from django.db.models import Q
    #
    from .forms     import UserItemFoundForm
    from .models    import UserItemFound
    from searching  import dUserItemFoundFields # in __init__.py
    #
    sItemID  = dItem['itemId']
    #
    bAlreadyInTable = ( UserItemFound.objects
                        .filter( iItemNumb = int( sItemID ),
                                 iUser     = oUser )
                        .exists() )
    #
    if bAlreadyInTable:
        #
        raise ItemAlreadyInTable(
                'ItemID %s is already in the UserItemFound table for %s' %
                ( sItemID, oUser.username ) )
        #
    #
    return storeEbayInfo(
            dItem, dUserItemFoundFields, UserItemFoundForm, _getValueOrUser,
            oUser = oUser, iSearch = iSearch )



def doSearch( iSearchID = None, sFileName = None ):
    #
    '''pass Search ID to search ebay via the api, or pass
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
        sFileName = getSearchResults( iSearchID )
        #
    #
    # 'Search-%s-%s-ID-%s.json' % ( sMarket, sUserName, oSearch.id ) )
    #
    lParts = sFileName.split( '_' )
    #
    sUserName   =                     lParts[ 2]
    iSearch     = int( getTextBefore( lParts[-1], '.json' ) )
    #
    oUser = User.objects.get( username = sUserName )
    #
    oItemIter = getSearchResultGenerator( sFileName )
    #
    iItems = iStoreItems = iStoreUsers = 0
    #
    for dItem in oItemIter:
        #
        iItems += 1
        #
        try:
            storeItemFound( dItem )
            iStoreItems += 1
        except ItemAlreadyInTable:
            pass
        except ValueError as e:
            logger.error( 'ValueError: %s | %s' %
                          ( str(e), repr(dItem) ) )
        #
        try:
            storeUserItemFound( dItem, oUser, iSearch )
            iStoreUsers += 1
        except ItemAlreadyInTable:
            pass
        #
    #
    return iItems, iStoreItems, iStoreUsers



def trySearchCatchExceptions( iSearchID = None, sFileName = None ):
    #
    iItems = iStoreItems = iStoreUsers = 0
    #
    try:
        iItems, iStoreItems, iStoreUsers = doSearch(
                    iSearchID = iSearchID, sFileName = sFileName )
    except SearchNotWorkingError as e:
        logger.error( 'SearchNotWorkingError: %s' % e )
    except SearchGotZeroResults as e:
        logger.error( 'SearchGotZeroResults: %s' % e )
    #
    return iItems, iStoreItems, iStoreUsers 

