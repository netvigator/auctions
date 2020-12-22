from core.tests.base        import TestCasePlus

from ..models               import Market

from ebayinfo.tests         import sMarketsTable, sPriorMarketsTable
from ebayinfo.tests.utils   import getMarketsDict


dMarkets = getMarketsDict( sMarketsTable )


class PutMarketsInDatabaseTestBase( TestCasePlus ):
    ''' set up for tests '''
    #
    def setUp(self):
        #
        super().setUp()
        #
        '''fetches the markets table text dump,
        uses that to populate the markets table.
        useful for testing, where the database starts empty.'''
        #
        #
        for k, v in dMarkets.items():
            #
            oMarket = Market(
                iEbaySiteID     = k,
                cMarket         = v.cMarket,
                cCountry        = v.cCountry,
                iCategoryVer    = v.iCategoryVer,
                cLanguage       = v.cLanguage,
                bHasCategories  = v.bHasCategories,
                cCurrencyDef    = v.cCurrencyDef,
                iUtcPlusOrMinus = v.iUtcPlusOrMinus,
                cUseCategoryID  = v.cUseCategoryID )
            #
            oMarket.save()
