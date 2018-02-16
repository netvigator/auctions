from django.core.urlresolvers   import reverse, resolve

from core.tests                 import ( BaseUserTestCase,
                                         getUrlQueryStringOff, queryGotUTC )

from .forms                     import SearchAddOrUpdateForm
from .models                    import Search



class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
        oSearch = Search(
            cTitle          = "My clever search 1",
            cKeyWords       = "Blah bleh blih",
            cPriority       = "A",
            iUser           = self.user1,
            id              = 1 )
        #
        oSearch.save()
        #
        tParts = getUrlQueryStringOff( oSearch.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/searching/%s/' % oSearch.id )
        #
        self.assertTrue( queryGotUTC( tParts[1] ) )
        #
        self.assertFalse( queryGotUTC( tParts[0] ) )

    def test_list_reverse(self):
        """searches:index should reverse to /searching/."""
        self.assertEqual(reverse('searching:index'), '/searching/')


    def test_list_resolve(self):
        """/searching/ should resolve to searching:index."""
        self.assertEqual(resolve('/searching/').view_name, 'searching:index')

    def test_detail_reverse(self):
        """searching:detail should reverse to /searching/<pk>/."""
        self.assertEqual(
            reverse('searching:detail', kwargs={ 'pk': 1 }),
            '/searching/1/'
        )

    def test_edit_reverse(self):
        """searching:edit should reverse to /searching/edit/."""
        self.assertEqual(reverse('searching:edit', kwargs={ 'pk': 1 }),
                         '/searching/1/edit/')

    def test_update_resolve(self):
        """/searching/~update/ should resolve to searching:update."""
        self.assertEqual(
            resolve('/searching/1/edit/').view_name,
            'searching:edit'
        )


