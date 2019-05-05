import logging

from django.core.urlresolvers   import reverse

from core.utils_test            import ( SetUpBrandsCategoriesModelsTestPlus,
                                         BaseUserWebTestCase,
                                         setup_view_for_tests )

from core.utils                 import getExceptionMessageFromResponse

from searching.tests.test_stars import SetUpForHitStarsWebTests

from ..views                    import ( ItemsFoundIndexView,
                                         ItemFoundDetailView,
                                         ItemFoundUpdateView )



class ItemsFoundViewsTests( SetUpForHitStarsWebTests ):
    ''' test the items found views '''

    def test_items_found_view( self ):
        #
        pass

