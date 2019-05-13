from core.utils         import getDateTimeObjGotEbayStr, getShrinkItemURL

from pyPks.Utils.Config import getBoolOffYesNoTrueFalse


# https://developer.ebay.com/devzone/finding/callref/types/ShippingInfo.html
tEBAY_SHIPPING_TYPES = (
    ( 0,    'Calculated',
            'Calculated' ),
    ( 1,    'CalculatedDomesticFlatInternational',
            'Calculated Domestic Flat International' ),
    ( 2,    'Flat',
            'Flat' ),
    ( 3,    'FlatDomesticCalculatedInternational',
            'Flat Domestic Calculated International' ),
    ( 4,    'Free',
            'Free' ),
    ( 5,    'FreePickup',
            'Pick Up ONLY!' ),
    ( 6,    'Freight',
            'Freight' ),
    ( 7,    'FreightFlat',
            'Freight Flat' ),
    ( 8,    'NotSpecified',
            'Not Specified' ) )

EBAY_SHIPPING_CHOICES = tuple(
        [ ( t[0], t[2] ) for t in tEBAY_SHIPPING_TYPES ] )

dEBAY_SHIPPING_CHOICE_CODE = dict(
        [ ( t[1], t[0] ) for t in tEBAY_SHIPPING_TYPES ] )


def getChoiceCode( sChoice ): return dEBAY_SHIPPING_CHOICE_CODE.get( sChoice )

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
    cListingType    = d( t = ( 'listingInfo','listingType') ),
    lLocalCurrency  = d( t = ( 'sellingStatus','currentPrice','@currencyId') ),
    lCurrentPrice   = d( t = ( 'sellingStatus','currentPrice','__value__'),
                         f = float ),
    dCurrentPrice   = d( t = ( 'sellingStatus',
                               'convertedCurrentPrice','__value__'),
                         f = float ),
    iShippingType   = d( t = ( 'shippingInfo', 'shippingType'),
                         f = getChoiceCode ),
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
    iSearch         = d( t = () ),
    iUser           = d( t = () ),
    tCreate         = d( t = () ), # why does this not work for tCreate?
    bAuction        = d( t = (), bCalculate = True ) )

