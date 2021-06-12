from ..models           import EbayCategory

from .base              import GetMarketsAndCategoriesWebTestSetUp, \
                               GetMarketsAndCategoriesTestPlusSetUp

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



class EbayCategoriesSetUpMixIn( object ):
    #
    '''new June 2021'''
    #
    def test_set_up_categories( self ):
        #
        '''test whether all the categories are in the table'''
        #
        self.assertEqual(
                EbayCategory.objects.all().count(), self.iCategories )



class EbayCategoriesWebSetUp(
        EbayCategoriesSetUpMixIn, GetMarketsAndCategoriesWebTestSetUp ):
    #
    # to avoid search ambiguity, for now, name is EbayCategoriesWebSetUp
    # change name to EbayCategoriesWebTestSetUp later
    #
    # the actual test comes in via mixin above
    #
    pass


class EbayCategoriesTestPlusSetUp(
        EbayCategoriesSetUpMixIn, GetMarketsAndCategoriesTestPlusSetUp ):
    #
    # the actual test comes in via mixin above
    #
    pass

