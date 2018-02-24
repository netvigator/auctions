from core.utils     import getDateTimeObjGotEbayStr as getDT
from Utils.Config   import getBoolOffYesNoTrueFalse as getBo

dItemFoundFields = dict(
    iItemNumb       = (int,  'itemId',),
    cTitle          = (None, 'title',),
    cLocation       = (None, 'location',),
    cCountry        = (None, 'country',),
    cMarket         = (None, 'globalId',),
    cGalleryURL     = (None, 'galleryURL',),
    cEbayItemURL    = (None, 'viewItemURL',),
    tTimeBeg        = (getDT,'listingInfo','startTime'),
    tTimeEnd        = (getDT,'listingInfo','endTime'),
    bBestOfferable  = (getBo,'listingInfo','bestOfferEnabled'),
    bBuyItNowable   = (getBo,'listingInfo','buyItNowAvailable'),
    cListingType    = (None, 'listingInfo','listingType'),
    lLocalCurrency  = (None, 'sellingStatus','currentPrice','@currencyId'),
    lCurrentPrice   = (float,'sellingStatus','currentPrice','__value__'),
    dCurrentPrice   = (float,'sellingStatus','convertedCurrentPrice','__value__'),
    iCategoryID     = (int,  'primaryCategory','categoryId'),
    cCategory       = (None, 'primaryCategory','categoryName'),
    iConditionID    = (int,  'condition','conditionId'),
    cCondition      = (None, 'condition','conditionDisplayName'),
    cSellingState   = (None, 'sellingStatus','sellingState') )


dUserItemFoundFields = dict(
    iItemNumb       = (int,  'itemId',),
    iSearch         = (None, '',),
    iUser           = (None, '',) )
