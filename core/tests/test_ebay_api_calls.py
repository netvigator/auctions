
from .base                  import TestCasePlus

from ..ebay_api_calls       import _getApiConfValues, _getListingTypeTuple

from pyPks.Time.Convert     import getDateTimeObjFromString
from pyPks.Time.Delta       import getDeltaDaysFromObjs


class GetConfFileValuesTests( TestCasePlus ):
    '''ebay API conf file values tests'''

    def setUp( self ):
        #
        self.dConfValues = _getApiConfValues()


    def test_ini_values(self):

        dConfValues = self.dConfValues

        self.assertEqual( dConfValues['call']['global_id'], 'EBAY-US' )
        self.assertEqual( dConfValues['call']['siteid'   ], '0'       )

        self.assertEqual( dConfValues['endpoints']['finding'],
                    'https://svcs.ebay.com/services/search/FindingService/v1' )

        self.assertIsNotNone( dConfValues[ "keys"     ].get( "ebay_app_id" ) )

        sTokenStart = 'AgAAAA**AQAAAA**aAAAAA**'

        self.assertEqual(
                dConfValues['auth']['token'][ : len( sTokenStart ) ],
                sTokenStart )

        dConfValues = _getApiConfValues( bUseSandbox = True )

        self.assertEqual( dConfValues['call']['global_id'], 'EBAY-US' )
        self.assertEqual( dConfValues['call']['siteid'   ], '0'       )

        self.assertEqual( dConfValues['endpoints']['finding'],
                    'http://svcs.sandbox.ebay.com/services/search/FindingService/v1' )

        sTokenStart = 'AgAAAA**AQAAAA**aAAAAA**'

        self.assertIsNotNone( dConfValues[ "keys"     ].get( "ebay_app_id" ) )
        self.assertEqual(
                dConfValues['auth']['token'][ : len( sTokenStart ) ],
                sTokenStart )

    def test_token_expiration( self ):
        '''tokens expire, keep tabs'''
        #
        sExpiration     = self.dConfValues['auth']['expires']
        #
        oExpiration     = getDateTimeObjFromString( sExpiration )
        #
        iDaysTillExpire = - int( getDeltaDaysFromObjs( oExpiration ) )
        #
        self.assertGreater( iDaysTillExpire, 15 )
        #
        if iDaysTillExpire <= 0:
            #
            print('')
            print( '### eBay AUTH token has expired or will soon!!! ###' )
            print( '### obtain new one from eBay developer webiste! ###' )
            print('')
            #
        elif iDaysTillExpire < 32:
            #
            print('')
            print( '### eBay AUTH token expires in %s days!!! ###' % iDaysTillExpire )
            print( '### obtain new one from eBay developer webiste! ###' )
            print('')


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



