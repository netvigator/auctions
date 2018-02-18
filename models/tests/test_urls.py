from django.core.urlresolvers   import reverse, resolve

from django.test                import TestCase

from ..models                   import Model

# Create your tests here.

'''
no views implemented yet
class ModelsViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/models/')
        self.assertEqual(resp.status_code, 200)
'''


class TestURLs(TestCase):

    def test_list_reverse(self):
        """models:index should reverse to /models/."""
        self.assertEqual(reverse('models:index'), '/models/')

    def test_list_resolve(self):
        """/models/ should resolve to models:index."""
        self.assertEqual(resolve('/models/').view_name, 'models:index')

    def test_detail_reverse(self):
        """models:detail should reverse to /models/<pk>/."""
        self.assertEqual(
            reverse('models:detail', kwargs={ 'pk': 1 }),
            '/models/1/' )

    def test_detail_resolve(self):
        """/models/<pk>/ should resolve to models:detail."""
        self.assertEqual(resolve('/models/1/').view_name, 'models:detail')

    def test_edit_reverse(self):
        """models:edit should reverse to /models/edit/."""
        self.assertEqual(reverse('models:edit', kwargs={ 'pk': 1 }),
                         '/models/1/edit/')

    def test_edit_resolve(self):
        """/models/<pk>/edit/ should resolve to models:edit."""
        self.assertEqual(
            resolve('/models/1/edit/').view_name,
            'models:edit' )

    def test_delete_reverse(self):
        """models:delete should reverse to /models/<pk>/delete/."""
        self.assertEqual(reverse('models:delete', kwargs={ 'pk': 1 }),
                         '/models/1/delete/')

    def test_delete_resolve(self):
        """/models/<pk>/delete/ should resolve to models:delete."""
        self.assertEqual(
            resolve('/models/1/delete/').view_name,
            'models:delete' )

    def test_add_reverse(self):
        """models:add should reverse to /models/add/."""
        self.assertEqual(reverse('models:add'),
            '/models/add/')

    def test_add_resolve(self):
        """/models/add/ should resolve to models:add."""
        self.assertEqual(
            resolve('/models/add/').view_name,
            'models:add' )

