

from ..models       import Keeper
from .test_utils    import StoreItemsTestPlus
from .base          import StoreItemsTestPlusBase

class TestUrlProcessing( StoreItemsTestPlusBase ):

    def test_get_reverse( self ):
        #
        oItem = Keeper.objects.get( pk = 142766343340 )
        #
        self.assertEqual( oItem.get_absolute_url(), '/keepers/142766343340/' )


