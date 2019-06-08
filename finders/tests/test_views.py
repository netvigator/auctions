import logging


from django.core.urlresolvers   import reverse

from core.utils_test            import ( SetUpBrandsCategoriesModelsTestPlus,
                                         BaseUserWebTestCase,
                                         setup_view_for_tests )

from core.utils                 import getExceptionMessageFromResponse

from searching.tests.test_stars import SetUpForHitStarsWebTests

from ..views                    import ( ItemsFoundIndexView,
                                         ItemFoundDetailView,
                                         ItemFoundUpdateView )


from pprint import pprint

class FindersNotYetViewTest( BaseUserWebTestCase ):
    """Brand views tests."""

    def test_no_finders_yet(self):
        #
        """
        If no finders exist, an appropriate message is displayed.
        """
        #
        response = self.client.get(reverse('finders:index'))

        self.assertEqual(response.status_code, 200)
        #
        self.assertQuerysetEqual(response.context['finders_list'], [])
        #
        self.assertContains(response, "No items have been found.")
        #
        #print('')
        #print('response.__dict__:')
        #print( response.__dict__ )
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


class FindersViewsTests( SetUpForHitStarsWebTests ):
    ''' test the finders views '''

    def test_finders_view( self ):
        #
        response = self.client.get(reverse('finders:index'))
        #
        self.assertEqual(response.status_code, 200)
        #
        self.assertGreater( len( response.context['finders_list'] ), 50 )
        #
        #print('')
        #print( "len( response.context['finders_list'] ):" )
        #print( len( response.context['finders_list'] ) )
        ##
        #print( "response.context['finders_list']:" )
        #print( pprint( response.context['finders_list'] ) )
        #
        #self.assertIn(
                #response.context['finders_list'],
               #'Altec 603 B 15" Speaker 604 803 Vintage' )
        #
        self.assertContains(response, "Altec 603" )
        self.assertContains(response, "Speaker 604 803 Vintage" )


    def test_finders_view_pass_params( self ):
        #
        response = self.client.get(
                reverse('finders:index', kwargs = {'select': 'D'} ) )
        #
        self.assertEqual(response.status_code, 200)
        #
        self.assertQuerysetEqual(response.context['finders_list'], [])
        #
        self.assertContains(response, "No items have been found.")
        #
        #
        response = self.client.get(
                reverse('finders:index', kwargs = {'select': 'P'} ) )
        #
        self.assertEqual(response.status_code, 200)
        #
        self.assertGreater( len( response.context['finders_list'] ), 80 )
        #print('')
        #print( "len( response.context['finders_list'] ):" )
        #print( len( response.context['finders_list'] ) )
        #
