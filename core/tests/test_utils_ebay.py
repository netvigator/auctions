from django.test            import TestCase

from ..utils_ebay           import getValueOffItemDict
from ..utils_test           import AssertEmptyMixin

from searching              import dItemFoundFields         # in __init__.py
from searching.tests        import sResponseItems2Test  # in __init__.py
from searching.utilsearch   import getSearchResultGenerator


class GetValueOffItemDictTests( AssertEmptyMixin, TestCase ):
    '''need to test getValueOffItemDict()'''

    def test_get_value_off_item_dict( self, **kwargs ):
        #
        oItemIter = getSearchResultGenerator( '', 1, sResponseItems2Test )
        #
        dItem = next( oItemIter )
        #
        dFields     = dItemFoundFields
        getValue    = getValueOffItemDict
        #
        dNewResult  = { k: getValue( dItem, k, v, **kwargs )
                        for k, v in dFields.items() }
        #
        self.assertIsNotNone( dNewResult.get( 'iCategoryID' ) )
        #
        self.assertEqual( dNewResult.get( 'iCategoryID' ), 38034 )
        #
        self.assertEmpty( dNewResult.get( 'i2ndCatHeirarchy' ) )
