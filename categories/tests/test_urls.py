
from django.urls        import reverse, resolve

from core.utils_test    import TestCasePlus

from ..models           import Category



class TestURLs( TestCasePlus ):

    def test_list_reverse(self):
        """categories:index should reverse to /categories/."""
        self.assertEqual(reverse('categories:index'), '/categories/')

    def test_list_resolve(self):
        """/categories/ should resolve to categories:index."""
        self.assertEqual(resolve('/categories/').view_name, 'categories:index')

    def test_detail_reverse(self):
        """categories:detail should reverse to /categories/<pk>/."""
        self.assertEqual(
            reverse('categories:detail', kwargs={ 'pk': 1 }),
            '/categories/1/' )

    def test_detail_resolve(self):
        """/categories/<pk>/ should resolve to categories:detail."""
        self.assertEqual(resolve('/categories/1/').view_name, 'categories:detail')

    def test_edit_reverse(self):
        """categories:edit should reverse to /categories/edit/."""
        self.assertEqual(reverse('categories:edit', kwargs={ 'pk': 1 }),
                         '/categories/1/edit/')

    def test_edit_resolve(self):
        """/categories/<pk>/edit/ should resolve to categories:edit."""
        self.assertEqual(
            resolve('/categories/1/edit/').view_name,
            'categories:edit' )

    def test_delete_reverse(self):
        """categories:delete should reverse to /categories/<pk>/delete/."""
        self.assertEqual(reverse('categories:delete', kwargs={ 'pk': 1 }),
                         '/categories/1/delete/')

    def test_delete_resolve(self):
        """/categories/<pk>/delete/ should resolve to categories:delete."""
        self.assertEqual(
            resolve('/categories/1/delete/').view_name,
            'categories:delete' )

    def test_add_reverse(self):
        """categories:add should reverse to /categories/add/."""
        self.assertEqual(reverse('categories:add'),
            '/categories/add/')

    def test_add_resolve(self):
        """/categories/add/ should resolve to categories:add."""
        self.assertEqual(
            resolve('/categories/add/').view_name,
            'categories:add' )

