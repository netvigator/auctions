import inspect

from django.utils       import timezone

from .base              import TestCasePlus

from ..ebay_api_calls   import getApiConfValues, _getListingTypeTuple, \
                               _ApplicationtToken, _getRequestHeaders, \
                               _getApplicationRequestBody, lScopes, \
                               getApplicationToken

from pyPks.Time.Convert import getIsoDateTimeFromObj

sTokenStart = 'AgAAAA**AQAAAA**aAAAAA**'


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


        self.assertEqual(
                dConfValues['auth']['token'][ : len( sTokenStart ) ],
                sTokenStart )

        dConfValues = getApiConfValues( bUseSandbox = True )

        self.assertEqual( dConfValues['call']['global_id'], 'EBAY-US' )
        self.assertEqual( dConfValues['call']['siteid'   ], '0'       )

        self.assertEqual( dConfValues['endpoints']['finding'],
                    'https://svcs.sandbox.ebay.com/services/search/FindingService/v1' )

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



class AuthTokenTests( TestCasePlus ):
    '''ebay API conf file values tests'''

    def setUp( self ):
        #
        self.dConfValues = getApiConfValues()

    def test_auth_object( self ):
        #
        oTest = _ApplicationtToken( error = 'abc' )
        #
        self.assertEqual( str( oTest ), '{"error": "abc"}' )
        #
        oSomeLater = timezone.now() + timezone.timedelta( seconds = 7200 )
        #
        oTest = _ApplicationtToken(
                    access_token = sTokenStart,
                    tokenExpires = oSomeLater )
        #
        sExpect = ( '{"access_token": "%s", "expires": "%s"}' %
                     (  sTokenStart,
                        getIsoDateTimeFromObj( oSomeLater ) ) )
        #
        self.assertEqual( str( oTest ), sExpect )
        #
        oMoreLter = timezone.now() + timezone.timedelta( seconds = 2 * 7200 )
        #
        oTest = _ApplicationtToken(
                    access_token        = sTokenStart,
                    tokenExpires        = oSomeLater,
                    refresh_token       = sTokenStart.swapcase(),
                    refreshExpires= oMoreLter )
        #
        sExpect = ( '{"access_token": "%s", "expires": "%s", '
                    '"refresh_token": "%s", "expires": "%s"}' %
                    ( sTokenStart,
                      getIsoDateTimeFromObj( oSomeLater ),
                      sTokenStart.swapcase(),
                      getIsoDateTimeFromObj( oMoreLter ) ) )
        #
        self.assertEqual( str( oTest ), sExpect )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_request_headers( self ):
        #
        dHeaders = _getRequestHeaders( self.dConfValues )
        #
        self.assertIn( 'Authorization', dHeaders )
        self.assertIn( 'Content-Type',  dHeaders )
        #
        self.assertEqual(
                dHeaders['Content-Type'],
                'application/x-www-form-urlencoded' )
        #
        self.assertTrue( dHeaders['Authorization'].startswith( 'Basic ') )
        #
        self.assertEqual( len( dHeaders['Authorization'] ), 110 )


    def test_request_body( self ):
        #
        dBody = _getApplicationRequestBody( self.dConfValues, lScopes )
        #
        self.assertIn( 'grant_type',    dBody )
        self.assertIn( 'scope',         dBody )
        #
        self.assertEqual( dBody['grant_type'], 'client_credentials' )

        self.assertEqual( dBody['scope'],
                          'https://api.ebay.com/oauth/api_scope' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_get_token( self ):
        #
        oToken = getApplicationToken( bUseSandbox = True )
        #
        self.assertIsNotNone( oToken )
        #
        self.assertIsNone( oToken.error )
        #
        self.assertGreater( oToken.tokenExpires, timezone.now() )
        #
        self.assertGreater( len( oToken.access_token ), 1800 )
        #
        self.assertTrue( oToken.access_token.startswith( 'v^' ) )



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




