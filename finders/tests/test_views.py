import logging

from django.urls            import reverse
from django.utils           import timezone

from core.tests.base        import ( SetUpBrandsCategoriesModelsTestPlus,
                                     BaseUserWebTestCase,
                                     setup_view_for_tests )

from core.utils             import getExceptionMessageFromResponse

from brands.models          import Brand
from categories.models      import Category
from models.models          import Model
from searching.models       import Search

from ..models               import UserFinder, UserItemFound

from searching.tests.base   import SetUpForHitStarsWebTests


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


class FindersViewsTests( SetUpForHitStarsWebTests ):
    ''' test the finders views '''

    def test_finders_view( self ):
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


    def test_finders_view_pass_params( self ):
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

    def test_finders_detail( self ):
        #
        """
        Test got finders detail view
        """
        #
        oSample = UserFinder.objects.get(
            cTitle = 'Altec Lansing 288-8K High Frequency Drive MRII 542 Horn',
            iUser = self.user1 )
        #
        iSampleID = oSample.id
        #
        response = self.client.get(
                reverse( 'finders:detail', kwargs={ 'pk': iSampleID } ) )
        self.assertEqual(response.status_code, 200)
        #
        self.assertContains( response, "Altec Lansing" )
        self.assertContains( response, "542 Horn" )



    #def test_finders_hit( self ):
        ##
        #"""
        #Test got finders hit
        #"""
        ##
        #oBrand = Brand.objects.get(
                #cTitle = 'Altec-Lansing',
                #iUser  = self.user1 )
        #oModel = Model.objects.get(
                #cTitle = 'N-1500A',
                #iBrand = oBrand,
                #iUser  = self.user1 )
        #oCategory = Category.objects.get(
                #cTitle = 'Crossover',
                #iUser  = self.user1 )
        ##
        #oSample = UserItemFound.objects.get(
                #iBrand      = oBrand,
                #iModel      = oModel,
                #iCategory   = oCategory,
                #iUser       = self.user1 )
        ##
        ##print(oSample)
        ##
        #iSampleID = oSample.id
        ##
        #response = self.client.get(
                #reverse( 'finders:hit', kwargs={ 'pk': iSampleID } ) )
        #self.assertEqual(response.status_code, 200)
        ##
        #self.assertContains( response, "Altec-Lansing" )
        #self.assertContains( response, "N-1500A" )
        #self.assertContains( response, "Crossover" )


    def test_finder_add_post(self):
        """
        Test post requests
        """
        oSample = UserFinder.objects.get(
            cTitle = 'Altec Lansing 288-8K High Frequency Drive MRII 542 Horn',
            iUser = self.user1 )
        #
        oBrand = Brand.objects.get(
                cTitle = 'Altec-Lansing',
                iUser  = self.user1 )
        oModel = Model.objects.get(
                cTitle = '311-90',
                iBrand = oBrand,
                iUser  = self.user1 )
        oCategory = Category.objects.get(
                cTitle = 'Horn',
                iUser  = self.user1 )
        #
        data = dict(
                iItemNumb   = oSample,
                iBrand      = oBrand,
                iModel      = oModel,
                iCategory   = oCategory,
                iUser       = self.user1 )
        #
        # Create the request
        #
        response = self.client.post( reverse('finders:add'), data )
        #
        self.assertEqual( response.status_code, 200 )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_finder_edit( self ):
        #
        """
        Test finders edit
        """
        #
        oSample = UserFinder.objects.get(
            cTitle = 'Altec Lansing 288-8K High Frequency Drive MRII 542 Horn',
            iUser = self.user1 )
        #
        oBrand = Brand.objects.get(
                cTitle = 'Altec-Lansing',
                iUser  = self.user1 )
        oModel1 = Model.objects.get(
                cTitle = '511A',
                iBrand = oBrand,
                iUser  = self.user1 )
        oCategory = Category.objects.get(
                cTitle = 'Horn',
                iUser  = self.user1 )
        #
        oSearch = Search.objects.all()[1]
        #
        oUserItemFound = UserItemFound(
                iItemNumb   = oSample.iItemNumb,
                iBrand      = oBrand,
                iModel      = oModel1,
                iCategory   = oCategory,
                iUser       = self.user1,
                iSearch     = oSearch,
                tCreate     = timezone.now() )
        #
        oUserItemFound.save()
        #
        oModel2 = Model.objects.get(
                cTitle = '811B',
                iBrand = oBrand,
                iUser  = self.user1 )

        data = dict( iModel = oModel2 )
        #
        # Create the request
        #
        response = self.client.post(
                reverse('finders:edit',
                        kwargs={ 'pk': oUserItemFound.id } ), data )
        #
        self.assertEqual( response.status_code, 200 )
        #
        #oUpdated = UserItemFound.objects.get( id = oUserItemFound.id )
        #
        #self.assertEqual( oUpdated.iModel, oModel2 )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
