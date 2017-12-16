
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
def GetSingleItem(item_id, include_selector=None, encoding="JSON"):



'''