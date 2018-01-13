from django.test import TestCase

import datetime

# Create your tests here.

from markets.models             import Market
from .utils                     import getDateTimeObj
from .user_one                  import oUserOne
from .templatetags.core_tags    import getNbsp

from .ebay_wrapper              import oEbayConfig



def getDefaultMarket( caller ):
    
    if Market.objects.count() == 0:
        #
        market = Market()
        #
        market.id          = 1
        market.cMarket     = 'EBAY-US'
        market.cCountry    = 'US'
        market.iEbaySiteID = 1
        market.iCategoryVer= 117
        market.cCurrencyDef= 'USD'
        market.cLanguage   = 'en-US'
        market.save()
        
        caller.market = market

    # print( 'self.market.id:', Market.objects.filter( pk = 1 ) )



def CoreMarketTests(TestCase):
    #
    ''' need the default market '''
    #
    def setUp(self):
        getDefaultMarket( self )
    
    def test_default_market( self ):
        #
        assertIsNotNone( self.market.id )
        #
        assertEquals( self.market.id, 1 )


    
class CoreUserTests(TestCase):
    """User tests."""

    def setUp(self):
        getDefaultMarket( self )
    
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

class NbspTests(TestCase):
    '''test substituting &nbsp; for spaces'''
    def test_Nbsp(self):
        #
        self.assertEquals( getNbsp( "how now brown cow" ),
                           "how&nbsp;now&nbsp;brown&nbsp;cow" )

'''
oTest = {
    'cNationality': ('Nationality', 'C'),
    'iUser_id': ('Owner', 1), 
    'cLookFor': ('Considered A Hit If This Text Is Found (Each Line '
                 'Evaluated Separately, Put Different Look For Tests '
                 'On Different Lines)', None),
    'iLegacyKey': ('Legacy Key', 3140),
    'cComment': ('Comments', ''),
    'tLegacyModify': ('Legacy Row Updated On', None),
    'tModify': ('Updated On',
            datetime.datetime(2017, 11, 5, 6, 9, 49, 259192, tzinfo=<UTC>)),
    'id': ('Id', 1021),
    'cTitle': ('Brand Name', 'Addison'),
    'tLegacyCreate': ('Legacy Row Created On',
            datetime.datetime(2001, 9, 16, 23, 49, 9, tzinfo=<UTC>)),
    'tCreate': ('Created On',
            datetime.datetime(2017, 11, 5, 6, 9, 49, 259160, tzinfo=<UTC>)),
    'bAllOfInterest': ('Want Everything From This Brand?', False),
    'bWanted': ('Want Anything From This Brand?', True),
    'cExcludeIf': ('Not A Hit If This Text Is Found (Each Line Evaluated '
                   'Separately, Put Different Exclude Tests On Different '
                   'Lines)', ''),
    'iStars': ('Desireability, 10 Star Brand Is Most Desireable', 5),
    'iUser_id': ('Owner', 1),
    'NotOnList': ('blah blah blah', None }
'''