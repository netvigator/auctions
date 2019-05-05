from core.dj_import     import reverse, resolve

from core.utils_test    import TestCasePlus


class TestURLs( TestCasePlus ):

    def test_list_reverse(self):
        """searching:index should reverse to /searching/."""
        self.assertEqual(reverse('searching:index'), '/searching/')

    def test_list_resolve(self):
        """/searching/ should resolve to searching:index."""
        self.assertEqual(resolve('/searching/').view_name, 'searching:index')

    def test_detail_reverse(self):
        """searching:detail should reverse to /searching/<pk>/."""
        self.assertEqual(
            reverse('searching:detail', kwargs={ 'pk': 1 }),
            '/searching/1/' )

    def test_detail_resolve(self):
        """/searching/<pk>/ should resolve to searching:detail."""
        self.assertEqual(resolve('/searching/1/').view_name, 'searching:detail')

    def test_edit_reverse(self):
        """searching:edit should reverse to /searching/edit/."""
        self.assertEqual(reverse('searching:edit', kwargs={ 'pk': 1 }),
                         '/searching/1/edit/')

    def test_edit_resolve(self):
        """/searching/<pk>/edit/ should resolve to searching:edit."""
        self.assertEqual(
            resolve('/searching/1/edit/').view_name,
            'searching:edit' )

    def test_delete_reverse(self):
        """searching:delete should reverse to /searching/<pk>/delete/."""
        self.assertEqual(reverse('searching:delete', kwargs={ 'pk': 1 }),
                         '/searching/1/delete/')

    def test_delete_resolve(self):
        """/searching/<pk>/delete/ should resolve to searching:delete."""
        self.assertEqual(
            resolve('/searching/1/delete/').view_name,
            'searching:delete' )

    def test_add_reverse(self):
        """searching:add should reverse to /searching/add/."""
        self.assertEqual(reverse('searching:add'),
            '/searching/add/')

    def test_add_resolve(self):
        """/searching/add/ should resolve to searching:add."""
        self.assertEqual(
            resolve('/searching/add/').view_name,
            'searching:add' )

