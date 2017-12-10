
from os             import environ
from os.path        import join
from sys            import path

import django

from ebay.utils     import set_config_file, get_config_store
from ebay.finding   import findItemsAdvanced, findItemsByKeywords, \
                            findItemsByCategory

from File.Write     import QuickDump

# from six import print_ as print3

path.append('~/Devel/auctions')

environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

django.setup()

set_config_file( 'config/settings/ebay_config.ini' )

# accessing the config object only for testing in tests.py
oEbayConfig = get_config_store()

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
'''

sResults = findItemsAdvanced( keywords='Simpson 360', categoryId='58277' )

QuickDump( sResults, 'Results.json' )
