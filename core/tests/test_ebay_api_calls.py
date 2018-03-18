from django.test import TestCase

from ..ebay_api_calls import dEbayConf


class EbayWrapperTests(TestCase):
    '''ebay wrapper tests'''
    
    def test_get_ini_values(self):
        
        self.assertEquals( dEbayConf['call']['global_id'], 'EBAY-US' )
        self.assertEquals( dEbayConf['call']['siteid'   ], '0'       )
        
        self.assertEquals( dEbayConf['endpoints']['finding'],
                    'http://svcs.ebay.com/services/search/FindingService/v1' )

