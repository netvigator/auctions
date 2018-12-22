from django.test import TestCase

from ..ebay_api_calls import _getApiConfValues, _getListingTypeTuple


class GetConfFileValuesTests(TestCase):
    '''ebay API conf file values tests'''

    def test_ini_values(self):

        dConfValues = _getApiConfValues( False )

        self.assertEqual( dConfValues['call']['global_id'], 'EBAY-US' )
        self.assertEqual( dConfValues['call']['siteid'   ], '0'       )

        self.assertEqual( dConfValues['endpoints']['finding'],
                    'http://svcs.ebay.com/services/search/FindingService/v1' )

        self.assertIsNotNone( dConfValues[ "keys"     ].get( "ebay_app_id" ) )

        sTokenStart = 'AgAAAA**AQAAAA**aAAAAA**m1'

        self.assertEqual(
                dConfValues['auth']['token'][ : len( sTokenStart ) ],
                sTokenStart )

        dConfValues = _getApiConfValues( True )

        self.assertEqual( dConfValues['call']['global_id'], 'EBAY-US' )
        self.assertEqual( dConfValues['call']['siteid'   ], '0'       )

        self.assertEqual( dConfValues['endpoints']['finding'],
                    'http://svcs.sandbox.ebay.com/services/search/FindingService/v1' )

        sTokenStart = 'AgAAAA**AQAAAA**aAAAAA**/0'

        self.assertIsNotNone( dConfValues[ "keys"     ].get( "ebay_app_id" ) )
        self.assertEqual(
                dConfValues['auth']['token'][ : len( sTokenStart ) ],
                sTokenStart )



class TestListingTypeTupleTests(TestCase):
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



