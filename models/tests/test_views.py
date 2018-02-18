from django.core.urlresolvers   import reverse

from core.test_utils            import BaseUserTestCase

from core.utils                 import getExceptionMessageFromResponse

from categories.models          import Category

from ..models                   import Model

# Create your tests here.



class ModelViewsTests(BaseUserTestCase):
    """Model views tests."""
    
    def setUp(self):
        #
        super( ModelViewsTests, self ).setUp()
        #
        self.oCategory = Category(
            cTitle          = "My awesome category",
            iUser           = self.user1 )
        self.oCategory.save()
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
        
        oModel      = Model(
            cTitle = "Crest", iUser = self.user1, iCategory = self.oCategory )
        oModel.save()
        
        oModel      = Model(
            cTitle = "Colgate", iUser = self.user1, iCategory = self.oCategory )
        oModel.save()
        iLeverID    = oModel.id

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

