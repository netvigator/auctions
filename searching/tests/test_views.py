import logging

from django.core.urlresolvers   import reverse

from core.utils_test            import BaseUserWebTestCase, setup_view_for_tests
from core.utils                 import getExceptionMessageFromResponse

from ..forms                    import CreateSearchForm, UpdateSearchForm
from ..models                   import Search

from ..views                    import ( SearchCreateView, SearchIndexView,
                                         SearchDetailView, SearchDeleteView,
                                         SearchUpdateView )


#from pprint import pprint

# Create your tests here.

class SearchViewsHitButtons( BaseUserWebTestCase ):
    """
    Test Save and Cancel
    """
    def setUp(self):
        #
        super( SearchViewsHitButtons, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')



    def test_get(self):
        """
        Test GET requests
        """
        request = self.factory.get(reverse('searching:add'))
        request.user = self.user1
        #
        response = SearchCreateView.as_view()(request)
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
        data = dict(
            cTitle      = "Great Widget",
            cKeyWords   = "Blah bleh blih",
            iUser       = self.user1 )
        # Create the request
        response = self.client.post( reverse('searching:add'), data )
        # import pdb; pdb.set_trace()
        self.assertEqual( response.status_code, 200 )
        #oSearch = Search.objects.get( cTitle = "Great Widget" )
        #self.assertEqual( oSearch, self.searching )

        #request = self.factory.get(reverse('searching:add'))
        #request.user = self.user1

        #response = self.client.post( request, data )

        #print( 'response.status_code:', response.status_code )


    def test_add_hit_cancel(self):
        #
        """
        Hit cancel when adding
        """
        data = dict(
            cTitle      = "Great Widget",
            cKeyWords   = "Blah bleh blih",
            iUser       = self.user1,
            Cancel      = True )
        # Create the request
        response = self.client.post( reverse('searching:add'), data )
        #print( 'response.status_code:', response.status_code )
        #print( 'response.__dict__:' )
        #pprint( response.__dict__ )
        self.assertEqual( response.status_code, 200 )
        # self.assertRedirects( response, reverse( 'searching:index' ) )

    def test_search_create_view(self):
        #
        request = self.factory.get(reverse('searching:add'))
        request.user = self.user1
        #request.POST._mutable = True
        #request.POST['cancel'] = True
        #
        response = SearchCreateView.as_view()(request)
        #
        # print( 'type( request.POST ):', type( request.POST ) )
        #
        self.assertEqual(response.status_code, 200 )
        #print( 'response.template_name:' )
        #print( response.template_name ) ['searching/add.html']
        #
    #

class SearchViewsTests( BaseUserWebTestCase ):

    def test_no_search_yet(self):
        #
        """
        If no search exists, an appropriate message is displayed.
        """
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
        logging.disable(logging.CRITICAL)

        #
        self.client.login(username='username1', password='mypassword')
        #
        sSearch = "Great Widget"
        oSearch = Search( cTitle = sSearch, iUser = self.user1 )
        oSearch.save()

        sSearch = "Phenominal Gadget"
        oSearch = Search( cTitle = sSearch, iUser = self.user1 )
        oSearch.save()
        sGadgetID = str( oSearch.id )

        response = self.client.get(reverse('searching:index'))
        #response = self.client.get('/searching/')

        #print( 'printing response:')
        #pprint( response.context )
        #print( response.context['search_list'])

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['search_list'],
                ['<Search: Phenominal Gadget>', '<Search: Great Widget>'],
                ordered=False )
        self.assertContains(response, "Phenominal Gadget")
        #
        response = self.client.get(
                reverse( 'searching:detail', kwargs={ 'pk': sGadgetID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phenominal Gadget")

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
        self.assertContains(response, "Phenominal Gadget")

        """
        Not logged in, cannot see form, direct to login page.
        """
        self.client.logout()
        response = self.client.get(reverse('searching:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/searching/')

        logging.disable(logging.NOTSET)



class SearchUpdateViewTests( BaseUserWebTestCase ):

    ''' test SearchUpdateView View '''

    def setUp(self):

        # call BaseUserWebTestCase.setUp()
        super(SearchUpdateViewTests, self).setUp()
        #
        sSearch = "Great Widget"
        oSearch = Search( cTitle = sSearch, iUser = self.user1 )
        oSearch.save()
        #
        self.form = UpdateSearchForm( instance = oSearch )
        #
        self.request = self.factory.get( reverse( 'searching:index' ) )
        #
        self.request.user = self.user1
        #
        self.view = setup_view_for_tests( SearchUpdateView(), self.request )
        #
        self.client.login(username='username1', password='mypassword')
        #

    #def test_form_dot_save_called_with_user(self):
        #self.view.form_valid(self.form)
        #self.form.save.assert_called_once_with(iUser=self.request.user)


    def test_update_view_context(self):
        #
        self.assertEqual( self.view.template_name, 'searching/edit.html' )
        #
        self.assertEqual( self.form.which, "Update" )
        #
        self.assertEqual( self.view.model, Search )



class SearchCreateViewTests( BaseUserWebTestCase ):

    ''' test SearchUpdateView View '''

    def setUp(self):
        #
        super(SearchCreateViewTests, self).setUp()
        #
        data = dict(
            cTitle      = "Great Widget",
            cKeyWords   = "Blah bleh blih",
            iUser       = self.user1 )
        #
        self.form = CreateSearchForm( data = data )
        #
        self.request = self.factory.get( reverse( 'searching:add' ) )
        #
        self.request.user = self.user1
        #
        self.view = setup_view_for_tests( SearchCreateView(), self.request )
        #
        self.client.login(username='username1', password='mypassword')


    def test_create_view_cancelled(self):
        #
        self.assertEqual( self.view.template_name, 'searching/add.html' )
        #
        self.assertEqual( self.form.which, "Create" )
        #
        self.assertEqual( self.view.model, Search )
        #
        self.request.POST._mutable = True
        self.request.POST['cancel'] = True
        ##
        response = self.view.post( self.request ) # , Cancel = True
        response.client = self.client
        #
        self.assertEqual(response.status_code, 302 )
        self.assertEqual(response.url, '/searching/')
        #
        #print( 'response:' )
        #pprint( response )



    def test_create_view_not_cancelled(self):
        #
        self.assertEqual( self.view.template_name, 'searching/add.html' )
        #
        self.assertEqual( self.form.which, "Create" )
        #
        self.assertEqual( self.view.model, Search )
        #
        response = self.view.post( self.request ) # , Cancel = True
        #
        self.assertEqual(response.status_code, 200 )

