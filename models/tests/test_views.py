from django.core.urlresolvers   import reverse

from core.utils_test            import BaseUserTestCase

from core.utils                 import getExceptionMessageFromResponse

from categories.models          import Category

from ..models                   import Model

from ..views                    import ModelCreateView
# Create your tests here.



class ModelViewsTests(BaseUserTestCase):
    """Model views tests."""
    
    def setUp(self):
        #
        super( ModelViewsTests, self ).setUp()
        #
        sCategory = "Widgets"
        oCategory = Category( cTitle= sCategory, iUser = self.user1 )
        oCategory.save()
        #
        self.oCategory = oCategory
        #

    def test_no_models_yet(self):
        #
        """
        If no models exist, an appropriate message is displayed.
        """
        self.client.login(username='username1', password='mypassword')
        #
        response = self.client.get(reverse('models:index'))
        #response = self.client.get('/models/')
        
        #pprint( 'printing response:')
        #pprint( response )
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['model_list'], [])
        self.assertContains(response, "No models are available.")
    
    
        
    def test_got_models(self):
        #
        """
        If models exist, an appropriate message is displayed.
        """
        #
        self.client.login(username='username1', password='mypassword')
        #
        
        oModel  = Model(
                cTitle      = "Crest",
                iUser       = self.user1,
                iCategory   = self.oCategory )
        oModel.save()
        
        oModel  = Model(
                cTitle = "Colgate",
                iUser       = self.user1,
                iCategory   = self.oCategory )
        oModel.save()
        #
        iLeverID= oModel.id

        response = self.client.get(reverse('models:index'))
        #response = self.client.get('/models/')
        
        #pprint( 'printing response:')
        #pprint( response )
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['model_list'],
                ['<Model: Colgate>', '<Model: Crest>'] )
        self.assertContains(response, "Colgate")
        #
        response = self.client.get(
                reverse( 'models:detail', kwargs={ 'pk': iLeverID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Colgate")
        
        self.client.logout()
        self.client.login(username='username2', password='mypassword')
        
        response = self.client.get(
                reverse( 'models:detail', kwargs={ 'pk': iLeverID } ) )

        self.assertEqual(response.status_code, 403) # forbidden
        self.assertEqual(
            getExceptionMessageFromResponse( response ),
            "Permission Denied -- that's not your record!" )

        self.client.logout()
        self.client.login(username='username3', password='mypassword')
        
        response = self.client.get(
                reverse( 'models:detail', kwargs={ 'pk': iLeverID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Colgate")

        """
        Not logged in, cannot see form, direct to login page.
        """
        self.client.logout()
        response = self.client.get(reverse('models:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/models/')




class ModelViewsHitButtons(BaseUserTestCase):
    """
    Test Save and Cancel
    """
    def setUp(self):
        #
        super( ModelViewsHitButtons, self ).setUp()
        #
        sCategory = "Widgets"
        oCategory = Category( cTitle= sCategory, iUser = self.user1 )
        oCategory.save()
        #
        self.oCategory = oCategory
        #
        self.client.login(username ='username1', password='mypassword')



    def test_get(self):
        """
        Test GET requests
        """
        request = self.factory.get(reverse('models:add'))
        request.user = self.user1
        #
        response = ModelCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        #print( 'response.context_data has form and view, view keys:' )
        #for k in response.context_data['view'].__dict__:
            #print( k )
        #self.assertEqual(response.context_data['iUser'], self.user1)
        self.assertEqual(response.context_data['view'].__dict__['request'], request)


    # @patch('models.models.Model.save', MagicMock(name="save"))
    def test_add_post(self):
        """
        Test post requests
        """
        data = dict(
            cTitle      = "Permium Number One",
            iCategory   = self.oCategory,
            iUser       = self.user1 )
        # Create the request
        response = self.client.post( reverse('models:add'), data )
        # import pdb; pdb.set_trace()
        self.assertEqual( response.status_code, 200 )
        #oModel = Model.objects.get( cTitle = "Great Widget" )
        #self.assertEqual( oModel, self.models )

        #request = self.factory.get(reverse('models:add'))
        #request.user = self.user1

        #response = self.client.post( request, data )

        #print( 'response.status_code:', response.status_code )


    def test_add_hit_cancel(self):
        #
        """
        Hit cancel when adding
        """
        data = dict(
            cTitle      = "Permium Number One",
            iUser       = self.user1,
            iCategory   = self.oCategory,
            Cancel      = True )
        # Create the request
        response = self.client.post( reverse('models:add'), data )
        #print( 'response.status_code:', response.status_code )
        #print( 'response.__dict__:' )
        #pprint( response.__dict__ )
        self.assertEqual( response.status_code, 200 )
        # self.assertRedirects( response, reverse( 'models:index' ) )

    def test_search_create_view(self):
        #
        request = self.factory.get(reverse('models:add'))
        request.user = self.user1
        #request.POST._mutable = True
        #request.POST['cancel'] = True
        #
        response = ModelCreateView.as_view()(request)
        #
        # print( 'type( request.POST ):', type( request.POST ) )
        #
        self.assertEqual(response.status_code, 200 )
        #print( 'response.template_name:' )
        #print( response.template_name ) ['models/add.html']
        #
    #

    # @patch('models.models.Model.save', MagicMock(name="save"))
    def test_edit_post(self):
        """
        Test post requests
        """
        sModel = "Permium Number One"
        oModel = Model( cTitle    = sModel,
                        iUser     = self.user1,
                        iCategory = self.oCategory )
        oModel.save()
        #
        data = dict(
            cTitle      = "Permium Number Two",
            iUser       = self.user1 )
        # Create the request
        response = self.client.post(
                reverse('models:edit', kwargs={'pk': oModel.id} ), data )
        # import pdb; pdb.set_trace()
        self.assertEqual( response.status_code, 200 )


    def test_edit_hit_cancel(self):
        #
        """
        Hit cancel when adding
        """
        sModel = "Permium Number One"
        oModel = Model( cTitle    = sModel,
                        iUser     = self.user1,
                        iCategory = self.oCategory )
        oModel.save()
        #
        data = dict(
            cTitle      = "Permium Number Two",
            iUser       = self.user1,
            Cancel      = True )
        # Create the request
        response = self.client.post(
                reverse('models:edit', kwargs={'pk': oModel.id} ), data )
        #print( 'response.status_code:', response.status_code )
        #print( 'response.__dict__:' )
        #pprint( response.__dict__ )
        self.assertEqual( response.status_code, 200 )
        # self.assertRedirects( response, reverse( 'models:index' ) )

