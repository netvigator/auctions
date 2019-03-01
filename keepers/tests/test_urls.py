

from ..models           import Keeper
from .test_utils        import StoreItemsTest


class TestUrlProcessing( StoreItemsTest ):


    def test_get_reverse( self ):
        #
        oItem = Keeper.objects.get( pk = 142766343340 )
        #
        self.assertEqual( oItem.get_absolute_url(), '/keepers/142766343340' )


