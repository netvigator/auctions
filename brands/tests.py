from django.contrib.auth        import get_user_model
from django.core.urlresolvers   import reverse, resolve
from django.test                import TestCase
from django.test.client         import Client
from django.test.client         import RequestFactory
from django.urls                import reverse

from core.tests                 import getDefaultMarket, BaseUserTestCase
from core.utils                 import getExceptionMessageFromResponse

from pprint import pprint


# Create your tests here.

from .models        import Brand



class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
        oBrand = Brand(
            cTitle          = "My premium brand",
            iUser           = self.user1,
            id              = 1 )
        oBrand.save()
            
        self.assertEqual(
            oBrand.get_absolute_url(),
            '/brands/1/'
        )

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
        self.client = Client()
        
        self.client.login(username='username1', password='mypassword')
        #
        response = self.client.get(reverse('brands:index'))
        #response = self.client.get('/brands/')
        
        #pprint( 'printing response:')
        #pprint( response )
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['brand_list'], [])
        self.assertContains(response, "No brands are available.")
    
    
        
    def test_got_brands(self):
        #
        """
        If brands exist, an appropriate message is displayed.
        """
        self.client = Client()
        
        self.client.login(username='username1', password='mypassword')
        #
        sBrand = "Proctor & Gamble"
        oBrand = Brand( cTitle= sBrand, iUser = self.user1 )
        oBrand.save()
        
        sBrand = "Lever Brothers"
        oBrand = Brand( cTitle= sBrand, iUser = self.user1 )
        oBrand.save()
        sLeverID = str( oBrand.id )

        response = self.client.get(reverse('brands:index'))
        #response = self.client.get('/brands/')
        
        #pprint( 'printing response:')
        #pprint( response )
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['brand_list'],
                ['<Brand: Lever Brothers>', '<Brand: Proctor & Gamble>'] )
        self.assertContains(response, "Lever Brothers")
        #
        response = self.client.get(
                reverse( 'brands:detail', kwargs={ 'pk': sLeverID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lever Brothers")
        
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
        self.assertContains(response, "Lever Brothers")




'''
from brands.views   import IndexView
from core.user_one  import oUserOne

class BrandListViewTests(TestCase):
    """Brand list view tests."""

    def setUp(self):
        getDefaultMarket( self )
        
    def test_brands_in_the_context(self):

        client = Client()
        response = client.get('/')

        self.assertEquals(list(response.context['index']), [])

        Brand.objects.create(cTitle='Chevrolet', iUser=oUserOne )
        response = client.get('/')
        self.assertEquals(response.context['index'].count(), 1)

    def test_brands_in_the_context_request_factory(self):

        factory = RequestFactory()
        request = factory.get('/')

        response = IndexView.as_view()(request)

        self.assertEquals(list(response.context_data['index']), [])

        Brand.objects.create(cTitle='Chevrolet', iUser=oUserOne )
        response = IndexView.as_view()(request)
        self.assertEquals(response.context_data['index'].count(), 1)
'''
