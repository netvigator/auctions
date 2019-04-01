# import inspect

from core.utils_test    import ( BaseUserWebTestCase,
                                 getUrlQueryStringOff, queryGotUpdated )

# Create your tests here.

from ..models           import Brand


class BrandModelWebTest( BaseUserWebTestCase ):

    def setUp( self ):
        #
        super( BrandModelWebTest, self ).setUp()
        #
        oBrand = Brand(
            cTitle          = "My premium brand",
            iUser           = self.user1,
            id              = 1 )
        #
        oBrand.save()
        #
        self.oBrand = oBrand


    def test_string_representation(self):
        #
        self.assertEqual(str(self.oBrand), self.oBrand.cTitle)
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_get_absolute_url(self):
        """browser refresh trick: detail URL includes a UTC query string"""
        #
        tParts = getUrlQueryStringOff( self.oBrand.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/brands/%s/' % self.oBrand.id )
        #
        self.assertTrue( queryGotUpdated( tParts[1] ) )
        #
        self.assertFalse( queryGotUpdated( tParts[0] ) )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

