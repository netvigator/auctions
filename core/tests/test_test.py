from datetime                   import datetime, timezone

from django.core.exceptions     import ValidationError
from django.test                import TestCase

# Create your tests here.

from ..templatetags.core_tags   import getNbsp
from ..user_one                 import oUserOne
from ..utils                    import getDateTimeObjGotEbayStr as getDateTime

from ..utils_test               import (getUrlQueryStringOff,
                                        getEbayCategoriesSetUp,
                                        queryGotUpdated, getDefaultMarket )

from ebayinfo.models            import EbayCategory, Market


class TestingHelperTests(TestCase):
    #
    ''' test the testing helpers above (here)  '''
    #
    def setUp(self):
        #
        self.sURL1 = 'www.google.com/search?q=django+test+validation+assertRaises'
        self.sURL2 = 'www.google.com/search?updated=2008-04-17_14.28.28'
        self.sURL3 = 'www.google.com/search?updated=2008-04-17 14:28:28'
        #
        self.tParts = getUrlQueryStringOff( self.sURL1 )
        #
    #
    def test_URL_Parts(self):
        #
        self.assertEqual( self.tParts[0], 'www.google.com/search' )
        self.assertEqual( self.tParts[1], 'q=django+test+validation+assertRaises' )
    #
    def test_Query_Dont_Got_Updated(self):
        #
        self.assertFalse( queryGotUpdated( self.sURL1 ) )
        #
    #
    def test_Query_Got_Updated(self):
        #
        self.assertTrue( queryGotUpdated( self.sURL2 ) )
        #
    #
    def test_Query_Got_Invalid_Updated(self):
        #
        self.assertFalse( queryGotUpdated( self.sURL3 ) )
        #
    #




class CoreMarketTests(TestCase):
    #
    ''' need the default market '''
    #
    def setUp(self):
        self.market = getDefaultMarket()
    
    def test_default_market( self ):
        #
        self.assertIsNotNone( self.market.pk )
        #
        self.assertEqual( self.market.pk, 0 )





class CoreUserTests(TestCase):
    """ User tests."""

    def setUp(self):
        self.market = getDefaultMarket()
    
    def test_get_user(self):
        
        self.assertEqual( oUserOne.username, 'netvigator')



class DateTimeImportTests(TestCase):
    '''test converting ebay string dates into python datetime objects'''
    def test_convert_ebay_string_DateTime(self):
        #
        self.assertEqual(
                getDateTime( "2017-12-15T05:22:47.000Z" ),
                datetime(2017, 12, 15, 5, 22, 47, 0, timezone.utc ) )

class NbspTests(TestCase):
    '''test substituting &nbsp; for spaces'''
    def test_Nbsp(self):
        #
        self.assertEqual( getNbsp( "how now brown cow" ),
                           "how&nbsp;now&nbsp;brown&nbsp;cow" )


class TestEbayCategoriesSetUp(getEbayCategoriesSetUp):

    def test_set_up_categories( self ):
        #
        '''test whether all the categories are in the table'''
        #
        self.assertEqual(
                EbayCategory.objects.all().count(), self.iCategories )
