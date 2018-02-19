from core.utils_testing         import ( BaseUserTestCase,
                                         getUrlQueryStringOff, queryGotUpdated )

# Create your tests here.

from ..models                   import Brand


class ModelModelTest(BaseUserTestCase):

    def test_string_representation(self):
        sBrand = "My brand name"
        oBrand = Brand(cTitle= sBrand )
        self.assertEqual(str(oBrand), oBrand.cTitle)

    def test_get_absolute_url(self):
        """browser refresh trick: detail URL includes a UTC query string"""
        oBrand = Brand(
            cTitle          = "My premium brand",
            iUser           = self.user1,
            id              = 1 )
        oBrand.save()
        #
        tParts = getUrlQueryStringOff( oBrand.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/brands/%s/' % oBrand.id )
        #
        self.assertTrue( queryGotUpdated( tParts[1] ) )
        #
        self.assertFalse( queryGotUpdated( tParts[0] ) )
        
