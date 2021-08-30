from base64             import b64encode
from copy               import deepcopy
from json               import loads
from json.decoder       import JSONDecodeError
from logging            import getLogger
from os                 import environ
from os.path            import join
from sys                import path

from pprint            import pprint

from urllib.request     import urlopen, Request

from django.utils       import timezone as tz

from lxml               import etree
import requests

from ebayinfo.models    import Market
from ebayinfo.utils     import dMarket2SiteID

from pyPks.Iter.AllVers import tMap
from pyPks.Object.Get   import ValueContainer
from pyPks.Time.Convert import getIsoDateTimeFromObj
from pyPks.Utils.Config import getConfDict
from pyPks.Utils.Config import getBoolOffYesNoTrueFalse as getBool


logger = getLogger(__name__)

class InvalidParameters( Exception ): pass


'''
for troubleshooting:
https://developer.ebay.com/DevZone/build-test/test-tool/
'''

tEBAY_LISTING_TYPES = (
      'Auction',
      'AuctionWithBIN',
      'Classified',
      'FixedPrice',
      'StoreInventory',
      'All' )


class _ApplicationtToken( object ):
    #
    '''
    tokenExpires & refreshExpires: datetime in UTC
    '''
    # credit (and see): ValueContainer in pyPks.Object.Get
    #
    error           = None
    access_token    = None
    refresh_token   = None
    tokenExpires    = None
    refreshExpires  = None

    def __init__( self, **kwargs ):
        #
        self.__dict__.update( kwargs )

    def __str__( self ):
        #
        lTokenStr = [ '{' ]
        #
        if self.error is None:
            #
            lTokenStr.append(
                    '"access_token": "%s", "expires": "%s"' %
                    ( self.access_token,
                      getIsoDateTimeFromObj( self.tokenExpires ) ) )
            #
            if self.refresh_token is not None:
                #
                lTokenStr.append(
                        ', "refresh_token": "%s", "expires": "%s"' %
                        ( self.refresh_token,
                          getIsoDateTimeFromObj( self.refreshExpires ) ) )
                #
            #
        else: # error is not None
            #
            lTokenStr.append( '"error": "' + self.error + '"' )
            #
        #
        lTokenStr.append( '}' )
        #
        return ''.join( lTokenStr )

    def isStillGood( self ):
        #
        return self.tokenExpires > tz.now()


def getApiConfValues( bUseSandbox = False ):
    #
    dConfSecrets   = getConfDict( 'config/settings/Secrets.ini' )  # secret
    dEbayConf      = getConfDict( 'config/settings/ebay.ini' )     # not secret
    #
    # sandbox.ini now obsolete
    # dSandBox     = getConfDict( 'config/settings/sandbox.ini' )  # mixed
    #
    if bUseSandbox:
        dEbaySandbox                = dEbayConf
        dEbaySandbox['endpoints']   = dEbaySandbox['sandboxendpoints']
        dEbaySandbox.update( dConfSecrets ) # add production secrets
        dEbaySandbox['keys']        = dEbaySandbox['sandboxkeys']
        dEbaySandbox['auth']        = dEbaySandbox['sandboxauth']
        dUseThis = dEbaySandbox
    else:
        dProduction = dConfSecrets
        dProduction.update( dEbayConf ) # non secrets mixed in for convenience
        dUseThis    = dProduction
    #
    return dUseThis



def _postResponseEbayApi(
        sOperation,
        sEndPointURL,
        sBody,
        uTimeOuts   = ( 4, 10 ), # ( connect, read )
        bMoreHeaders = True,
        **dHttpHeaders ):
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
    if bMoreHeaders:
        #
        dMoreHeaders = {
            "X-EBAY-SOA-OPERATION-NAME"      : sOperation,
            "X-EBAY-SOA-RESPONSE-DATA-FORMAT": 'json' }
        #
        dHttpHeaders.update( dMoreHeaders )
        #
    #
    oResponse = requests.post(
                    sEndPointURL,
                    data    = sBody,
                    timeout = uTimeOuts,
                    headers = dHttpHeaders ) # params is for query string!!!
    #
    return oResponse.text



def _getResponseEbayApi(
        sEndPointURL,
        dData,
        uTimeOuts   = ( 4, 10 ), # ( connect, read )
        dHeaders = {},
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
                    params  = dData,
                    headers = dHeaders,
                    timeout = uTimeOuts )
    #
    return oResponse.text

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

'''

def _getItemInfo( uItemNumb, sCallName,
                  bUseSandbox = False,
                  tWantMore   = None,
                  oAuthToken  = None ):
    #
    dParams = { 'callname'          : sCallName, # 'GetSingleItem',
                'responseencoding'  : "JSON",
                'ItemId'            : str( uItemNumb ) }
    #
    if tWantMore:
        #
        dParams['IncludeSelector'] = ','.join( tWantMore )
        #
    #
    dConfValues = getApiConfValues( bUseSandbox )
    #
    sEndPointURL= dConfValues[ "endpoints"][ 'shopping'        ]
    iSiteID     = dConfValues[ "call"     ][ "global_id"       ]
    sCompatible = dConfValues[ "shopping" ][ "compatibility"   ]
    sAppID      = dConfValues[ "keys"     ][ "ebay_app_id"     ]
    sTimeOutConn= dConfValues[ "call"     ][ "time_out_connect"]
    sTimeOutRead= dConfValues[ "call"     ][ "time_out_read"   ]
    #
    # both the appid query parameter and X-EBAY-API-APP-ID HTTP header
    # will be deprecated on June 30, 2021
    #
    # instead use X-EBAY-API-IAF-TOKEN
    #
    dMore       = dict( appid   = sAppID,
                        siteid  = str( iSiteID ),
                        version = sCompatible )
    #
    dParams.update( dMore )
    #
    tTimeOuts   = tMap( int, ( sTimeOutConn, sTimeOutRead ) )
    #
    dHeaders = {}
    #
    if oAuthToken is not None and oAuthToken.error is None:
        #
        dHeaders = { 'X-EBAY-API-IAF-TOKEN': oAuthToken.access_token }
        #
        del dParams[ 'appid' ]
        #
    #
    return _getResponseEbayApi( sEndPointURL, dParams, tTimeOuts, dHeaders )


_tIncludeDefaults = ( 'Details', 'TextDescription' )

def getSingleItem(
            uItemNumb,
            bUseSandbox = False,
            tWantMore   = _tIncludeDefaults,
            oAuthToken  = None ):
    #
    return _getItemInfo( uItemNumb, 'GetSingleItem',
                         tWantMore   = tWantMore,
                         bUseSandbox = bUseSandbox,
                         oAuthToken  = oAuthToken )


def getItemStatus( uItemNumb, bUseSandbox = False ):
    #
    return _getItemInfo( uItemNumb, 'GetItemStatus',
                         bUseSandbox = bUseSandbox,
                         oAuthToken  = oAuthToken )


def _getCategoriesOrVersion(
            iSiteId      = 0,
            sDetailLevel = None,
            iLevelLimit  = None,
            bUseSandbox  = False,
            **headers ):
    #
    dConfValues = getApiConfValues( bUseSandbox )
    #
    sEndPointURL= dConfValues[ "endpoints"][ 'trading'         ]
    sCompatible = dConfValues[ "trading"  ][ "compatibility"   ]
    sAppID      = dConfValues[ "keys"     ][ "ebay_app_id"     ] # client_id
    sCertID     = dConfValues[ "keys"     ][ "ebay_certid"     ] # client_secret
    sDevID      = dConfValues[ "keys"     ][ "ebay_dev_id"     ]
    sToken      = dConfValues[ "auth"     ][ "token"           ]
    sTimeOutConn= dConfValues[ "call"     ][ "time_out_connect"]
    sTimeOutRead= dConfValues[ "call"     ][ "time_out_read"   ]
    #
    dHttpHeaders= {
            "X-EBAY-API-CALL-NAME"          : 'GetCategories',
            "X-EBAY-API-SITEID"             : str( iSiteId ),
            "X-EBAY-API-COMPATIBILITY-LEVEL": sCompatible,
            }
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
    oElement = etree.SubElement(root, "ErrorLanguage")
    oElement.text = 'en_US'
    #
    oElement = etree.SubElement(root, "WarningLevel")
    oElement.text = 'High'
    #
    if sDetailLevel:
        #
        oElement = etree.SubElement( root, "DetailLevel" )
        oElement .text = sDetailLevel
        #
    else:
        #
        oElement = etree.SubElement( root, "ViewAllNodes" )
        oElement .text = 'false'
        #
    #
    if iLevelLimit:
        oElement = etree.SubElement(root, "LevelLimit")
        oElement.text = str( iLevelLimit )
    #
    sBody = etree.tostring(
                root,
                pretty_print    = True,
                xml_declaration = True,
                encoding        = "utf-8" ).decode('utf-8')
    #
    tTimeOuts   = tMap( int, ( sTimeOutConn, sTimeOutRead ) )
    #
    return _postResponseEbayApi(
            'trading',
            sEndPointURL,
            sBody,
            tTimeOuts,
            bMoreHeaders = False,
            **dHttpHeaders )




def _getListingTypeTuple( *tValues ):
    #
    tListingTypes = ()
    #
    tValidTypes = tuple(
            ( s for s in tValues if s in tEBAY_LISTING_TYPES ) )
    #
    if (    ( 'All', ) in tValidTypes or
            len( tValidTypes ) >= len( tEBAY_LISTING_TYPES ) - 1 ):
        #
        pass
        #
    elif tValidTypes:
        #
        tListingTypes = tValidTypes
        #
    #
    return tListingTypes




def _getEbayFindingResponse(
            sKeyWords       = None,
            sCategoryID     = None,
            tListingTypes   = ('Auction', 'AuctionWithBIN'),
            iPage           = 1,
            bUseSandbox     = False,
            uTimeOuts       = ( 4, 10 ), # ( connect, read )
            sSayInfo        = '',
            oAuthToken      = None,
            **headers ):
    #
    if sKeyWords and sCategoryID:
        #
        sCall = 'findItemsAdvanced'
        #
    elif sKeyWords:
        #
        sCall = 'findItemsByKeywords'
        #
    elif sCategoryID:
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
    if sCategoryID:
        oElement        = etree.SubElement( root, "categoryId" )
        oElement.text   = sCategoryID
    #
    if iPage > 1:
        #
        oElement        = etree.SubElement( root, "paginationInput" )
        #
        oSubElement     = etree.SubElement( oElement, 'entriesPerPage' )
        oSubElement.text= '100'
        oSubElement     = etree.SubElement( oElement, 'pageNumber' )
        oSubElement.text= str( iPage )
        #
    #
    if False and iPage == 1 and sSayInfo:
        print( sSayInfo, 'page', iPage )
        print( 'tListingTypes (before):', tListingTypes )
    #
    tListingTypes = _getListingTypeTuple( *tListingTypes )
    #
    if False and iPage == 1 and sSayInfo:
        print( 'tListingTypes (after):', tListingTypes )
    #
    if tListingTypes:
        #
        oElement            = etree.SubElement( root, 'itemFilter' )
        #
        oSubElement         = etree.SubElement( oElement, "name" )
        oSubElement.text    = 'ListingType'
        #
        # i = 0
        #
        for s in tListingTypes:
            #
            oSubElement     = etree.SubElement( oElement, "value" )
            oSubElement.text= s
            #
            # i += 1
            #
        #
    #
    sBody = etree.tostring(
                root,
                pretty_print    = False,
                encoding        = "utf-8" ).decode('utf-8')
    #
    ''' connect to ebay for finding, get response '''
    #
    dConfValues = getApiConfValues( bUseSandbox )
    #
    sEndPointURL= dConfValues[ "endpoints"][ "finding"    ]
    sGlobalID   = dConfValues[ "call"     ][ "global_id"  ]
    sAppID      = dConfValues[ "keys"     ][ "ebay_app_id"]
    #
    dHttpHeaders= {
            "X-EBAY-SOA-GLOBAL-ID"        : sGlobalID, # can override this
            "X-EBAY-SOA-SECURITY-APPNAME" : sAppID }
    #
    if oAuthToken is not None:
        #
        dHttpHeaders[
            "X-EBAY-API-IAF-TOKEN" ]      = oAuthToken.sToken
        #
        del dHttpHeaders[ "X-EBAY-SOA-SECURITY-APPNAME" ]
        #
    #
    dHttpHeaders.update( headers )
    #
    return _postResponseEbayApi(
              sCall, sEndPointURL, sBody, uTimeOuts, **dHttpHeaders )




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


def findItems(
            sKeyWords       = None,
            sCategoryID     = None,
            sMarketID       = 'EBAY-US',
            iPage           = 1,
            tListingTypes   = ('Auction', 'AuctionWithBIN'),
            bUseSandbox     = False,
            sSayInfo        = '',
            oAuthToken      = None ):
    #
    dHeader = _getMarketHeader( sMarketID )
    #
    dConfValues = getApiConfValues( bUseSandbox )
    #
    sTimeOutConn= dConfValues[ "call"     ][ "time_out_connect"]
    sTimeOutRead= dConfValues[ "call"     ][ "time_out_read"   ]
    #
    tTimeOuts   = tMap( int, ( sTimeOutConn, sTimeOutRead ) )
    #
    return _getDecoded(
                _getEbayFindingResponse(
                    sKeyWords       = sKeyWords,
                    sCategoryID     = sCategoryID,
                    iPage           = iPage,
                    bUseSandbox     = bUseSandbox,
                    tListingTypes   = tListingTypes,
                    uTimeOuts       = tTimeOuts,
                    sSayInfo        = sSayInfo,
                    oAuthToken      = oAuthToken,
                    **dHeader ) )

#sResults = findItems( sKeyWords = 'Simpson 360', '58277' )
#
#QuietDump( sResults, 'Results_Adv_Simpson360.json' )


def getCategoryVersionGotSiteID(
            iSiteId = 0, bUseSandbox = False ): # ID for EBAY-US
    #
    oVersion = _getCategoriesOrVersion(
                    iSiteId      = iSiteId,
                    bUseSandbox  = bUseSandbox )
    #
    return _getDecoded( oVersion )

#These are invalid! getCategoryVersionGotSiteID argument got a hyphen
#QuietDump( getCategoryVersionGotSiteID( 'EBAY-US' ), 'Categories_Ver_EBAY-US.xml' )
#QuietDump( getCategoryVersionGotSiteID( 'EBAY-DE' ), 'Categories_Ver_EBAY-DE.xml' )

#These are invalid! getCategoryVersionGotSiteID argument got an underscore
#QuietDump( getCategoryVersionGotSiteID( 'EBAY_US' ), 'Categories_Ver_EBAY-US.xml' )
#QuietDump( getCategoryVersionGotSiteID( 'EBAY_DE' ), 'Categories_Ver_EBAY-DE.xml' )

# ### These are OK ### getCategoryVersionGotSiteID argument got an integer
#QuietDump( getCategoryVersionGotSiteID(  0 ), 'Categories_Ver_EBAY-US.xml' )
#QuietDump( getCategoryVersionGotSiteID( 77 ), 'Categories_Ver_EBAY-DE.xml' )





def getCategoryVersionGotGlobalID(
        sGlobalID = 'EBAY-US', bUseSandbox = False ):
    #
    # called by ebayinfo/utils/getWhetherAnyEbayCategoryListsAreUpdated
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
logic and code for testing whether oAuthToken is still good

from django.utils import timezone as tz
oUseUntil = tz.now() + tz.timedelta( seconds = 5 )

In [42]: oUseUntil > tz.now()
Out[42]: True

In [43]: oUseUntil > tz.now()
Out[43]: True

In [44]: oUseUntil > tz.now()
Out[44]: True

In [45]: oUseUntil > tz.now()
Out[45]: False


sEndPointURLAuthWeb = dConfValues[ "endpoints"][ 'auth_web' ]

for application token
sEndPointURLAuthApi = dConfValues[ "endpoints"][ 'auth_api' ]



'''


def _getRequestHeaders( dConfValues ):
    #
    # Authorization – The word "Basic "
    # followed by your Base64-encoded OAuth credentials
    # (<client_id>:<client_secret>).
    #
    sCredential = '%s:%s' % (
            dConfValues[ "keys" ][ "ebay_app_id" ],
            dConfValues[ "keys" ][ "ebay_certid" ] )
    #
    sCredentialEncoded = b64encode(
            sCredential.encode("utf-8") ).decode( 'utf-8' )
    #
    dHeaders = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Authorization': 'Basic %s' % sCredentialEncoded }
    #
    return dHeaders


def _getApplicationRequestBody( dConfValues, lScopes ):
    #
    # maybe not needed
    #        'redirect_uri': dConfValues[ "keys" ][ "ebay_ru_name" ],
    #
    dBody = {
            'grant_type': 'client_credentials',
            'scope': ' '.join( lScopes )
    }
    #
    return dBody


lScopes = [ 'https://api.ebay.com/oauth/api_scope' ]


def getApplicationToken( lScopes = lScopes, bUseSandbox = False ):
    #
    dConfValues     = getApiConfValues( bUseSandbox )
    #
    dHeaders        = _getRequestHeaders( dConfValues )
    #
    dBody           = _getApplicationRequestBody( dConfValues, lScopes )
    #
    sEndPointURL    = dConfValues[ "endpoints"][ 'auth_api' ]
    #
    oResponse       = requests.post(
            sEndPointURL, data = dBody, headers = dHeaders )
    #
    oJsonException  = None
    #
    try:
        #
        dContent    = loads( oResponse.content )
        #
    except JSONDecodeError as oJsonException: # ebay server down?
        #
        dContent    = None
        #
    #
    if dContent is None:
        #
        #if oJsonException is not None:
            #sTokenValue = str( oJsonException )
        #else:
        sContent = oResponse.content.decode( encoding = 'utf-8' )
        #
        if (    sContent.startswith( '<!DOCTYPE html>' ) and
                'server is down' in sContent ):
            #
            sTokenValue = 'server is down'
            #
        else:
            #
            sTokenValue = sContent
            #
        #
        sSayError = ( '%s: %s' %
            ( str( oResponse.status_code ), sTokenValue ) )
        #
        oAppToken   = _ApplicationtToken( error = sSayError)
        #
        logger.error( "Unable to retrieve token -- %s" % sSayError )
        #
    elif oResponse.status_code == requests.codes.ok:
        #
        iGoodFor    = int( dContent['expires_in'] ) - 300
        #
        dtExpires   = tz.now() + tz.timedelta( seconds = iGoodFor )
        #
        oAppToken   = _ApplicationtToken(
            access_token    = dContent['access_token'],
            tokenExpires    = dtExpires )
        #
    else:
        #
        oAppToken   = _ApplicationtToken(
            error   = '%s: %s' %
            ( str( oResponse.status_code ),
              dContent['error_description'] ) )
        #
        logger.error(
                "Unable to retrieve token.  Status code: %s - %s" %
                ( oResponse.status_code,
                  requests.status_codes._codes[ oResponse.status_code ] ) )
        #
        logger.error(
                "Error: %s - %s" %
                ( dContent['error'], dContent['error_description'] ) )
        #
    #
    return oAppToken

