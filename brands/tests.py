from django.test        import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.urls        import reverse
from django.contrib.auth import get_user_model

from core.utils         import getExceptionMessageFromResponse

from pprint import pprint
from six    import print_ as print3


# Create your tests here.

from .models        import Brand
from brands.views   import IndexView
from core.utils     import oUserOne


class ModelModelTest(TestCase):

    def test_string_representation(self):
        sBrand = "My brand name"
        oBrand = Brand(cTitle= sBrand )
        self.assertEqual(str(sBrand), oBrand.cTitle)


def createBrand( sName, oUser ):
    #
    oBrand = Brand(cTitle = sName, iUser = oUser )
    oBrand.save()
    #
    return oBrand.id

    
class BrandViewsTests(TestCase):
    """Brand views tests."""
    
    def setUp(self):
        
        oUser = get_user_model()

        self.user1 = oUser.objects.create_user( 'username1', 'email@ymail.com' )
        self.user1.set_password( 'mypassword')
        self.user1.first_name = 'John'
        self.user1.last_name = 'Citizen'
        self.user1.save()
        
        # print3( 'user1.id:', user1.id )
        
        self.user2 = oUser.objects.create_user( 'username2', 'email@gmail.com' )
        self.user2.set_password( 'mypassword')
        self.user2.first_name = 'Joe'
        self.user2.last_name = 'Blow'
        self.user2.save()
        
        
        '''
        sBrand = "Proctor & Gamble"
        oBrand = Brand(cTitle= sBrand, iUser = user1 )
        
        sBrand = "Lever Brothers"
        oBrand = Brand(cTitle= sBrand, iUser = user2 )
        '''
        
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
        If no brands exist, an appropriate message is displayed.
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

    


'''
class BrandListViewTests(TestCase):
    """Brand list view tests."""

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
