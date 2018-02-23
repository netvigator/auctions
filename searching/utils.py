from django.test.client import Client, RequestFactory
from django.utils       import timezone


class SearchNotWorkingError( Exception ): pass
class SearchGotZeroResults(  Exception ): pass
class ItemAlreadyInTable(    Exception ): pass


def getSearchResultGenerator( sFile ):
    #
    from json           import load
    #
    from Dict.Get       import getAnyValue
    from Dict.Maintain  import getDictValuesFromSingleElementLists
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
        'Search-%s-%s-ID_%s.json' % ( sMarket, sUserName, oSearch.id ) )
    #
    if sKeyWords and iEbayCategory:
        #
        QuietDump(
            getItemsByBoth( sKeyWords, iEbayCategory, sMarketID = sMarket ),
            sFileName )
        #
    elif sKeyWords:
        #
        QuietDump(
            getItemsByKeyWords( sKeyWords, sMarketID = sMarket ),
            sFileName )
        #
    elif iEbayCategory:
        #
        QuietDump(
            getItemsByCategory( iEbayCategory, sMarketID = sMarket ),
            sFileName )
        #
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


def _getValueOffItemDict( k, dItem, dFields, oUser = None ):
    #
    t = dFields[ k ]
    #
    uValue  = dItem[ t[1] ]
    #
    tRest   = t[ 2 : ]
    #
    for sKey in tRest:
        uValue = uValue[ sKey ]
    #
    sValue  = uValue
    #
    if t[0] is None:
        uReturn = sValue
    else:
        f = t[0]
        uReturn = f( sValue )
    #
    return uReturn


def _getValueOrUser( k, dItem, dFields, oUser ):
    #
    if k == 'iUser':
        return oUser.id
    else:
        return _getValueOffItemDict( k, dItem, dFields )


def storeRow( dItem, dFields, Form, getValue, oUser = None ):
    #
    '''can store a row in either ItemFound or UserItemFound'''
    #
    dNewResult = { k: getValue( k, dItem, dFields, oUser ) for k in dFields }
    #
    form = Form( data = dNewResult )
    #
    if form.is_valid():
        #
        form.save()
        #
    else:
        #
        from pprint import pprint
        #
        print( 'log this error, form did not save' )
        #
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', str(v) )
        else:
            print( 'no form errors at bottom!' )
    
    
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
    return storeRow( dItem, dItemFoundFields, ItemFoundForm, _getValueOffItemDict )


def storeUserItemFound( dItem, oUser ):
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
    return storeRow( dItem, dUserItemFoundFields, UserItemFoundForm, _getValueOrUser, oUser )



def doSearch( iSearchID = None, sFileName = None ):
    #
    '''pass Search ID to search ebay via the api, or pass
    a file name to process the results of a prior search'''
    #
    from django.contrib.auth import get_user_model
    #
    User = get_user_model()
    #
    if sFileName is None:
        #
        sFileName = getSearchResults( iSearchID )
        #
    #
    # 'Search-%s-%s-ID_%s.json' % ( sMarket, sUserName, oSearch.id ) )
    #
    lParts = sFileName.split( '-' )
    #
    sUserName = lParts[1]
    #
    oUser = User.objects.get( username = sUserName )
    #
    oItemIter = getSearchResultGenerator( sFileName )
    #
    for dItem in oItemIter:
        #
        try:
            storeItemFound( dItem )
        except ItemAlreadyInTable:
            pass
        #
        try:
            storeUserItemFound( dItem, oUser )
        except ItemAlreadyInTable:
            pass
        #



def trySearchCatchExceptions( iSearchID = None, sFileName = None ):
    #
    try:
        doSearch( iSearchID, sFileName )
    except SearchNotWorkingError as e:
        pass
    except SearchGotZeroResults as e:
        pass


