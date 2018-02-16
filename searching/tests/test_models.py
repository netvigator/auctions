from core.tests                 import BaseUserTestCase

from ..forms                     import SearchAddOrUpdateForm
from ..models                    import Search
from ..test_big_text             import sExampleResponse
from ..utils                     import getSearchResultGenerator




class SearchModelTest(BaseUserTestCase):

    def test_string_representation(self):
        sSearch = "My clever search 2"
        oSearch = Search( cTitle = sSearch )
        self.assertEqual( str(oSearch), oSearch.cTitle )


