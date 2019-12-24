from core.utils_test    import TestCasePlus

from ..utils_test       import getMarketsIntoDatabase

from ..models           import Market

from ebayinfo.tests     import ( EBAY_US_CURRENT_VERSION,
                                 EBAY_SG_CURRENT_VERSION )

class PutMarketsInDatabaseTestBase( TestCasePlus ):
    '''test getMarketsIntoDatabase()'''
    #
    def setUp(self):
        #
        super( PutMarketsInDatabaseTestBase, self ).setUp()
        #
        getMarketsIntoDatabase()




