from core.utils_test    import ( getTableFromScreenCaptureGenerator,
                                 getNamePositionDict )

from core.utils_test    import TestCasePlus

# in __init__.py
from ebayinfo           import ( EBAY_US_CURRENT_VERSION,
                                 EBAY_SG_CURRENT_VERSION,
                                 sMarketsTable )

from .models            import Market

from pyPks.Utils.Config import getBoolOffYesNoTrueFalse as getBool


def getMarketsIntoDatabase():
    #
    '''fetches the markets table text dump,
    uses that to populate the markets table.
    useful for testing, where the database starts empty.'''
    #
    #
    #
    #
    oTableIter = getTableFromScreenCaptureGenerator( sMarketsTable )
    #
    lHeader = next( oTableIter )
    #
    d = getNamePositionDict( lHeader )
    #
    for lParts in oTableIter:
        #
        oMarket = Market(
                iEbaySiteID     = int(      lParts[ d['iEbaySiteID'    ] ] ),
                cMarket         =           lParts[ d['cMarket'        ] ],
                cCountry        =           lParts[ d['cCountry'       ] ],
                cLanguage       =           lParts[ d['cLanguage'      ] ],
                bHasCategories  = getBool(  lParts[ d['bHasCategories' ] ] ),
                cCurrencyDef    =           lParts[ d['cCurrencyDef'   ] ],
                iUtcPlusOrMinus = int(      lParts[ d['iUtcPlusOrMinus'] ] ) )
        #
        if lParts[ d['iCategoryVer'] ]:
            oMarket.iCategoryVer= int(      lParts[ d['iCategoryVer'   ] ] )
        #
        if lParts[ d['cUseCategoryID' ] ]:
            oMarket.cUseCategoryID=         lParts[ d['cUseCategoryID' ] ]
        #
        oMarket.save()



class PutMarketsInDatabaseTest( TestCasePlus ):
    '''test getMarketsIntoDatabase()'''
    #
    def setUp(self):
        #
        super( PutMarketsInDatabaseTest, self ).setUp()
        #
        getMarketsIntoDatabase()

    def test_market_count( self ):
        #
        iCount = Market.objects.all().count()
        #
        self.assertEqual( 23, iCount )

    def test_got_market_info_right( self ):
        #
        oUSA = Market.objects.get( cMarket = 'EBAY-US' )
        #
        self.assertEqual( oUSA.iEbaySiteID, 0 )
        #
        self.assertEqual( oUSA.cCurrencyDef, 'USD' )
        #
        self.assertEqual( oUSA.iCategoryVer, EBAY_US_CURRENT_VERSION )
        #
        oSG  = Market.objects.get( cMarket = 'EBAY-SG' )
        #
        self.assertEqual( oSG.iEbaySiteID, 216 )
        #
        self.assertEqual( oSG.iCategoryVer, EBAY_SG_CURRENT_VERSION )

