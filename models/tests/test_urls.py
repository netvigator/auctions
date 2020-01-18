from django.urls        import reverse, resolve

from core.tests.base    import TestCasePlus


class TestURLs( TestCasePlus ):

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
                         '/models/edit/1/')

    def test_edit_resolve(self):
        """/models/<pk>/edit/ should resolve to models:edit."""
        self.assertEqual(
            resolve('/models/edit/1/').view_name,
            'models:edit' )

    def test_delete_reverse(self):
        """models:delete should reverse to /models/<pk>/delete/."""
        self.assertEqual(reverse('models:delete', kwargs={ 'pk': 1 }),
                         '/models/delete/1/')

    def test_delete_resolve(self):
        """/models/<pk>/delete/ should resolve to models:delete."""
        self.assertEqual(
            resolve('/models/delete/1/').view_name,
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

