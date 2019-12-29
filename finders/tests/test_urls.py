# import inspect

from django.urls        import reverse, resolve

from core.utils_test    import TestCasePlus



class TestURLs( TestCasePlus ):

    def test_list_reverse(self):
        """finders:index should reverse to /finders/."""
        self.assertEqual(reverse('finders:index'), '/finders/')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_list_resolve(self):
        """/finders/ should resolve to finders:index."""
        self.assertEqual(resolve('/finders/').view_name, 'finders:index')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_detail_reverse(self):
        """finders:detail should reverse to /finders/<pk>/."""
        self.assertEqual(
            reverse('finders:detail', kwargs={ 'pk': 1 }),
            '/finders/1/' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_detail_resolve(self):
        """/finders/<pk>/ should resolve to finders:detail."""
        self.assertEqual(resolve('/finders/1/').view_name, 'finders:detail')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_edit_reverse(self):
        """finders:edit should reverse to /finders/edit/."""
        self.assertEqual(reverse('finders:edit', kwargs={ 'pk': 1 }),
                         '/finders/edit/1/')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_edit_resolve(self):
        """/finders/<pk>/edit/ should resolve to finders:edit."""
        self.assertEqual(
            resolve('/finders/edit/1/').view_name,
            'finders:edit' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_hit_resolve(self):
        """/finders/<pk>/edit/ should resolve to finders:edit."""
        self.assertEqual(
            resolve('/finders/hit/1/').view_name,
            'finders:hit' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_hit_reverse(self):
        """finders:edit should reverse to /finders/edit/."""
        self.assertEqual(reverse('finders:hit', kwargs={ 'pk': 1 }),
                         '/finders/hit/1/')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_add_resolve(self):
        """/finders/<pk>/edit/ should resolve to finders:edit."""
        self.assertEqual(
            resolve('/finders/add/').view_name,
            'finders:add' )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_add_reverse(self):
        """finders:edit should reverse to /finders/edit/."""
        self.assertEqual(reverse('finders:add' ), '/finders/add/')
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    #def test_delete_reverse(self):
        #"""finders:delete should reverse to /finders/<pk>/delete/."""
        #self.assertEqual(reverse('finders:delete', kwargs={ 'pk': 1 }),
                         #'/finders/delete/1/')
        ##
        ## print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    #def test_delete_resolve(self):
        #"""/finders/<pk>/delete/ should resolve to finders:delete."""
        #self.assertEqual(
            #resolve('/finders/delete/1/').view_name,
            #'finders:delete' )
        ##
        ## print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    #def test_add_reverse(self):
        #"""finders:add should reverse to /finders/add/."""
        #self.assertEqual(reverse('finders:add'),
            #'/finders/add/')
        ##
        ## print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    #def test_add_resolve(self):
        #"""/finders/add/ should resolve to finders:add."""
        #self.assertEqual(
            #resolve('/finders/add/').view_name,
            #'finders:add' )
        ##
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

