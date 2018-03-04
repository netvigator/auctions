from core.utils     import getDateTimeObjGotEbayStr as getDT
from Utils.Config   import getBoolOffYesNoTrueFalse as getBo

sResultFileNamePattern = 'Search_%s_%s_ID_%s.json'

# condition is optional
# https://developer.ebay.com/DevZone/guides/ebayfeatures/Development/Desc-ItemCondition.html

d = dict

dItemFoundFields = d(
    iItemNumb       = d( f = int,  t = ( 'itemId',) ),
    cTitle          = d( f = None, t = ( 'title',) ),
    cLocation       = d( f = None, t = ( 'location',) ),
    cCountry        = d( f = None, t = ( 'country',) ),
    cMarket         = d( f = None, t = ( 'globalId',) ),
    cGalleryURL     = d( f = None, t = ( 'galleryURL',) ),
    cEbayItemURL    = d( f = None, t = ( 'viewItemURL',) ),
    tTimeBeg        = d( f = getDT,t = ( 'listingInfo','startTime') ),
    tTimeEnd        = d( f = getDT,t = ( 'listingInfo','endTime') ),
    bBestOfferable  = d( f = getBo,t = ( 'listingInfo','bestOfferEnabled') ),
    bBuyItNowable   = d( f = getBo,t = ( 'listingInfo','buyItNowAvailable') ),
    cListingType    = d( f = None, t = ( 'listingInfo','listingType') ),
    lLocalCurrency  = d( f = None,
                         t = ( 'sellingStatus','currentPrice','@currencyId') ),
    lCurrentPrice   = d( f = float,
                         t = ( 'sellingStatus','currentPrice','__value__') ),
    dCurrentPrice   = d( f = float,
                         t = ( 'sellingStatus',
                               'convertedCurrentPrice','__value__') ),
    iCategoryID     = d( f = int,  t = ( 'primaryCategory','categoryId') ),
    cCategory       = d( f = None, t = ( 'primaryCategory','categoryName') ),
    iConditionID    = d( f = int,  t = ( 'condition','conditionId'),
                         bOptional = True ),
    cCondition      = d( f = None, t = ( 'condition','conditionDisplayName'),
                         bOptional = True ),
    cSellingState   = d( f = None, t = ( 'sellingStatus','sellingState') ) )


dUserItemFoundFields = d(
    iItemNumb       = d( f = int,  t = ( 'itemId',) ),
    iSearch         = d( f = None, t = ( '',) ),
    iUser           = d( f = None, t = ( '',) ) )
