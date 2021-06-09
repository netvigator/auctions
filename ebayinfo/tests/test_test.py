from ..models           import EbayCategory, Market

from core.tests.base    import GetEbayCategoriesWebTestSetUp

class TestEbayCategoriesSetUp( GetEbayCategoriesWebTestSetUp ):

    def test_set_up_categories( self ):
        #
        '''test whether all the categories are in the table'''
        #
        self.assertEqual(
                EbayCategory.objects.all().count(), self.iCategories )

