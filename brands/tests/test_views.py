from django.core.urlresolvers   import reverse

from core.utils_testing         import BaseUserTestCase

from core.utils                 import getExceptionMessageFromResponse

# Create your tests here.

from ..models                   import Brand




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
        
