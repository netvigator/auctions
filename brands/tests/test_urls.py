from django.core.urlresolvers   import reverse, resolve

from core.test_utils            import ( BaseUserTestCase,
                                         getUrlQueryStringOff, queryGotUTC )

# Create your tests here.

from ..models                   import Brand



class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
        oBrand = Brand(
            cTitle          = "My premium brand",
            iUser           = self.user1,
            id              = 1 )
        oBrand.save()
        #
        tParts = getUrlQueryStringOff( oBrand.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/brands/%s/' % oBrand.id )
        #
        self.assertTrue( queryGotUTC( tParts[1] ) )
        #
        self.assertFalse( queryGotUTC( tParts[0] ) )
        

    def test_list_reverse(self):
        """searches:index should reverse to /brands/."""
        self.assertEqual(reverse('brands:index'), '/brands/')


    def test_list_resolve(self):
        """/brands/ should resolve to brands:index."""
        self.assertEqual(resolve('/brands/').view_name, 'brands:index')

    def test_detail_reverse(self):
        """brands:detail should reverse to /brands/<pk>/."""
        self.assertEqual(
            reverse('brands:detail', kwargs={ 'pk': 1 }),
            '/brands/1/' )

    def test_edit_reverse(self):
        """brands:edit should reverse to /brands/edit/."""
        self.assertEqual(reverse('brands:edit', kwargs={ 'pk': 1 }),
                         '/brands/1/edit/')

    def test_edit_resolve(self):
        """/brands/~edit/ should resolve to brands:edit."""
        self.assertEqual(
            resolve('/brands/1/edit/').view_name,
            'brands:edit' )

