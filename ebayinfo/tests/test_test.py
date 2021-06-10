from ..models           import EbayCategory

from .base              import GetMarketsAndCategoriesWebTestSetUp

from core.tests.base    import GetEbayCategoriesWebTestSetUp

class TestEbayCategoriesSetUp( GetEbayCategoriesWebTestSetUp ):
    #
    '''obsolete when the changes started in June 2021 are complete'''
    #

    def test_set_up_categories( self ):
        #
        '''test whether all the categories are in the table'''
        #
        self.assertEqual(
                EbayCategory.objects.all().count(), self.iCategories )



class EbayCategoriesWebSetUp( GetMarketsAndCategoriesWebTestSetUp ):
    #
    '''new June 2021'''
    #
    def test_set_up_categories( self ):
        #
        '''test whether all the categories are in the table'''
        #
        self.assertEqual(
                EbayCategory.objects.all().count(), self.iCategories )
