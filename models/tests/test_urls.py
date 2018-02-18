from django.core.urlresolvers   import reverse, resolve

from core.test_utils            import ( BaseUserTestCase,
                                         getUrlQueryStringOff, queryGotUTC )

from categories.models          import Category

from ..models                   import Model

# Create your tests here.

'''
no views implemented yet
class ModelsViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/models/')
        self.assertEqual(resp.status_code, 200)
'''


class TestURLs(BaseUserTestCase):

    def setUp(self):
        #
        super( TestURLs, self ).setUp()
        #
        self.oCategory = Category(
            cTitle          = "My awesome category",
            iUser           = self.user1 )
        self.oCategory.save()
        #


    def test_get_absolute_url(self):
        
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
        self.assertTrue( queryGotUTC( tParts[1] ) )
        #
        self.assertFalse( queryGotUTC( tParts[0] ) )

    def test_list_reverse(self):
        """searches:index should reverse to /models/."""
        self.assertEqual(reverse('models:index'), '/models/')


    def test_list_resolve(self):
        """/models/ should resolve to models:index."""
        self.assertEqual(resolve('/models/').view_name, 'models:index')

    def test_detail_reverse(self):
        """models:detail should reverse to /models/<pk>/."""
        self.assertEqual(
            reverse('models:detail', kwargs={ 'pk': 1 }),
            '/models/1/'
        )

    def test_edit_reverse(self):
        """models:edit should reverse to /models/edit/."""
        self.assertEqual(reverse('models:edit', kwargs={ 'pk': 1 }),
                         '/models/1/edit/')

    def test_update_resolve(self):
        """/models/~update/ should resolve to models:update."""
        self.assertEqual(
            resolve('/models/1/edit/').view_name,
            'models:edit'
        )
