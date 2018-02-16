from django.core.urlresolvers   import reverse
from django.test.client         import Client, RequestFactory

from core.tests                 import BaseUserTestCase
from core.utils                 import getExceptionMessageFromResponse

from .models                    import Search

from .views                     import (
        SearchCreate, IndexView, SearchDetail, SearchDelete, SearchUpdate )


# from pprint import pprint

# Create your tests here.

class SearchViewsHitButtons(BaseUserTestCase):
    """
    Test Save and Cancel
    """
    def setUp(self):
        #
        super( SearchViewsHitButtons, self ).setUp()
        #
        self.factory = RequestFactory()
    

    def test_get(self):
        """
        Test GET requests
        """
        request = self.factory.get(reverse('searching:add'))
        request.user = self.user1
        #
        response = SearchCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)
        #print( 'response.context_data has form and view, view keys:' )
        #for k in response.context_data['view'].__dict__:
            #print( k )
        #self.assertEqual(response.context_data['iUser'], self.user1)
        self.assertEqual(response.context_data['view'].__dict__['request'], request)


    # @patch('searching.models.Search.save', MagicMock(name="save"))
    def test_post(self):
        """
        Test post requests
        """
        data = dict( cTitle = "Great Widgets", iUser = self.user1 )
        # Create the request
        response = self.client.post(reverse('searching:add'), data )
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 302)
        #oSearch = Search.objects.get( cTitle = "Great Widgets" )
        #self.assertEqual( oSearch, self.searching )


        
    #def test_add_hit_cancel(self):
        ##
        #"""
        #Hit cancel when adding
        #"""
        #self.client = Client()
        ##
        #self.client.login(username='username1', password='mypassword')
        ##
        #sSearch = "Great Widgets"
        #oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        ##
        ##
    #

class SearchViewsTests(BaseUserTestCase):

    def test_no_search_yet(self):
        #
        """
        If no search exists, an appropriate message is displayed.
        """
        self.client = Client()
        #
        self.client.login(username='username1', password='mypassword')
        #
        response = self.client.get(reverse('searching:index'))
        #response = self.client.get('/searching/')
        
        #pprint( 'printing response:')
        #pprint( response )
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['search_list'], [])
        self.assertContains(response, "No searches are available.")

    def test_got_search(self):
        #
        """
        If no search exist, an appropriate message is displayed.
        """
        self.client = Client()
        #
        self.client.login(username='username1', password='mypassword')
        #
        sSearch = "Great Widgets"
        oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        
        sSearch = "Phenominal Gadgets"
        oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        sGadgetID = str( oSearch.id )

        response = self.client.get(reverse('searching:index'))
        #response = self.client.get('/searching/')
        
        #print( 'printing response:')
        #pprint( response.context )
        #print( response.context['search_list'])
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['search_list'],
                ['<Search: Phenominal Gadgets>', '<Search: Great Widgets>'],
                ordered=False )
        self.assertContains(response, "Phenominal Gadgets")
        #
        response = self.client.get(
                reverse( 'searching:detail', kwargs={ 'pk': sGadgetID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phenominal Gadgets")
        
        self.client.logout()
        self.client.login(username='username2', password='mypassword')
        
        response = self.client.get(
                reverse( 'searching:detail', kwargs={ 'pk': sGadgetID } ) )

        self.assertEqual(response.status_code, 403) # forbidden
        self.assertEqual(
            getExceptionMessageFromResponse( response ),
            "Permission Denied -- that's not your record!" )

        self.client.logout()
        self.client.login(username='username3', password='mypassword')
        
        response = self.client.get(
                reverse( 'searching:detail', kwargs={ 'pk': sGadgetID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phenominal Gadgets")

        """
        Not logged in, cannot see form, direct to login page.
        """
        self.client.logout()
        response = self.client.get(reverse('searching:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/searching/')



    #def test_get_success_url(self):
        ## Expect: '/users/testuser/', as that is the default username for
        ##   self.make_user()
        #self.assertEqual(
            #self.view.get_success_url(),
            #'/searching/index/'
        #)
    #def test_get_object(self):
        ## Expect: self.user, as that is the request's user object
        #self.assertEqual(
            #self.view.get_object(),
            #self.user
        #)

