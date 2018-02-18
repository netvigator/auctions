from django.core.urlresolvers   import reverse, resolve

from core.test_utils            import ( BaseUserTestCase,
                                         getUrlQueryStringOff, queryGotUTC )

from ..models                   import Category


# Create your tests here.


class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
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
        self.assertTrue( queryGotUTC( tParts[1] ) )
        #
        self.assertFalse( queryGotUTC( tParts[0] ) )

    def test_list_reverse(self):
        """searches:index should reverse to /categories/."""
        self.assertEqual(reverse('categories:index'), '/categories/')


    def test_list_resolve(self):
        """/categories/ should resolve to categories:index."""
        self.assertEqual(resolve('/categories/').view_name, 'categories:index')

    def test_detail_reverse(self):
        """categories:detail should reverse to /categories/<pk>/."""
        self.assertEqual(
            reverse('categories:detail', kwargs={ 'pk': 1 }),
            '/categories/1/'
        )

    def test_edit_reverse(self):
        """categories:edit should reverse to /categories/edit/."""
        self.assertEqual(reverse('categories:edit', kwargs={ 'pk': 1 }),
                         '/categories/1/edit/')

    def test_update_resolve(self):
        """/categories/~update/ should resolve to categories:update."""
        self.assertEqual(
            resolve('/categories/1/edit/').view_name,
            'categories:edit'
        )

