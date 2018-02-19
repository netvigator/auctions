import datetime

from django.core.exceptions     import ValidationError
from django.test                import TestCase

# Create your tests here.

from ..ebay_wrapper             import oEbayConfig
from ..templatetags.core_tags   import getNbsp
from ..user_one                 import oUserOne
from ..utils                    import getDateTimeObj
from ..validators               import gotTextOutsideParens

from ..utils_testing            import (getUrlQueryStringOff,
                                        queryGotUTC, getDefaultMarket )


def TestingHelperTests(TestCase):
    #
    ''' test the testing helpers above (here)  '''
    #
    sURL = 'www.google.com/search?q=django+test+validation+assertRaises'
    #
    tParts = getUrlQueryStringOff( sURL )
    #
    def test_URL_Parts(self):
        #
        self.assertEquals( tParts[0], 'www.google.com/search' )
        self.assertEquals( tParts[1], 'q=django+test+validation+assertRaises' )
    #
    #
    def test_Query_Dont_Got_UTC(self):
        #
        self.assertFalse( queryGotUTC, sURL )
        #
    sURL = 'www.google.com/search?utc=2008-04-17_14.28.28'
    #
    def test_Query_Got_UTC(self):
        #
        self.assertTrue( queryGotUTC, sURL )
        #
    #
    sURL = 'www.google.com/search?utc=2008-04-17 14:28:28'
    #
    def test_Query_Got_Invalid_UTC(self):
        #
        self.assertTrue( queryGotUTC, sURL )
        #




def CoreMarketTests(TestCase):
    #
    ''' need the default market '''
    #
    def setUp(self):
        self.market = getDefaultMarket()
    
    def test_default_market( self ):
        #
        assertIsNotNone( self.market.id )
        #
        assertEquals( self.market.id, 1 )





def GotTextOutsideParensTests(TestCase):
    #
    ''' test the gotTextOutsideParens() validator '''
    #
    s1 = 'abcde (efghijk)'
    s2 = 'abcde'
    s1 = ' (efghijk) '
    
    def test_OK_titles( self ):
        #
        try:
            gotTextOutsideParens( s1 )
            gotTextOutsideParens( s2 )
        except ExceptionType:
            self.fail("gotTextOutsideParens() raised ExceptionType unexpectedly!")
    #
    def test_bad_title( self ):
        #
        with self.assertRaises( ValidationError):
            gotTextOutsideParens( s3 )


class CoreUserTests(TestCase):
    """ User tests."""

    def setUp(self):
        self.market = getDefaultMarket()
    
    def test_get_user(self):
        
        self.assertEquals( oUserOne.username, 'netvigator')


class EbayWrapperTests(TestCase):
    ''' ebay wrapper tests '''
    
    def test_get_ini_values(self):
        
        self.assertEquals( oEbayConfig['call']['global_id'], 'EBAY-US' )
        
        self.assertEquals( oEbayConfig['research']['Token'], 'ENTER_HERE' )
        


class DateTimeImportTests(TestCase):
    '''test converting ebay string dates into python datetime objects'''
    def test_convert_ebay_string_DateTime(self):
        #
        self.assertEquals( getDateTimeObj( "2017-12-15T05:22:47.000Z" ),
                           datetime.datetime(2017, 12, 15, 5, 22, 47) )

class NbspTests(TestCase):
    '''test substituting &nbsp; for spaces'''
    def test_Nbsp(self):
        #
        self.assertEquals( getNbsp( "how now brown cow" ),
                           "how&nbsp;now&nbsp;brown&nbsp;cow" )

