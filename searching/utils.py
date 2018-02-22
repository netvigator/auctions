from django.test.client import Client, RequestFactory

from searching          import dItemFoundFields

class SearchNotWorkingError( Exception ): pass
class SearchGotZeroResults(  Exception ): pass
class ItemFoundAlready(      Exception ): pass


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

def _getTableRowForWriting( oTableModel, iWantOlderThan ):
    #
    from datetime       import timedelta
    #
    from django.utils   import timezone
    #
    dDropDead = timezone.now() - timedelta( days = iWantOlderThan )
    #
    bGotOldRecords = ( oTableModel.objects
                        .filter( tCreate__lte = dDropDead )
                        .exists() )
    #
    if bGotOldRecords:
        #
        oNewItem = ( oTableModel.objects
                        .filter( tCreate__lte = dDropDead )
                        .order_by( 'tCreate' )
                        .first() )
        #
        oNewItem.tCreate = timezone.now()
        #
    else:
        #
        oNewItem = None
        #
    #
    return oNewItem


def getItemFoundForWriting( iWantOlderThan = 100 ):
    #
    from .models import ItemFound
    #
    return _getTableRowForWriting( ItemFound, iWantOlderThan )



def getUserItemFoundForWriting( iWantOlderThan = 100 ):
    #
    from .models import UserItemFound
    #
    return _getTableRowForWriting( UserItemFound, iWantOlderThan )




def storeRow( dItem, dFields, getRow, Form, oUser = None ):
    #
    def getValueOffItemDict( k ):
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
    #
    if oUser is None:
        #
        getValue = getValueOffItemDict
        #
    else:
        #
        def getValue( k ):
            #
            if k == 'iUser':
                return oUser
            else:
                return getValueOffItemDict( k )
            #
        #
    #
    oRow = getRow()
    #
    dNewResult = { k: getValue( k ) for k in dFields }
    #
    if oRow is None: # no old record to recycle, form will save to new row
        #
        form = Form( data = dNewResult )
        #
        print( '\noRow is None: no old record to recycle, form will save to new row' )
        #
    else: # got an old record to recycle, overwrite its values then save
        #
        print( '\noRow is an old record to recycle, form will save to this row' )
        #
        factory = RequestFactory()
        request = factory.get('/%s/edit/' % oRow.iItemNumb )
        #
        form = Form( data=request.POST or None, instance = oRow )
        #
        form.data.update( dNewResult )
        #
    #
    if form.is_valid():
        #
        form.save()
        #
        print( 'form saved!' )
    else:
        print( '\nform.is_valid() returned False' )
        if oRow is None:
            print( 'fetched row was None, meaning no old record to recycle' )
        else:
            print( 'row  iItemNumb:', oRow.__dict__['iItemNumb'] )
        print( 'dict iItemNumb:', dNewResult['iItemNumb'] )
        print( 'form iItemNumb:', form.data['iItemNumb'] )
        #
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', str(v) )
        else:
            print( 'no form errors at bottom!' )
        pass # log error
    
    
def storeItemFound( dItem ):
    #
    from .forms import ItemFoundForm
    #
    return storeRow(
            dItem, dItemFoundFields, getItemFoundForWriting, ItemFoundForm )


def storeItemFoundOrig( dItem ):
    #
    from Object.Get         import QuickObject
    #
    #
    from .forms             import ItemFoundForm, tItemFoundFields
    #
    oNew = QuickObject()
    #
    oNew.iItemNumb      = int(     dItem['itemId'] )
    oNew.cTitle         =          dItem['title']
    oNew.cLocation      =          dItem['location']
    oNew.cCountry       =          dItem['country']
    oNew.cMarket        =          dItem['globalId']
    oNew.cGalleryURL    =          dItem['galleryURL']
    oNew.cEbayItemURL   =          dItem['viewItemURL']
    oNew.tTimeBeg       = getDT(   dItem['listingInfo']['startTime'] )
    oNew.tTimeEnd       = getDT(   dItem['listingInfo']['endTime']   )
    oNew.bBestOfferable = getBo(   dItem['listingInfo']['bestOfferEnabled'] )
    oNew.bBuyItNowable  = getBo(   dItem['listingInfo']['buyItNowAvailable'] )
    oNew.cListingType   =          dItem['listingInfo']['listingType']
    oNew.lCurrentPrice  =   float( dItem['sellingStatus']
                                        ['currentPrice']['__value__']   )
    oNew.lLocalCurrency =        ( dItem['sellingStatus']
                                        ['currentPrice']['@currencyId'] )
    oNew.dCurrentPrice  =   float( dItem['sellingStatus']
                                        ['convertedCurrentPrice']
                                        ['__value__'] )
    oNew.iCategoryID    = int(     dItem['primaryCategory']['categoryId'] )
    oNew.cCategory      =          dItem['primaryCategory']['categoryName']
    oNew.iConditionID   = int(     dItem['condition']['conditionId'] )
    oNew.cCondition     =          dItem['condition']['conditionDisplayName']
    oNew.cSellingState  =          dItem['sellingStatus']['sellingState']
    #
    form = ItemFoundForm( data = oNew.__dict__ )
    #
    if form.is_valid():
        #
        form.save()
        #
        #print( 'form saved!' )
    else:
        #print( '\nform.is_valid() returned False' )
        #print( 'dict lCurrentPrice:', oNew.__dict__['lCurrentPrice'] )
        #print( 'form lCurrentPrice:', form.data['lCurrentPrice'] )
        ##
        #if form.errors:
            #for k, v in form.errors.items():
                #print( k, ' -- ', str(v) )
        #else:
            #print( 'no form errors at bottom!' )
        pass # log error

