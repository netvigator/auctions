from django.test        import TestCase

from django.test.client import Client

from core.utils_test    import ( BaseUserTestCase,
                                 getUrlQueryStringOff, queryGotUpdated )

from searching          import ( EBAY_SHIPPING_CHOICES, getChoiceCode,
                                 dEBAY_SHIPPING_CHOICE_CODE )

from ..models           import Search

class SearchModelTest(BaseUserTestCase):

    def test_string_representation(self):
        sSearch = "My clever search 2"
        oSearch = Search( cTitle = sSearch )
        self.assertEqual( str(oSearch), oSearch.cTitle )

    def test_get_absolute_url(self):
        #
        self.client.login(username='username1', password='mypassword')
        #
        sSearch     = "My clever search 1"
        oSearch     = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        #

        tParts = getUrlQueryStringOff( oSearch.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/searching/%s/' % oSearch.id )
        #
        self.assertTrue( queryGotUpdated( tParts[1] ) )
        #
        self.assertFalse( queryGotUpdated( tParts[0] ) )


class TestChoices(TestCase):

    def test_CHOICES( self ):
        """ test the ebay shipping choices tuple """
        self.assertEqual( EBAY_SHIPPING_CHOICES[5], ( 5, 'Free Pick up' ) )

    def test_dCHOICE_CODES( self ):
        """ test the ebay shipping choices dictionary """
        self.assertEqual( dEBAY_SHIPPING_CHOICE_CODE['FreePickup'], 5 )

    def test_getChoiceCode( self ):
        """ test the ebay shipping choice code function """
        self.assertEqual( getChoiceCode('FreePickup'), 5 )
