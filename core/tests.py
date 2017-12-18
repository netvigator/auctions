from django.test import TestCase

# Create your tests here.

from .utils     import oUserOne

from .ebay_wrapper  import oEbayConfig

class CoreUserTests(TestCase):
    """User tests."""

    def test_get_user(self):
        
        self.assertEquals( oUserOne.username, 'aardvigator')


class EbayWrapperTests(TestCase):
    '''ebay wrapper tests'''
    
    def test_get_ini_values(self):
        
        self.assertEquals( oEbayConfig['call']['global_id'], 'EBAY-US' )
        
        self.assertEquals( oEbayConfig['research']['Token'], 'ENTER_HERE' )
        