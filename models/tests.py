from django.core.urlresolvers   import reverse, resolve
from django.test                import TestCase
from django.test.client         import Client

from core.tests                 import getDefaultMarket, BaseUserTestCase
from core.utils                 import getExceptionMessageFromResponse

from categories.models          import Category

from .models                    import Model

# Create your tests here.

'''
no views implemented yet
class ModelsViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/models/')
        self.assertEqual(resp.status_code, 200)
'''


class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
        
        oModel = Model(
            cTitle          = "My stellar model",
            iUser           = self.user1,
            iCategory       = self.oCategory )
        oModel.save()
        
        self.assertEqual(
            oModel.get_absolute_url(),
            '/models/%s/' % oModel.id
        )

    def test_list_reverse(self):
        """searches:index should reverse to /models/."""
        self.assertEqual(reverse('models:index'), '/models/')


    def test_list_resolve(self):
        """/models/ should resolve to models:index."""
        self.assertEqual(resolve('/models/').view_name, 'models:index')

    def test_detail_reverse(self):
        """models:detail should reverse to /models/<pk>/."""
        self.assertEqual(
            reverse('models:detail', kwargs={ 'pk': 1 }),
            '/models/1/'
        )

    def test_edit_reverse(self):
        """models:edit should reverse to /models/edit/."""
        self.assertEqual(reverse('models:edit', kwargs={ 'pk': 1 }),
                         '/models/1/edit/')

    def test_update_resolve(self):
        """/models/~update/ should resolve to models:update."""
        self.assertEqual(
            resolve('/models/1/edit/').view_name,
            'models:edit'
        )


class ModelModelTest(TestCase):

    def test_string_representation(self):
        sModel = "My model name/number"
        oModel = Model(cTitle= sModel )
        self.assertEqual(str(sModel), oModel.cTitle)




class ModelViewsTests(BaseUserTestCase):
    """Model views tests."""
    
        
    def test_no_models_yet(self):
        #
        """
        If no models exist, an appropriate message is displayed.
        """
        self.client = Client()
        
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
        self.client = Client()
        
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



