from core.tests.base        import TestCasePlus
from django_webtest         import WebTest

from ..models               import Market

from ebayinfo.tests         import sMarketsTable, sPriorMarketsTable
from ebayinfo.tests.utils   import getMarketsDict


dMarkets = getMarketsDict( sMarketsTable )


class PutMarketsInDatabaseMixIn( object ):

    @classmethod
    def setUpTestData(self):
        #
        '''fetches the markets table text dump,
        uses that to populate the markets table.
        useful for testing, where the database starts empty.'''
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



class PutMarketsInDatabaseTestPlusBase( PutMarketsInDatabaseMixIn, TestCasePlus ):
    ''' set up for tests '''
    #
    pass


class PutMarketsInDatabaseWebTestBase( PutMarketsInDatabaseMixIn, WebTest ):
    ''' set up for tests '''
    #
    pass

