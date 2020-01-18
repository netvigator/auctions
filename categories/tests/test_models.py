from core.tests.base    import ( BaseUserWebTestCase,
                                 getUrlQueryStringOff, queryGotUpdated )

from ..models           import Category


class CategoryModelTest( BaseUserWebTestCase ):

    def test_string_representation(self):
        sCategory = "This category"
        oCategory = Category( cTitle = sCategory )
        self.assertEqual(str(sCategory), oCategory.cTitle)

    def test_get_absolute_url(self):
        """browser refresh trick: detail URL includes a UTC query string"""
        oCategory = Category(
            cTitle          = "My awesome category",
            iUser           = self.user1 )
        #
        oCategory.save()
        #
        tParts = getUrlQueryStringOff( oCategory.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/categories/%s/' % oCategory.id )
        #
        self.assertTrue( queryGotUpdated( tParts[1] ) )
        #
        self.assertFalse( queryGotUpdated( tParts[0] ) )

