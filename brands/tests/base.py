from core.tests.base    import BaseUserWebTestCase

from ..models           import Brand

class BrandModelWebTestBase( BaseUserWebTestCase ):

    def setUp( self ):
        #
        super( BrandModelWebTestBase, self ).setUp()
        #
        oBrand = Brand(
            cTitle          = "My premium brand",
            iUser           = self.user1,
            id              = 1 )
        #
        oBrand.save()
        #
        self.oBrand = oBrand

