from ..models           import EbayCategory

from .base              import GetMarketsAndCategoriesWebTestSetUp, \
                               GetMarketsAndCategoriesTestPlusSetUp

from core.tests.base    import GetEbayCategoriesWebTestSetUp




class TestEbayCategoriesSetUpMixIn( object ):
    #
    '''new June 2021'''
    #
    def test_set_up_categories( self ):
        #
        '''test whether all the categories are in the table'''
        #
        self.assertEqual(
                EbayCategory.objects.all().count(), self.iCategories )


class TestEbayCategoriesSetUp(
        TestEbayCategoriesSetUpMixIn, GetEbayCategoriesWebTestSetUp ):
    #
    '''obsolete when the changes started in June 2021 are complete'''
    #
    # the actual test comes in via mixin above
    #
    pass




class EbayCategoriesWebSetUp(
        TestEbayCategoriesSetUpMixIn, GetMarketsAndCategoriesWebTestSetUp ):
    #
    # to avoid search ambiguity, for now, name is EbayCategoriesWebSetUp
    # change name to EbayCategoriesWebTestSetUp later
    #
    # new June 2021
    #
    # the actual test comes in via mixin above
    #
    pass


class EbayCategoriesTestPlusSetUp(
        TestEbayCategoriesSetUpMixIn, GetMarketsAndCategoriesTestPlusSetUp ):
    #
    # new June 2021
    #
    # the actual test comes in via mixin above
    #
    pass

