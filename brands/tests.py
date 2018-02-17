from django.contrib.auth        import get_user_model
from django.core.urlresolvers   import reverse, resolve
from django.test                import TestCase
from django.http.request        import HttpRequest
from django.urls                import reverse

from core.tests                 import ( getDefaultMarket, BaseUserTestCase,
                                         getUrlQueryStringOff, queryGotUTC )

from core.utils                 import getExceptionMessageFromResponse

# Create your tests here.

from .forms                     import BrandForm
from .models                    import Brand

from pprint                     import pprint


class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
        oBrand = Brand(
            cTitle          = "My premium brand",
            iUser           = self.user1,
            id              = 1 )
        oBrand.save()
        #
        tParts = getUrlQueryStringOff( oBrand.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/brands/%s/' % oBrand.id )
        #
        self.assertTrue( queryGotUTC( tParts[1] ) )
        #
        self.assertFalse( queryGotUTC( tParts[0] ) )
        

    def test_list_reverse(self):
        """searches:index should reverse to /brands/."""
        self.assertEqual(reverse('brands:index'), '/brands/')


    def test_list_resolve(self):
        """/brands/ should resolve to brands:index."""
        self.assertEqual(resolve('/brands/').view_name, 'brands:index')

    def test_detail_reverse(self):
        """brands:detail should reverse to /brands/<pk>/."""
        self.assertEqual(
            reverse('brands:detail', kwargs={ 'pk': 1 }),
            '/brands/1/'
        )

    def test_edit_reverse(self):
        """brands:edit should reverse to /brands/edit/."""
        self.assertEqual(reverse('brands:edit', kwargs={ 'pk': 1 }),
                         '/brands/1/edit/')

    def test_update_resolve(self):
        """/brands/~update/ should resolve to brands:update."""
        self.assertEqual(
            resolve('/brands/1/edit/').view_name,
            'brands:edit'
        )



class ModelModelTest(TestCase):

    def test_string_representation(self):
        sBrand = "My brand name"
        oBrand = Brand(cTitle= sBrand )
        self.assertEqual(str(oBrand), oBrand.cTitle)


class BrandViewsTests(BaseUserTestCase):
    """Brand views tests."""
    
        
    def test_no_brands_yet(self):
        #
        """
        If no brands exist, an appropriate message is displayed.
        """
        self.client.login(username='username1', password='mypassword')
        #
        response = self.client.get(reverse('brands:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['brand_list'], [])
        self.assertContains(response, "No brands are available.")
    
    
        
    def test_got_brands(self):
        #
        """
        If brands exist, an appropriate message is displayed.
        """
        
        self.client.login(username='username1', password='mypassword')
        #
        sBrand = "Proctor & Gamble"
        oBrand = Brand( cTitle= sBrand, iUser = self.user1 )
        oBrand.save()
        
        sBrand = "Cadillac"
        oBrand = Brand( cTitle= sBrand, iUser = self.user1 )
        oBrand.save()
        sLeverID = str( oBrand.id )

        response = self.client.get(reverse('brands:index'))
        #response = self.client.get('/brands/')
        
        #pprint( 'printing response:')
        #pprint( response )
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['brand_list'],
                ['<Brand: Cadillac>', '<Brand: Proctor & Gamble>'] )
        self.assertContains(response, "Cadillac")
        #
        response = self.client.get(
                reverse( 'brands:detail', kwargs={ 'pk': sLeverID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cadillac")
        
        self.client.logout()
        self.client.login(username='username2', password='mypassword')
        
        response = self.client.get(
                reverse( 'brands:detail', kwargs={ 'pk': sLeverID } ) )

        self.assertEqual(response.status_code, 403) # forbidden
        self.assertEqual(
            getExceptionMessageFromResponse( response ),
            "Permission Denied -- that's not your record!" )

        self.client.logout()
        self.client.login(username='username3', password='mypassword')
        
        response = self.client.get(
                reverse( 'brands:detail', kwargs={ 'pk': sLeverID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cadillac")

        """
        Not logged in, cannot see form, direct to login page.
        """
        self.client.logout()
        response = self.client.get(reverse('brands:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/brands/')
        #pprint( 'printing response:')
        #pprint( response )
        


class TestFormValidation(BaseUserTestCase):
    
    ''' Brand Form Tests '''
    
    def setUp(self):
        #
        super( TestFormValidation, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')
        #
        oBrand = Brand(
            cTitle = "Cadillac", cLookFor = "Caddy", iUser = self.user1 )
        oBrand.save()

    def test_Title_got_outside_parens(self):
        #
        form_data = dict(
            cTitle      = '(Chevrolet)',
            iStars      = 5,
            iUser       = self.user1.id
            )
        #
        form = BrandForm(data=form_data)
        form.request = self.request
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
        form_data['cTitle'] = 'Chevrolet'
        #
        form = BrandForm(data=form_data)
        form.request = self.request
        self.assertTrue(form.is_valid())
        
        ''' test save '''
        form.instance.iUser = self.user1
        form.save()
        oBrand = Brand.objects.get( cTitle = 'Chevrolet' )
        self.assertEqual(
            reverse('brands:detail', kwargs={ 'pk': oBrand.id } ),
            '/brands/%s/' % oBrand.id )
        

    def test_Title_not_there_already(self):
        #
        form_data = dict(
            cTitle      = 'Cadillac',
            iStars      = 5,
            iUser       = self.user1.id
            )
        #
        form = BrandForm(data=form_data)
        form.request = self.request
        self.assertFalse(form.is_valid())
        #
        form_data['cTitle'] = 'Caddy'
        #
        form = BrandForm(data=form_data)
        form.request = self.request
        self.assertFalse(form.is_valid())
        #
        '''
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors at bottom!' )
        '''

