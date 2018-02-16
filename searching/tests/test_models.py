from core.tests                 import BaseUserTestCase

from .forms                     import SearchAddOrUpdateForm
from .models                    import Search
from .test_big_text             import sExampleResponse
from .utils                     import getSearchResultGenerator




class SearchModelTest(BaseUserTestCase):

    def test_string_representation(self):
        sSearch = "My clever search 2"
        oSearch = Search( cTitle = sSearch )
        self.assertEqual( str(oSearch), oSearch.cTitle )

    def test_AddNewSearch(self):

        # has key words
        dData = dict(
                cTitle          = "My clever search 3",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertTrue( form.is_valid() )

        # has a category
        dData = dict(
                cTitle          = "My clever search 4",
                iDummyCategory  = 10,
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request

        self.assertTrue( form.is_valid() )
        # no key words, no category
        dData = dict(
                cTitle          = "My clever search 5",
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData ) 
        form.request = self.request
        self.assertFalse( form.is_valid() )

        # has an invalid category
        dData = dict(
                cTitle          = "My clever search 6",
                iDummyCategory  = 'abc',
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertFalse( form.is_valid() )


