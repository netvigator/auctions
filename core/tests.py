from django.test import TestCase

import datetime

# Create your tests here.

from .utils     import oUserOne, getDateTimeObj

from .ebay_wrapper  import oEbayConfig

class CoreUserTests(TestCase):
    """User tests."""

    def test_get_user(self):
        
        self.assertEquals( oUserOne.username, 'netvigator')


class EbayWrapperTests(TestCase):
    '''ebay wrapper tests'''
    
    def test_get_ini_values(self):
        
        self.assertEquals( oEbayConfig['call']['global_id'], 'EBAY-US' )
        
        self.assertEquals( oEbayConfig['research']['Token'], 'ENTER_HERE' )
        


class DateTimeImportTests(TestCase):
    '''test converting ebay string dates into python datetime objects'''
    def test_convert_ebay_string_DateTime(self):
        #
        self.assertEquals( getDateTimeObj( "2017-12-15T05:22:47.000Z" ),
                           datetime.datetime(2017, 12, 15, 5, 22, 47) )