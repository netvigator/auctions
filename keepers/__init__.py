from core.utils         import getDateTimeObjGotEbayStr, getShrinkItemURL

from pyPks.Dir.Get      import getMakeDir
from pyPks.Utils.Config import getBoolOffYesNoTrueFalse

EBAY_ITEMS_FOLDER = '/tmp/ebay_items'


getMakeDir( EBAY_ITEMS_FOLDER )


def _intEnforceMax( s ):
    #
    return min( int( s ), 32767 )

def _getList( s ):
    #
    if isinstance( s, list ):
        #
        l = s
        #
    elif isinstance( s, str ):
        #
        if s.startswith( '[' ) and s.endswith( ']' ):
            #
            s = s[ 1 : -1 ]
            #
        #
        l = [ s.strip()[ 1 : -1 ] for s in s.split( ',' ) ]
        #
    #
    return l


def getListAsLines( s ):
    #
    l = _getList( s )
    #
    return '\n'.join( l )


def getListWithCommas( s ):
    #
    l = _getList( s )
    #
    return ', '.join( l )


def getListWithCommasMax88( s ):
    #
    return getListWithCommas( s )[ : 88 ]


d = dict

# null = True, blank = True fields in model MUST be marked bOptional here!
dItemFields = d(
    iItemNumb       = d( t = ( "ItemID",),
                         f = int ),
    cDescription    = d( t = ( "Description",),
                         bOptional = True ),
    bBestOfferable  = d( t = ( "BestOfferEnabled",),
                         f = getBoolOffYesNoTrueFalse ),
    tTimeEnd        = d( t = ( "EndTime",),
                         f = getDateTimeObjGotEbayStr ),
    tTimeBeg        = d( t = ( "StartTime",),
                         f = getDateTimeObjGotEbayStr ),
    cEbayItemURL    = d( t = ( "ViewItemURLForNaturalSearch",),
                         f = getShrinkItemURL ),
    cListingType    = d( t = ( "ListingType",), ),
    cLocation       = d( t = ( "Location",), ),
    cPaymentMethods = d( t = ( "PaymentMethods",),
                         f = getListWithCommasMax88 ),
    cGalleryURL     = d( t = ( "GalleryURL",),
                         bOptional = True ),
    cPictureURLs    = d( t = ( "PictureURL",),
                         f = getListAsLines ),
    cPostalCode     = d( t = ( "PostalCode",),
                         bOptional = True ),
    iQuantity       = d( t = ( "Quantity",),
                         f = int ),
    cSellerID       = d( t = ( "Seller", "UserID",), ),
    iFeedbackScore  = d( t = ( "Seller", "FeedbackScore",),
                         f = int,
                         bOptional = True ),
    cFeedbackPercent= d( t = ( "Seller", "PositiveFeedbackPercent",), ),
    iBidCount       = d( t = ( "BidCount",),
                         f = int ),
    dConvertPrice   = d( t = ( "ConvertedCurrentPrice", "Value",),
                         f = float ),
    cConvertCurrency= d( t = ( "ConvertedCurrentPrice", "CurrencyID",), ),
    lLocalPrice     = d( t = ( "CurrentPrice", "Value",),
                         f = float ),
    lLocalCurrency  = d( t = ( "CurrentPrice", "CurrencyID",), ),
    cHighBidder     = d( t = ( "HighBidder", "UserID",),
                         bOptional = True ),
    cListingStatus  = d( t = ( "ListingStatus",), ),
    iQuantitySold   = d( t = ( "QuantitySold",),
                         f = int ),
    cShipToLocations= d( t = ( "ShipToLocations",),
                         f = getListWithCommas ),
    cSite           = d( t = ( "Site",), ),
    cTitle          = d( t = ( "Title",), ),
    iHitCount       = d( t = ( "HitCount",),
                         f = _intEnforceMax,
                         bOptional = True ),
    iCategoryID     = d( t = ( "PrimaryCategoryID",),
                         f = int ),
    cCategoryIDs    = d( t = ( "PrimaryCategoryIDPath",), ),
    cCategoryNames  = d( t = ( "PrimaryCategoryName",), ),
    cCountry        = d( t = ( "Country",), ),
    cReturnPolicy   = d( t = ( "ReturnPolicy", "ReturnsAccepted",), ),
    dMinimumBid     = d( t = ( "MinimumToBid", "Value",),
                         bOptional = True ),
    cBidCurrency    = d( t = ( "MinimumToBid", "CurrencyID",),
                         bOptional = True ),
    iConditionID    = d( t = ( "ConditionID",),
                         f = int,
                         bOptional = True ),
    cCondition      = d( t = ( "ConditionDisplayName",),
                         bOptional = True ),
    bGlobalShipping = d( t = ( "GlobalShipping",),
                         f = getBoolOffYesNoTrueFalse ),

    bBuyItNowable   = d( t = ( "BuyItNowAvailable", ),
                         f = getBoolOffYesNoTrueFalse,
                         bOptional = True ),
    lBuyItNowPrice  = d( t = ( "BuyItNowPrice", "Value",),
                         f = float,
                         bOptional = True ),
    lBuyItNowCurrenc= d( t = ( "BuyItNowPrice", "CurrencyID",),
                         bOptional = True ),
    dBuyItNowPrice  = d( t = ( "ConvertedBuyItNowPrice", "Value",),
                         f = float,
                         bOptional = True ),
    cBuyItNowConvert= d( t = ( "ConvertedBuyItNowPrice", "CurrencyID",),
                         bOptional = True ),
)
