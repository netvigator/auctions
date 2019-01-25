from core.utils     import getDateTimeObjGotEbayStr, getShrinkItemURL

from Dir.Get        import getMakeDir
from Utils.Config   import getBoolOffYesNoTrueFalse

WORD_BOUNDARY_MAX   = 5

RESULTS_FILE_NAME_PATTERN = 'Search_%s_%s_ID_%s_p_%s_.json'
# variables: sMarket, sUserName, iSearchID, iPageNumb
# sName.split('_') gives this:
# ['Search',sMarket,sUserName,'ID',iSearchID,'p',iPageNumb,'.json' ]
#   0       1       2          3   4          5  6          7
#
# when selling on the ebay site, condition is optional
# https://developer.ebay.com/DevZone/guides/ebayfeatures/Development/Desc-ItemCondition.html

SEARCH_FILES_FOLDER  = '/tmp/searches'
SEARCH_TESTS_FOLDER  = '/tmp/searches_test'


getMakeDir( SEARCH_FILES_FOLDER )

d = dict

# null = True, blank = True fields in model MUST be marked bOptional here!
dItemFoundFields = d(
    iItemNumb       = d( t = ( 'itemId',),
                         f = int ),
    cTitle          = d( t = ( 'title',) ),
    cSubTitle       = d( t = ( 'subtitle'),
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
