import datetime

from django.contrib.auth        import get_user_model
from django.core.exceptions     import ValidationError
from django.core.urlresolvers   import reverse, resolve
from django.http.request        import HttpRequest
from django.test                import TestCase, RequestFactory

# Create your tests here.

from categories.models          import Category
from ebaycategories.models      import EbayCategory
from markets.models             import Market


from .ebay_wrapper              import oEbayConfig
from .templatetags.core_tags    import getNbsp
from .user_one                  import oUserOne
from .utils                     import getDateTimeObj
from .validators                import gotTextOutsideParens





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


def getUrlQueryStringOff( sURL ):
    #
    ''' get URL parts, before and after ? for http query string '''
    #
    lParts = sURL.split('?')
    #
    lParts.append( '' )
    #
    return tuple( lParts )


def queryGotUTC( s ):
    #
    from String.Get import getTextAfter, getTextBefore
    from Time.Test  import isISOdatetimeFileNameSafe
    #
    sQueryUTC = getTextBefore(
                    getTextAfter( s, 'utc=' ),
                    '&',
                    bWantEmptyIfNoAfter = False )
    #
    return isISOdatetimeFileNameSafe( sQueryUTC )


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




def GotTextOutsideParensTests(TestCase):
    #
    ''' test the gotTextOutsideParens() validator '''
    #
    from .validators import gotTextOutsideParens
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


class BaseUserTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        
        getDefaultMarket( self )

        oUser = get_user_model()

        self.user1 = oUser.objects.create_user('username1', 'email@ymail.com')
        self.user1.set_password( 'mypassword')
        self.user1.first_name   = 'John'
        self.user1.last_name    = 'Citizen'
        self.user1.save()

        self.user2 = oUser.objects.create_user('username2', 'email@gmail.com')
        self.user2.set_password( 'mypassword')
        self.user2.first_name   = 'Joe'
        self.user2.last_name    = 'Blow'
        self.user2.save()
        
        self.user3 = oUser.objects.create_user( 'username3', 'email@hotmail.com' )
        self.user3.set_password( 'mypassword')
        self.user3.first_name   = 'Oscar'
        self.user3.last_name    = 'Zilch'
        self.user3.is_superuser = True
        self.user3.save()
        #
        self.request = HttpRequest()
        self.request.user = self.user1
        #
        if (  ( not isinstance( self.market, Market ) ) or
              ( not Market.objects.get( pk = 1 ) ) ):
            self.market = Market(
                cMarket     = 'EBAY-US',
                cCountry    = 'US',
                iEbaySiteID = 0,
                cLanguage   = 'en-US',
                iCategoryVer= 1,
                cCurrencyDef= 'USD' )
            self.market.save()
        #
        self.ebc = EbayCategory(
            iCategoryID = 10,
            name        = 'hot products',
            iLevel      = 1,
            iParentID   = 1,
            iTreeVersion= 1,
            iMarket     = self.market,
            bLeafCategory = False )
        self.ebc.save()
        #

    
class CoreUserTests(TestCase):
    """ User tests."""

    def setUp(self):
        getDefaultMarket( self )
    
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