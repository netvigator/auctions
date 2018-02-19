from django.test.client import Client

from core.utils_testing import ( BaseUserTestCase,
                                 getUrlQueryStringOff, queryGotUTC )

from ..models           import Search

class SearchModelTest(BaseUserTestCase):

    def test_string_representation(self):
        sSearch = "My clever search 1"
        oSearch = Search( cTitle = sSearch )
        self.assertEqual( str(oSearch), oSearch.cTitle )

    def test_get_absolute_url(self):
        #
        self.client.login(username='username1', password='mypassword')
        #
        sSearch     = "My clever search 2"
        oSearch     = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        #
        tParts = getUrlQueryStringOff( oSearch.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/searching/%s/' % oSearch.id )
        #
        self.assertTrue( queryGotUTC( tParts[1] ) )
        #
        self.assertFalse( queryGotUTC( tParts[0] ) )

