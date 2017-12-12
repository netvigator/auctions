
from os             import environ
from os.path        import join
from sys            import path


import django

from ebay.utils     import set_config_file, get_config_store
from ebay.finding   import ( findItemsAdvanced, findItemsByKeywords,
                             findItemsByCategory )
from ebay.trading   import getCategories

from File.Write     import QuickDump

# from six import print_ as print3

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

#sResults = findItemsAdvanced( keywords='Simpson 360', categoryId='58277' )
#
#QuickDump( getDecoded( sResults ), 'Results_Adv_Simpson360.json' )


def getCategoryVersion( categorySiteId=0 ):
    #
    oVersion = getCategories(
                categorySiteId = categorySiteId, detailLevel = None )
    #
    return getDecoded( oVersion )

# QuickDump( getCategoryVersion(), 'Categories_Version_USA.xml' )


def getMarketCategories( categorySiteId=0 ):
    #
    dHeaders = { 'Accept-Encoding': 'application/gzip' }
    #
    oCategories = getCategories(
        categorySiteId = categorySiteId, levelLimit = None, **dHeaders )
    #
    return getDecoded( getDecompressed( oCategories ) )

# QuickDump( getMarketCategories(), 'Categories_USA.xml' )
