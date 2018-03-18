from copy               import deepcopy
from os                 import environ
from os.path            import join
from sys                import path

from urllib.request     import urlopen, Request

import django

from lxml               import etree
import requests


from File.Write         import QuietDump
from Utils.Config       import getConfDict
from Utils.Config       import getBoolOffYesNoTrueFalse as getBool

from ebayinfo.models    import Market
from ebayinfo.utils     import dMarket2SiteID


path.append('~/Devel/auctions')

environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

class InvalidParameters( Exception ): pass

django.setup()


_dProdSecrets   = getConfDict( 'config/settings/Secrets.ini' )  # secret

_dEbayConf      = getConfDict( 'config/settings/ebay.ini' )     # not secret

_dSandBox       = getConfDict( 'config/settings/sandbox.ini' )  # mixed

_dEbaySandbox   = deepcopy( _dEbayConf )

_dEbaySandbox.update( _dProdSecrets ) # add production secrets

_dEbaySandbox.update( _dSandBox ) # overwrite secrets, add some non secrets

_dProduction    = _dProdSecrets

_dProduction.update( _dEbayConf ) # non secrets mixed in for convenience



def _getApiConfValues( bUseSandbox ):
    #
    if bUseSandbox:
        dUseThis = _dEbaySandbox
    else:
        dUseThis = _dProduction
    #
    return dUseThis


def _getEbayApiPostResponse(
        sOperation,
        sEndPointURL,
        sRequest,
        uTimeOuts   = ( 4, 10 ), # ( connect, read )
        **headers ):
    #
    ''' connect to ebay, do a POST, get response '''
    #
    # It's a good practice to set connect timeouts to slightly larger than a
    # multiple of 3, which is the default TCP packet retransmission window.
    #
    # Can set single value, single timeout value will be applied to
    # both the connect and the read timeouts.
    # Specify a tuple if you would like to set the values separately
    # http://docs.python-requests.org/en/master/user/advanced/#timeouts
    #
    # can set to 0.001 for testing timed out response
    #
    dHttpHeaders= {
            "X-EBAY-SOA-OPERATION-NAME"      : sOperation,
            "X-EBAY-SOA-RESPONSE-DATA-FORMAT": 'json' }
    #
    dHttpHeaders.update( headers )
    #
    oResponse = requests.post(
                    sEndPointURL,
                    data    = sRequest,
                    timeout = uTimeOuts,
                    headers = dHttpHeaders )
    #
    return oResponse.text


def _getEbayApiGetResponse(
        sEndPointURL,
        dData,
        uTimeOuts   = ( 4, 10 ), # ( connect, read )
        **kwargs ):
    #
    ''' connect to ebay, do a GET, get response '''
    #
    # see comments above re timeouts
    #
    dData.update( kwargs )
    #
    oResponse = requests.get(
                    sEndPointURL,
                    params = dData,
                    timeout = uTimeOuts )
    #
    return oResponse.text


def _getItemInfo( iItemNumb, sCallName,
                  bUseSandbox = False,
                  dWantMore   = None ):
    #
    dParams = { 'callname'          : sCallName, # 'GetSingleItem',
                'responseencoding'  : "JSON",
                'ItemId'            : str( iItemNumb ) }
    #
    if dWantMore:
        #
        dParams['IncludeSelector'] = dWantMore
        #
    #
    dConfValues = _getApiConfValues( bUseSandbox )
    #
    sEndPointURL= dConfValues[ "endpoints"][ 'shopping'     ]
    iSiteID     = dConfValues[ "call"     ][ "global_id"    ]
    sCompatible = dConfValues[ "call"     ][ "compatibility"]
    sAppID      = dConfValues[ "keys"     ][ "ebay_app_id"  ]
    #
    dMore       = dict( appid   = sAppID,
                        siteid  = str( iSiteID ),
                        version = sCompatible )
    #
    dParams.update( dMore )
    #
    return _getEbayApiGetResponse( sEndPointURL, dParams )


def getSingleItem( iItemNumb, bUseSandbox = False, dWantMore = None ):
    #
    return _getItemInfo( iItemNumb, 'GetSingleItem',
                         dWantMore   = dWantMore,
                         bUseSandbox = bUseSandbox )


def getItemStatus( iItemNumb, bUseSandbox = False ):
    #
    return _getItemInfo( iItemNumb, 'GetItemStatus', 
                         bUseSandbox = bUseSandbox )



def _getCategoriesOrVersion(
            iSiteId      = 0,
            sDetailLevel = None,
            iLevelLimit  = None,
            bUseSandbox  = False,
            **headers ):
    #
    dConfValues = _getApiConfValues( bUseSandbox )
    #
    sEndPointURL= dConfValues[ "endpoints"][ 'trading'      ]
    sCompatible = dConfValues[ "call"     ][ "compatibility"]
    sAppID      = dConfValues[ "keys"     ][ "ebay_app_id"  ]
    sCertID     = dConfValues[ "keys"     ][ "ebay_certid"  ]
    sDevID      = dConfValues[ "keys"     ][ "ebay_dev_id"  ]
    sToken      = dConfValues[ "auth"     ][ "token"        ]
    #
    dHttpHeaders= {
            "X-EBAY-API-COMPATIBILITY-LEVEL": sCompatible,
            "X-EBAY-API-DEV-NAME"           : sDevID,
            "X-EBAY-API-APP-NAME"           : sAppID,
            "X-EBAY-API-CERT-NAME"          : sCertID,
            "X-EBAY-API-CALL-NAME"          : 'GetCategories',
            "X-EBAY-API-SITEID"             : str( iSiteId ),
            "Content-Type"                  : "text/xml" }
    #
    dHttpHeaders.update( headers )
    #
    root = etree.Element( "GetCategoriesRequest",
                          xmlns = "urn:ebay:apis:eBLBaseComponents" )
    #
    oCredentials = etree.SubElement( root, "RequesterCredentials" )
    #
    oElement = etree.SubElement( oCredentials, "eBayAuthToken")
    oElement.text = sToken
    #
    oElement = etree.SubElement(root, "CategorySiteID")
    oElement.text = str( iSiteId )
    #
    if sDetailLevel:
        oElement = etree.SubElement( root, "DetailLevel" )
        oElement .text = sDetailLevel
    #
    if iLevelLimit:
        oElement = etree.SubElement(root, "LevelLimit")
        oElement.text = str( iLevelLimit )
    #
    sRequest    = etree.tostring(
                    root,
                    pretty_print    = False,
                    xml_declaration = True,
                    encoding        = "utf-8" )
    #
    return _getEbayApiPostResponse(
            'trading',
            sEndPointURL,
            sRequest,
            **dHttpHeaders )


def _getEbayFindingResponse(
        sOperation,
        sRequest,
        bUseSandbox = False,
        uTimeOuts   = ( 4, 10 ), # ( connect, read )
        **headers ):
    #
    ''' connect to ebay for finding, get response '''
    #
    dConfValues = _getApiConfValues( bUseSandbox )
    #
    sEndPointURL= dConfValues[ "endpoints"][ 'finding'    ]
    sGlobalID   = dConfValues[ "call"     ][ "global_id"  ]
    sAppID      = dConfValues[ "keys"     ][ "ebay_app_id"]

    dHttpHeaders= {
            "X-EBAY-SOA-GLOBAL-ID"        : sGlobalID, # can override this
            "X-EBAY-SOA-SECURITY-APPNAME" : sAppID }

    dHttpHeaders.update( headers )
    #
    return _getEbayApiPostResponse( sOperation, sEndPointURL, sRequest, uTimeOuts, **headers )




def _findItems( sKeyWords   = None,
                iCategoryID = None,
                bUseSandbox = False,
                **headers ):
    #
    if sKeyWords and iCategoryID:
        #
        sCall = 'findItemsAdvanced'
        #
    elif sKeyWords:
        #
        sCall = 'findItemsByKeywords'
        #
    elif iCategoryID:
        #
        sCall = 'findItemsByCategory'
        #
    else:
        #
        raise InvalidParameters( 'must pass either key words or category' )
        #
    #
    root = etree.Element(
            sCall,
            xmlns = "http://www.ebay.com/marketplace/search/v1/services" )
    #
    if sKeyWords:
        oElement        = etree.SubElement( root, "keywords" )
        oElement.text   = sKeyWords
    #
    if iCategoryID:
        oElement        = etree.SubElement( root, "categoryId" )
        oElement.text   = iCategoryID
    #
    sRequest = etree.tostring( root, pretty_print = True )
    #
    return _getEbayFindingResponse(
                sCall, sRequest, bUseSandbox = bUseSandbox, **headers )


def _getDecoded( sContent ):
    #
    try:
        sContent = sContent.decode('utf-8')
    except AttributeError:
        pass
    #
    return sContent


def _getDecompressed( oContent ):
    #
    from gzip import decompress
    #
    try:
        bContent = decompress( oContent )
    except:
        bContent = oContent
    #
    return bContent


def _getMarketHeader( sMarketID ):
    #
    dHeader = { "X-EBAY-SOA-GLOBAL-ID": sMarketID }
    #
    return dHeader


#### find requires the hyphenated text global site IDs from here: ###
# http://developer.ebay.com/DevZone/half-finding/Concepts/SiteIDToGlobalID.html
# integer and underscore versions case HTTP Error 500: Internal Server Error

def getItemsByKeyWords( sKeyWords, sMarketID = 'EBAY-US', bUseSandbox = False ):
    #
    dHeader = _getMarketHeader( sMarketID )
    #
    return _getDecoded(
                _findItems(
                    sKeyWords = sKeyWords,
                    bUseSandbox = bUseSandbox,
                    **dHeader ) )

def getItemsByCategory( iCategoryID, sMarketID = 'EBAY-US', bUseSandbox = False ):
    #
    dHeader = _getMarketHeader( sMarketID )
    #
    return _getDecoded(
                _findItems(
                    iCategoryID = iCategoryID,
                    bUseSandbox = bUseSandbox,
                    **dHeader ) )

def getItemsByBoth( sKeyWords, iCategoryID, sMarketID = 'EBAY-US', bUseSandbox = False ):
    #
    dHeader = _getMarketHeader( sMarketID )
    #
    return _getDecoded(
                _findItems(
                    sKeyWords   = sKeyWords,
                    iCategoryID = iCategoryID,
                    bUseSandbox = bUseSandbox,
                    **dHeader ) )

#sResults = getItemsByBoth( 'Simpson 360', '58277' )
##
#QuietDump( sResults, 'Results_Adv_Simpson360.json' )


def getCategoryVersionGotSiteID(
            iSiteId = 0, bUseSandbox = False ): # ID for EBAY-US
    #
    oVersion = _getCategoriesOrVersion(
                    iSiteId     = iSiteId,
                    iLevelLimit = 1,
                    bUseSandbox = bUseSandbox )
    #
    return _getDecoded( oVersion )

#These are invalid!
#QuietDump( getCategoryVersionGotSiteID( 'EBAY-US' ), 'Categories_Ver_EBAY-US.xml' )
#QuietDump( getCategoryVersionGotSiteID( 'EBAY-DE' ), 'Categories_Ver_EBAY-DE.xml' )

#These are invalid!
#QuietDump( getCategoryVersionGotSiteID( 'EBAY_US' ), 'Categories_Ver_EBAY-US.xml' )
#QuietDump( getCategoryVersionGotSiteID( 'EBAY_DE' ), 'Categories_Ver_EBAY-DE.xml' )

#### These are OK ####
#QuietDump( getCategoryVersionGotSiteID(  0 ), 'Categories_Ver_EBAY-US.xml' )
#QuietDump( getCategoryVersionGotSiteID( 77 ), 'Categories_Ver_EBAY-DE.xml' )



def getCategoryVersionGotGlobalID(
        sGlobalID = 'EBAY-US', bUseSandbox = False ):
    #
    iID = dMarket2SiteID[ sGlobalID ]
    #
    return getCategoryVersionGotSiteID(
                iSiteId = iID, bUseSandbox = bUseSandbox )

# QuietDump( getCategoryVersionGotGlobalID( 'EBAY-GB' ), 'Categories_Ver_EBAY-GB.xml' )



def getMarketCategoriesGotSiteID( iSiteId = 0, bUseSandbox = False ): # ID for EBAY-US
    #
    dHeaders = { 'Accept-Encoding': 'application/gzip' }
    #
    oCategories = _getCategoriesOrVersion(
                        iSiteId      = iSiteId,
                        sDetailLevel = 'ReturnAll',
                        bUseSandbox  = bUseSandbox,
                        **dHeaders )
    #
    return _getDecoded( _getDecompressed( oCategories ) )

# QuietDump( getMarketCategoriesGotSiteID(), 'Categories_All_EBAY-USA.xml' )


def getMarketCategoriesGotGlobalID(
        sGlobalID = 'EBAY-US', bUseSandbox = False ):
    #
    iID = dMarket2SiteID[ sGlobalID ]
    #
    return getMarketCategoriesGotSiteID(
            iSiteId = iID, bUseSandbox = bUseSandbox )

# QuietDump( getMarketCategoriesGotGlobalID(),            'Categories_All_EBAY-US.xml' )
# QuietDump( getMarketCategoriesGotGlobalID( 'EBAY-GB' ), 'Categories_All_EBAY-GB.xml' )



'''

Best Practices
GetSingleItem has been optimized for response size, speed and usability.
So, it returns the most commonly used fields by default. 
Use the IncludeSelector field to get more data—
but please note that getting more data can result in longer response times.
...
So, after you initially retrieve an item's details, 
cache the item data locally, and then use GetItemStatus 
from then on to more quickly update the details that tend to change. 
Depending on your use case, you can call GetSingleItem again occasionally 
to see if the seller has revised any other data in the listing.

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
iSellerFeedback = models.PositiveIntegerField( 'seller feedback' )
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