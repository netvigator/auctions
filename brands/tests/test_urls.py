# import inspect

from django.core.urlresolvers   import reverse, resolve

from django.test                import TestCase

# Create your tests here.

from ..models                   import Brand



class TestURLs(TestCase):

    def test_list_reverse(self):
        """brands:index should reverse to /brands/."""
        self.assertEqual(reverse('brands:index'), '/brands/')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_list_resolve(self):
        """/brands/ should resolve to brands:index."""
        self.assertEqual(resolve('/brands/').view_name, 'brands:index')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_detail_reverse(self):
        """brands:detail should reverse to /brands/<pk>/."""
        self.assertEqual(
            reverse('brands:detail', kwargs={ 'pk': 1 }),
            '/brands/1/' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_detail_resolve(self):
        """/brands/<pk>/ should resolve to brands:detail."""
        self.assertEqual(resolve('/brands/1/').view_name, 'brands:detail')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_edit_reverse(self):
        """brands:edit should reverse to /brands/edit/."""
        self.assertEqual(reverse('brands:edit', kwargs={ 'pk': 1 }),
                         '/brands/1/edit/')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_edit_resolve(self):
        """/brands/<pk>/edit/ should resolve to brands:edit."""
        self.assertEqual(
            resolve('/brands/1/edit/').view_name,
            'brands:edit' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_delete_reverse(self):
        """brands:delete should reverse to /brands/<pk>/delete/."""
        self.assertEqual(reverse('brands:delete', kwargs={ 'pk': 1 }),
                         '/brands/1/delete/')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_delete_resolve(self):
        """/brands/<pk>/delete/ should resolve to brands:delete."""
        self.assertEqual(
            resolve('/brands/1/delete/').view_name,
            'brands:delete' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_add_reverse(self):
        """brands:add should reverse to /brands/add/."""
        self.assertEqual(reverse('brands:add'),
            '/brands/add/')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_add_resolve(self):
        """/brands/add/ should resolve to brands:add."""
        self.assertEqual(
            resolve('/brands/add/').view_name,
            'brands:add' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

