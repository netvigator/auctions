from django.test.client import Client

from core.test_utils    import (
                        BaseUserTestCase, getUrlQueryStringOff, queryGotUTC )

from ..forms            import SearchAddOrUpdateForm
from ..models           import Search
from ..utils            import getSearchResultGenerator

from .test_big_text     import sExampleResponse



class SearchModelTest(BaseUserTestCase):

    def test_string_representation(self):
        sSearch = "My clever search 2"
        oSearch = Search( cTitle = sSearch )
        self.assertEqual( str(oSearch), oSearch.cTitle )

    def test_get_absolute_url(self):
        #
        self.client.login(username='username1', password='mypassword')
        #
        sSearch     = "Great Widgets"
        oSearch     = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        #
        tUrlParts   = getUrlQueryStringOff( oSearch.get_absolute_url() )
        #
        self.assertEqual( tUrlParts[0], '/searching/%s/' % oSearch.id )
        #
        self.assertTrue( queryGotUTC( tUrlParts[1] ) )

