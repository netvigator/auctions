from json           import load

from core.utils     import oInParensFinder

from Dict.Get       import getAnyValue
from Dict.Maintain  import getDictValuesFromSingleElementLists
from String.Eat     import eatFromWithin
from String.Find    import getRegEx4Chars

class SearchNotWorkingError( Exception ): pass
class SearchGotZeroResults(  Exception ): pass



def getSearchResultGenerator( sFile ):
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
    from markets.models     import Market
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

next( oIter )

{'autoPay': 'false',
 'condition': {'conditionDisplayName': 'New', 'conditionId': '1000'},
 'country': 'US',
 'galleryURL': 'http://thumbs3.ebaystatic.com/m/mutHoe85kv1_SUEGG3k1yBw/140.jpg',
 'globalId': 'EBAY-US',
 'isMultiVariationListing': 'false',
 'itemId': '282330751118',
 'listingInfo': {'bestOfferEnabled': 'true',
  'buyItNowAvailable': 'false',
  'endTime': '2018-02-13T00:34:26.000Z',
  'gift': 'false',
  'listingType': 'FixedPrice',
  'startTime': '2017-01-19T00:34:26.000Z',
  'watchCount': '19'},
 'location': 'Staten Island,NY,USA',
 'paginationOutput': {'entriesPerPage': '100',
  'pageNumber': '1',
  'thisEntry': '1',
  'totalEntries': '1320',
  'totalPages': '14'},
 'paymentMethod': 'PayPal',
 'postalCode': '10303',
 'primaryCategory': {'categoryId': '73160',
  'categoryName': 'Capacitance & ESR Meters'},
 'returnsAccepted': 'true',
 'sellingStatus': {'convertedCurrentPrice': {'@currencyId': 'USD',
   '__value__': '27.99'},
  'currentPrice': {'@currencyId': 'USD', '__value__': '27.99'},
  'sellingState': 'Active',
  'timeLeft': 'P13DT6H33M56S'},
 'shippingInfo': {'expeditedShipping': 'false',
  'handlingTime': '1',
  'oneDayShippingAvailable': 'false',
  'shipToLocations': 'Worldwide',
  'shippingServiceCost': {'@currencyId': 'USD', '__value__': '0.0'},
  'shippingType': 'Free'},
 'title': 'Digital Capacitance Tester Capacitor Meter Auto Range Multimeter Checker 470mF',
 'topRatedListing': 'true',
 'viewItemURL': 'http://www.ebay.com/itm/Digital-Capacitance-Tester-Capacitor-Meter-Auto-Range-MultimeterChecker-470mF-/282330751118'
 }
 
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