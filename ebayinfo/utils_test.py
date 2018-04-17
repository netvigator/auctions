from django.test    import TestCase

from core.utils_test import ( getTableFromScreenCaptureGenerator,
                              getNamePositionDict )

from .models        import Market

def getMarketsIntoDatabase():
    #
    '''fetches the markets table text dump,
    uses that to populate the markets table.
    useful for testing, where the database starts empty.'''
    #
    from ebayinfo           import sMarketsTable # in __init__.py
    #
    #
    from Utils.Config       import getBoolOffYesNoTrueFalse as getBool
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
        


class PutMarketsInDatabaseTest(TestCase):
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
        self.assertEqual( oUSA.iCategoryVer, 118 )
        #
        oSG  = Market.objects.get( cMarket = 'EBAY-SG' )
        #
        self.assertEqual( oSG.iEbaySiteID, 216 )
        #
        self.assertEqual( oSG.iCategoryVer, 31 )

