from core.tests.base    import ( BaseUserWebTestCase,
                                 getUrlQueryStringOff, queryGotUpdated )

from categories.models  import Category

from ..models           import Model

class ModelModelTest( BaseUserWebTestCase ):

    def test_string_representation(self):
        sModel = "My model name/number"
        oModel = Model(cTitle= sModel )
        self.assertEqual(str(sModel), oModel.cTitle)

    def test_get_absolute_url(self):
        """browser refresh trick: detail URL includes a UTC query string"""
        self.oCategory = Category(
            cTitle          = "My awesome category",
            iUser           = self.user1 )
        self.oCategory.save()
        #
        oModel = Model(
            cTitle          = "My stellar model",
            iUser           = self.user1,
            iCategory       = self.oCategory )
        #
        oModel.save()
        #
        tParts = getUrlQueryStringOff( oModel.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/models/%s/' % oModel.id )
        #
        self.assertTrue( queryGotUpdated( tParts[1] ) )
        #
        self.assertFalse( queryGotUpdated( tParts[0] ) )

