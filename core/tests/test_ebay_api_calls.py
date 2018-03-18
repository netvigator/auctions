from django.test import TestCase

from ..ebay_api_calls import _getApiConfValues


class GetConfFileValuesTests(TestCase):
    '''ebay API conf file values tests'''
    
    def test_ini_values(self):
        
        dConfValues = _getApiConfValues( False )
        
        self.assertEquals( dConfValues['call']['global_id'], 'EBAY-US' )
        self.assertEquals( dConfValues['call']['siteid'   ], '0'       )
        
        self.assertEquals( dConfValues['endpoints']['finding'],
                    'http://svcs.ebay.com/services/search/FindingService/v1' )
        
        self.assertIsNotNone( dConfValues[ "keys"     ].get( "ebay_app_id" ) )

        dConfValues = _getApiConfValues( True )
        
        self.assertEquals( dConfValues['call']['global_id'], 'EBAY-US' )
        self.assertEquals( dConfValues['call']['siteid'   ], '0'       )
        
        self.assertEquals( dConfValues['endpoints']['finding'],
                    'http://svcs.sandbox.ebay.com/services/search/FindingService/v1' )
        
        self.assertIsNotNone( dConfValues[ "keys"     ].get( "ebay_app_id" ) )

'''
do not test because downloaded file is HUGE:
    getMarketCategoriesGotSiteID()
    getMarketCategoriesGotGlobalID()

do test:
    getCategoryVersionGotSiteID()
    getCategoryVersionGotGlobalID()
    getItemsByKeyWords()
    getItemsByCategory()
    getItemsByBoth()
    getSingleItem()
    getItemStatus()
'''


