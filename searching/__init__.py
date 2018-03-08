from core.utils     import getDateTimeObjGotEbayStr
from Utils.Config   import getBoolOffYesNoTrueFalse

sResultFileNamePattern = 'Search_%s_%s_ID_%s.json'

# condition is optional
# https://developer.ebay.com/DevZone/guides/ebayfeatures/Development/Desc-ItemCondition.html

d = dict

dItemFoundFields = d(
    iItemNumb       = d( t = ( 'itemId',),
                         f = int ),
    cTitle          = d( t = ( 'title',) ),
    cLocation       = d( t = ( 'location',) ),
    cCountry        = d( t = ( 'country',) ),
    cMarket         = d( t = ( 'globalId',) ),
    cGalleryURL     = d( t = ( 'galleryURL',) ),
    cEbayItemURL    = d( t = ( 'viewItemURL',) ),
    tTimeBeg        = d( t = ( 'listingInfo','startTime'),
                         f = getDateTimeObjGotEbayStr ),
    tTimeEnd        = d( t = ( 'listingInfo','endTime'),
                         f = getDateTimeObjGotEbayStr ),
    bBestOfferable  = d( t = ( 'listingInfo','bestOfferEnabled'),
                         f = getBoolOffYesNoTrueFalse ),
    bBuyItNowable   = d( t = ( 'listingInfo','buyItNowAvailable'),
                         f = getBoolOffYesNoTrueFalse ),
    cListingType    = d( t = ( 'listingInfo','listingType') ),
    lLocalCurrency  = d( t = ( 'sellingStatus','currentPrice','@currencyId') ),
    lCurrentPrice   = d( t = ( 'sellingStatus','currentPrice','__value__'),
                         f = float ),
    dCurrentPrice   = d( t = ( 'sellingStatus',
                               'convertedCurrentPrice','__value__'),
                         f = float ),
    iCategoryID     = d( t = ( 'primaryCategory','categoryId'),
                         f = int ),
    cCategory       = d( t = ( 'primaryCategory','categoryName') ),

    i2ndCategoryID  = d( t = ( 'secondaryCategory','categoryId'),
                         f = int,
                         bOptional = True ),
    c2ndCategory    = d( t = ( 'secondaryCategory','categoryName'),
                         bOptional = True ),

    iConditionID    = d( t = ( 'condition','conditionId'),
                         f = int,
                         bOptional = True ),
    cCondition      = d( t = ( 'condition','conditionDisplayName'),
                         bOptional = True ),
    cSellingState   = d( t = ( 'sellingStatus','sellingState') ) )


dUserItemFoundFields = d(
    iItemNumb       = d( t = ( 'itemId',),
                         f = int ),
    iSearch         = {},
    iUser           = {} )
