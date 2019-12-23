from core.utils         import getDateTimeObjGotEbayStr, getShrinkItemURL

from ebayinfo           import getEbayShippingChoiceCode

from pyPks.Utils.Config import getBoolOffYesNoTrueFalse



d = dict

# null = True, blank = True fields in model MUST be marked bOptional here!
dItemFoundFields = d(
    iItemNumb       = d( t = ( 'itemId',),
                         f = int ),
    cTitle          = d( t = ( 'title',) ),
    cSubTitle       = d( t = ( 'subtitle', ),
                         bOptional = True ),
    cLocation       = d( t = ( 'location',) ),
    cCountry        = d( t = ( 'country',) ),
    cMarket         = d( t = ( 'globalId',) ),
    iEbaySiteID     = d( t = ( 'iEbaySiteID',), # must use cMarket to look this up
                         bCalculate = True ),
    cGalleryURL     = d( t = ( 'galleryURL',), bOptional = True ),
    cEbayItemURL    = d( t = ( 'viewItemURL',),
                         f = getShrinkItemURL ),
    tTimeBeg        = d( t = ( 'listingInfo','startTime'),
                         f = getDateTimeObjGotEbayStr ),
    tTimeEnd        = d( t = ( 'listingInfo','endTime'),
                         f = getDateTimeObjGotEbayStr ),
    bBestOfferable  = d( t = ( 'listingInfo','bestOfferEnabled'),
                         f = getBoolOffYesNoTrueFalse ),
    bBuyItNowable   = d( t = ( 'listingInfo','buyItNowAvailable'),
                         f = getBoolOffYesNoTrueFalse ),
    lBuyItNowPrice  = d( t = ( 'listingInfo',
                               'buyItNowPrice','__value__'),
                         f = float,
                         bOptional = True ),
    dBuyItNowPrice  = d( t = ( 'listingInfo',
                               'convertedBuyItNowPrice','__value__'),
                         f = float,
                         bOptional = True ),
    cListingType    = d( t = ( 'listingInfo','listingType') ),
    lLocalCurrency  = d( t = ( 'sellingStatus','currentPrice','@currencyId') ),
    lCurrentPrice   = d( t = ( 'sellingStatus','currentPrice','__value__'),
                         f = float ),
    dCurrentPrice   = d( t = ( 'sellingStatus',
                               'convertedCurrentPrice','__value__'),
                         f = float ),
    iShippingType   = d( t = ( 'shippingInfo', 'shippingType'),
                         f = getEbayShippingChoiceCode ),
    iHandlingTime   = d( t = ( 'shippingInfo', 'handlingTime'),
                         f = int,
                         bOptional = True ),
    iCategoryID     = d( t = ( 'primaryCategory','categoryId'),
                         f = int ),
    cCategory       = d( t = ( 'primaryCategory','categoryName') ),

    iCatHeirarchy   = d( t = ( 'iCatHeirarchy',), # not from ebay, calculated
                         bCalculate = True ),
    i2ndCategoryID  = d( t = ( 'secondaryCategory','categoryId'),
                         f = int,
                         bOptional = True ),
    c2ndCategory    = d( t = ( 'secondaryCategory','categoryName'),
                         bOptional = True ),
    i2ndCatHeirarchy= d( t = ( 'i2ndCatHeirarchy',), # not from ebay, calculated
                         bCalculate = True ),
    iConditionID    = d( t = ( 'condition','conditionId'),
                         f = int,
                         bOptional = True ),
    cCondition      = d( t = ( 'condition','conditionDisplayName'),
                         bOptional = True ),
    cSellingState   = d( t = ( 'sellingStatus','sellingState') ) )


dUserItemFoundUploadFields = d(
    iItemNumb       = d( t = ( 'itemId',),
                         f = int ),
    tTimeEnd        = d( t = ( 'listingInfo','endTime'),
                         f = getDateTimeObjGotEbayStr ),
    iSearch         = d( t = () ),
    iUser           = d( t = () ),
    tCreate         = d( t = () ), # why does this not work for tCreate?
    bAuction        = d( t = (), bCalculate = True ) )

