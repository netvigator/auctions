
from os             import environ
from os.path        import join
from sys            import path


import django

from ebay.utils     import set_config_file, get_config_store
from ebay.finding   import ( findItemsAdvanced, findItemsByKeywords,
                             findItemsByCategory )
from ebay.shopping  import GetSingleItem
from ebay.trading   import getCategories

from File.Write     import QuickDump

from six.moves.urllib.error import HTTPError

from six import print_ as print3

path.append('~/Devel/auctions')

environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

django.setup()

set_config_file( 'config/settings/ebay_config.ini' )

# accessing the config object only for testing in tests.py
oEbayConfig = get_config_store()


def getDecoded( sContent ):
    #
    try:
        sContent = sContent.decode('utf-8')
    except AttributeError:
        pass
    #
    return sContent


def getDecompressed( oContent ):
    #
    from gzip import decompress
    #
    try:
        bContent = decompress( oContent )
    except:
        bContent = oContent
    #
    return bContent


# print3( 'dev_name:', oEbayConfig['keys']['dev_name'] )

'''
signatures:

findItemsAdvanced
keywords=None, \
categoryId=None, \

findItemsByKeywords
keywords, \

findItemsByCategory
categoryId, \

all 3:
affiliate=None, \
buyerPostalCode=None, \
sortOrder=None, \
paginationInput = None, \
aspectFilter=None, \
domainFilter=None, \
itemFilter=None, \
outputSelector=None, \

to vary the market searched, add param:
"X-EBAY-SOA-GLOBAL-ID" : {globalId_you_want}

from trading:
def getCategories(  parentId=None, \
                    detailLevel='ReturnAll', \
                    errorLanguage=None, \
                    messageId=None, \
                    outputSelector=None, \
                    version=None, \
                    warningLevel="High", \
                    levelLimit=1, \
                    viewAllNodes=True, \
                    categorySiteId=0, \
                    encoding="JSON",
                    **headers ):

maybe add to trading: getDefaultCategoryTreeId
https://developer.ebay.com/api-docs/commerce/taxonomy/resources/category_tree/methods/getDefaultCategoryTreeId

'''

def getMarketHeader( sMarketID ):
    #
    dHeader = { "X-EBAY-SOA-GLOBAL-ID": sMarketID }
    #
    return dHeader


#### find requires the hyphenated text global site IDs from here: ###
# http://developer.ebay.com/DevZone/half-finding/Concepts/SiteIDToGlobalID.html
# integer and underscore versions case HTTP Error 500: Internal Server Error

def getItemsByKeyWords( sKeyWords, sMarketID = 'EBAY-US' ):
    #
    dHeader = getMarketHeader( sMarketID )
    #
    return getDecoded(
            findItemsByKeywords( keywords = sKeyWords, **dHeader ) )

def getItemsByCategory( iCategoryID, sMarketID = 'EBAY-US' ):
    #
    dHeader = getMarketHeader( sMarketID )
    #
    return getDecoded(
            findItemsByCategory( categoryId = iCategoryID, **dHeader ) )

def getItemsByBoth( sKeyWords, iCategoryID, sMarketID = 'EBAY-US' ):
    #
    dHeader = getMarketHeader( sMarketID )
    #
    return getDecoded(
            findItemsAdvanced(
                keywords = sKeyWords, categoryId = iCategoryID, **dHeader ) )

#sResults = getItemsByBoth( 'Simpson 360', '58277' )
##
#QuickDump( sResults, 'Results_Adv_Simpson360.json' )


def getCategoryVersion( categorySiteId=0 ):
    #
    oVersion = getCategories(
                categorySiteId = categorySiteId, detailLevel = None )
    #
    return getDecoded( oVersion )

#These are invalid!
#QuickDump( getCategoryVersion( 'EBAY-US' ), 'Categories_Version_US.xml' )
#QuickDump( getCategoryVersion( 'EBAY-DE' ), 'Categories_Version_DE.xml' )

#These are invalid!
#QuickDump( getCategoryVersion( 'EBAY_US' ), 'Categories_Version_US.xml' )
#QuickDump( getCategoryVersion( 'EBAY_DE' ), 'Categories_Version_DE.xml' )

#### These are OK ####
#QuickDump( getCategoryVersion(  0 ), 'Categories_Version_US.xml' )
#QuickDump( getCategoryVersion( 77 ), 'Categories_Version_DE.xml' )


def getMarketCategories( categorySiteId=0 ):
    #
    dHeaders = { 'Accept-Encoding': 'application/gzip' }
    #
    oCategories = getCategories(
        categorySiteId = categorySiteId, levelLimit = None, **dHeaders )
    #
    return getDecoded( getDecompressed( oCategories ) )

# QuickDump( getMarketCategories(), 'Categories_USA.xml.gz' )


'''

Best Practices
GetSingleItem has been optimized for response size, speed and usability. So, it returns the most commonly used fields by default. Use the IncludeSelector field to get more data—but please note that getting more data can result in longer response times.
...
So, after you initially retrieve an item's details, cache the item data locally, and then use GetItemStatus from then on to more quickly update the details that tend to change. Depending on your use case, you can call GetSingleItem again occasionally to see if the seller has revised any other data in the listing.

http://developer.ebay.com/devzone/shopping/docs/callref/getsingleitem.html#IncludeSelector


def GetSingleItem(item_id, include_selector=None, encoding="JSON"):

iItemNumb       = models.BigIntegerField( 'ebay item number', primary_key = True )
cTitle          = models.CharField( 'auction headline', max_length = 48, db_index = True )
Item.Title
Item.Subtitle
mLastBid        = MoneyField( 'winning bid', max_digits = 10, decimal_places = 2, default_currency='USD', null = True )
Item.CurrentPrice
Item.ConvertedCurrentPrice
clastbid        = models.CharField( 'winning bid (text)', max_length = 18, db_index = False, null = True )
tGotLastBid     = models.DateTimeField( 'retrieved last bid date/time', null = True )
mBuyItNow       = MoneyField( 'buy it now price', max_digits = 10, decimal_places = 2, default_currency='USD', null = True )
cbuyitnow       = models.CharField( 'buy it now price (text)', max_length = 18, db_index = False, null = True )
Item.BuyItNowPrice
Item.BuyItNowAvailable
binvaliditem    = models.BooleanField( 'invalid item?', default = False )
iBidCount       = models.PositiveSmallIntegerField( 'number of bids' )
BidCount
tAuctionEnd     = models.DateTimeField( 'auction ending date/time' )
Item.EndTime
tAuctionBeg     = models.DateTimeField( 'auction beginning date/time' )
Item.StartTime
iQuantity       = models.PositiveSmallIntegerField( 'quantity' )
Item.Quantity
tcannotfind     = models.DateTimeField( 'cannot retrieve outcome date/time' )
tlook4images    = models.DateTimeField( 'tried to retrieve images date/time', null = True )
bgotimages      = models.NullBooleanField( 'got images?' )
bReserveMet     = models.NullBooleanField( 'reserve met?', null = True )
Item.ReserveMet
bBuyItNow       = models.BooleanField( 'buy it now?', default = False )
bRelisted       = models.BooleanField( 'relisted?', default = False )
cLocation       = models.CharField( 'location', max_length = 48 )
Location
cregion         = models.CharField( 'region', max_length = 48 )
cSeller         = models.CharField( 'seller', max_length = 48 )
Item.Seller
Seller
iseller
Item.Seller.UserID
isellerfeedback = models.PositiveIntegerField( 'seller feedback' )
FeedbackScore
PositiveFeedbackPercent
TopRatedSeller
cBuyer          = models.CharField( 'buyer', max_length = 48, null = True )
Item.HighBidder 
iBuyer          = models.PositiveIntegerField( 'buyer ID', null = True )
Item.HighBidder.UserID
iBuyerFeedback  = models.PositiveIntegerField( 'buyer feedback', null = True )
Item.HighBidder.FeedbackRatingStar
Item.HighBidder.FeedbackScore
cshipping       = models.CharField( 'shipping info', max_length = 188 )
cDescription    = models.TextField( 'description' )
Description
iImages         = models.PositiveSmallIntegerField( '# of pictures' )
GalleryURL
PictureURL
Variations.Pictures
Item.Variations.Pictures
Item.Variations.Pictures.VariationSpecificName
Item.Variations.Pictures.VariationSpecificPictureSet
Item.Variations.Pictures.VariationSpecificPictureSet.PictureURL
iRelistItemNumb = models.BigIntegerField( 'relist item number' )
SecondaryCategoryID
Site

Item.HighBidder
Item.HighBidder.UserID

def GetItemStatus(item_id, encoding="JSON"):


'''