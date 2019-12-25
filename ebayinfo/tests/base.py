from core.utils_test    import ( getTableFromScreenCaptureGenerator,
                                 getNamePositionDict, TestCasePlus )

from ..models           import Market

from ebayinfo.tests     import ( EBAY_US_CURRENT_VERSION,
                                 EBAY_SG_CURRENT_VERSION,
                                 sMarketsTable )

from pyPks.Utils.Config import getBoolOffYesNoTrueFalse as getBool



class PutMarketsInDatabaseTestBase( TestCasePlus ):
    ''' set up for tests '''
    #
    def setUp(self):
        #
        super( PutMarketsInDatabaseTestBase, self ).setUp()
        #
        '''fetches the markets table text dump,
        uses that to populate the markets table.
        useful for testing, where the database starts empty.'''
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



