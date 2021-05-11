
from .base                  import TestCasePlus

from ..ebay_api_calls       import getApiConfValues, _getListingTypeTuple



class GetConfFileValuesTests( TestCasePlus ):
    '''ebay API conf file values tests'''

    def setUp( self ):
        #
        self.dConfValues = getApiConfValues()


    def test_ini_values(self):

        dConfValues = self.dConfValues

        self.assertEqual( dConfValues['call']['global_id'], 'EBAY-US' )
        self.assertEqual( dConfValues['call']['siteid'   ], '0'       )

        self.assertEqual( dConfValues['endpoints']['finding'],
                    'https://svcs.ebay.com/services/search/FindingService/v1' )

        self.assertIsNotNone( dConfValues[ "keys"     ].get( "ebay_app_id" ) )

        sTokenStart = 'AgAAAA**AQAAAA**aAAAAA**'

        self.assertEqual(
                dConfValues['auth']['token'][ : len( sTokenStart ) ],
                sTokenStart )

        dConfValues = getApiConfValues( bUseSandbox = True )

        self.assertEqual( dConfValues['call']['global_id'], 'EBAY-US' )
        self.assertEqual( dConfValues['call']['siteid'   ], '0'       )

        self.assertEqual( dConfValues['endpoints']['finding'],
                    'http://svcs.sandbox.ebay.com/services/search/FindingService/v1' )

        sTokenStart = 'AgAAAA**AQAAAA**aAAAAA**'

        self.assertIsNotNone( dConfValues[ "keys"     ].get( "ebay_app_id" ) )
        self.assertEqual(
                dConfValues['auth']['token'][ : len( sTokenStart ) ],
                sTokenStart )



class TestListingTypeTupleTests( TestCasePlus ):
    '''test ebay API ListingType HTTP headers'''

    def test_getListingTypeTupleDefault(self):
        #
        tGotTypes = _getListingTypeTuple( 'Auction', 'AuctionWithBIN' )
        #
        tWantTypes = ( 'Auction', 'AuctionWithBIN' )
        #
        self.assertEqual( tGotTypes , tWantTypes )


    def test_getListingTypeTupleAll(self):
        #
        tGotTypes = _getListingTypeTuple( ('All',) )
        #
        tWantTypes = ()
        #
        self.assertEqual( tGotTypes , tWantTypes )


    def test_getListingTypeTupleCustom(self):
        #
        tGotTypes = _getListingTypeTuple(
                'Auction', 'AuctionWithBIN', 'FixedPrice' )
        #
        tWantTypes = ( 'Auction', 'AuctionWithBIN', 'FixedPrice' )
        #
        self.assertEqual( tGotTypes , tWantTypes )


'''
use these for time out tests only because downloaded file is HUGE:
    getMarketCategoriesGotSiteID()
    getMarketCategoriesGotGlobalID()

do test:
    getItemsByKeyWords()
    getItemsByCategory()
    getItemsByBoth()
    getSingleItem()
    getItemStatus()
'''



