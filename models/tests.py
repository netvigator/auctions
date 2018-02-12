from django.contrib.auth        import get_user_model
from django.core.urlresolvers   import reverse, resolve
from django.test                import TestCase
from django.test.client         import Client

from core.tests                 import ( BaseUserTestCase, getDefaultMarket,
                                         getUrlQueryStringOff, queryGotUTC )

from core.utils                 import getExceptionMessageFromResponse

from categories.models          import Category

from .forms                     import ModelForm
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
        #
        oModel.save()
        #
        tParts = getUrlQueryStringOff( oModel.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/models/%s/' % oModel.id )
        #
        self.assertTrue( queryGotUTC( tParts[1] ) )
        #
        self.assertFalse( queryGotUTC( tParts[0] ) )

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




class TestFormValidation(BaseUserTestCase):
    
    ''' Model Form Tests '''
    
    def setUp(self):
        #
        getDefaultMarket( self )
        #
        oUser = get_user_model()
        #
        self.user1 = oUser.objects.create_user( 'username1', 'email@ymail.com' )
        self.user1.set_password( 'mypassword')
        self.user1.first_name   = 'John'
        self.user1.last_name    = 'Citizen'
        self.user1.save()
        #
        self.client = Client()
        self.client.login(username ='username1', password='mypassword')
        #
        self.oCategory = Category(
            cTitle = "Widgets",
            iStars  = 5,
            iUser = self.user1 )
        self.oCategory.save()
        self.CategoryID = self.oCategory.id
        
        # print( 'category ID:', self.CategoryID )

    def test_Title_got_outside_parens(self):
        #
        form_data = dict(
            cTitle      = '(LS3-5A)',
            iStars      = 5,
            iCategory   = self.CategoryID,
            iUser       = self.user1
            )
        
        form = ModelForm(data=form_data)
        self.assertFalse(form.is_valid())
        #
        '''
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors above!' )
        '''
        #
        form_data['cTitle'] = 'LS3-5A'
        #
        form = ModelForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        '''
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors at bottom!' )
        '''

