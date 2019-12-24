# import inspect

from core.utils_test    import getUrlQueryStringOff, queryGotUpdated

from .base              import BrandModelWebTestBase


class BrandModelWebTest( BrandModelWebTestBase ):


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

