import logging
import inspect

from django.urls            import reverse

from core.tests.base        import ( SetUpBrandsCategoriesModelsTestPlus,
                                     BaseUserWebTestCase,
                                     setup_view_for_tests )

from core.utils             import getExceptionMessageFromResponse

from models.models          import Model

from .base                  import SetUpUserItemFoundWebTests

from ..models               import UserFinder, UserItemFound

from pprint import pprint

class FindersNotYetViewTest( BaseUserWebTestCase ):
    """Finders views tests."""

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


class FindersViewsTests( SetUpUserItemFoundWebTests ):

    ''' test the finders views '''

    def dont_test_finders_view( self ):
        #
        """
        Test got finders index
        """
        #
        response = self.client.get(reverse('finders:index'))
        #
        self.assertEqual(response.status_code, 200)
        #
        self.assertGreater( len( response.context['finders_list'] ), 50 )
        #
        self.assertContains(response, "Altec 603" )
        self.assertContains(response, "Speaker 604 803 Vintage" )
        #
        print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def dont_test_finders_view_pass_params( self ):
        #
        """
        Test got finders search params as query string
        """
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
                reverse('finders:index', kwargs = {'select': 'A'} ) )
        #
        self.assertEqual(response.status_code, 200)
        #
        self.assertGreater( len( response.context['finders_list'] ), 80 )
        #
        #
        response = self.client.get(
                reverse('finders:index', kwargs = {'select': 'D'} ) )
        #
        self.assertEqual(response.status_code, 200)
        #
        self.assertEqual( len( response.context['finders_list'] ), 0 )
        #
        #
        #print('')
        #print( "len( response.context['finders_list'] ):" )
        #print( len( response.context['finders_list'] ) )
        #
        #
        print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def dont_test_finders_detail( self ):
        #
        """
        Test got finders detail view
        """
        #
        response = self.client.get(
                reverse( 'finders:detail',
                        kwargs={ 'pk': self.oSample.id } ) )
        self.assertEqual(response.status_code, 200)
        #
        self.assertContains( response, "Altec Lansing" )
        self.assertContains( response, "542 Horn" )
        #
        print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



    def dont_test_finder_add_post(self):
        """
        Test post requests
        """
        oModel = Model.objects.get(
                cTitle = '311-90',
                iBrand = self.oBrand,
                iUser  = self.user1 )
        #
        data = dict(
                iItemNumb   = self.oSample,
                iBrand      = self.oBrand,
                iModel      = oModel,
                iCategory   = self.oCategory,
                iUser       = self.user1 )
        #
        # Create the request
        #
        response = self.client.post( reverse('finders:add'), data )
        #
        self.assertEqual( response.status_code, 200 )
        #
        print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_finder_edit( self ):
        #
        """
        Test finders edit
        """
        #
        oModel2 = Model.objects.get(
                cTitle = '811B',
                iBrand = self.oBrand,
                iUser  = self.user1 )

        data = dict( iModel = oModel2 )
        data['iBrand'] = self.oBrand
        data['iUser' ] = self.user1
        #
        print( 'data (dict):' )
        pprint( data )
        #
        # Create the request
        #
        response = self.client.post(
                reverse('finders:edit',
                        kwargs={ 'pk': self.oUserItemFound.id } ), data )
        #
        self.assertEqual( response.status_code, 200 )
        #
        #oUpdated = UserItemFound.objects.get( id = oUserItemFound.id )
        #
        #self.assertEqual( oUpdated.iModel, oModel2 )
        #
        print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
