from django.core.urlresolvers   import reverse

from core.utils_testing         import BaseUserTestCase

from core.utils                 import getExceptionMessageFromResponse

# Create your tests here.

from ..models                   import Brand
from ..views                    import BrandCreateView



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
        


class BrandViewsHitButtons(BaseUserTestCase):
    """
    Test Save and Cancel
    """
    def setUp(self):
        #
        super( BrandViewsHitButtons, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')



    def test_get(self):
        """
        Test GET requests
        """
        request = self.factory.get(reverse('brands:add'))
        request.user = self.user1
        #
        response = BrandCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        #print( 'response.context_data has form and view, view keys:' )
        #for k in response.context_data['view'].__dict__:
            #print( k )
        #self.assertEqual(response.context_data['iUser'], self.user1)
        self.assertEqual(response.context_data['view'].__dict__['request'], request)


    # @patch('brands.models.Brand.save', MagicMock(name="save"))
    def test_add_post(self):
        """
        Test post requests
        """
        data = dict(
            cTitle      = "Proctor & Gamble",
            iUser       = self.user1 )
        # Create the request
        response = self.client.post( reverse('brands:add'), data )
        # import pdb; pdb.set_trace()
        self.assertEqual( response.status_code, 200 )
        #oBrand = Brand.objects.get( cTitle = "Great Widget" )
        #self.assertEqual( oBrand, self.brands )

        #request = self.factory.get(reverse('brands:add'))
        #request.user = self.user1
        
        #response = self.client.post( request, data )
        
        #print( 'response.status_code:', response.status_code )

        
    def test_add_hit_cancel(self):
        #
        """
        Hit cancel when adding
        """
        data = dict(
            cTitle      = "Proctor & Gamble",
            iUser       = self.user1,
            Cancel      = True )
        # Create the request
        response = self.client.post( reverse('brands:add'), data )
        #print( 'response.status_code:', response.status_code )
        #print( 'response.__dict__:' )
        #pprint( response.__dict__ )
        self.assertEqual( response.status_code, 200 )
        # self.assertRedirects( response, reverse( 'brands:index' ) )
        
    def test_search_create_view(self):
        #
        request = self.factory.get(reverse('brands:add'))
        request.user = self.user1
        #request.POST._mutable = True
        #request.POST['cancel'] = True
        #
        response = BrandCreateView.as_view()(request)
        #
        # print( 'type( request.POST ):', type( request.POST ) )
        #
        self.assertEqual(response.status_code, 200 )
        #print( 'response.template_name:' )
        #print( response.template_name ) ['brands/add.html']
        #
    #

    # @patch('brands.models.Brand.save', MagicMock(name="save"))
    def test_edit_post(self):
        """
        Test post requests
        """
        sBrand = "Proctor & Gamble"
        oBrand = Brand( cTitle= sBrand, iUser = self.user1 )
        oBrand.save()
        #
        data = dict(
            cTitle      = "Colgate-Palmolive",
            iUser       = self.user1 )
        # Create the request
        response = self.client.post(
                reverse('brands:edit', kwargs={'pk': oBrand.id} ), data )
        # import pdb; pdb.set_trace()
        self.assertEqual( response.status_code, 200 )


    def test_edit_hit_cancel(self):
        #
        """
        Hit cancel when adding
        """
        sBrand = "Proctor & Gamble"
        oBrand = Brand( cTitle= sBrand, iUser = self.user1 )
        oBrand.save()
        #
        data = dict(
            cTitle      = "Colgate-Palmolive",
            iUser       = self.user1,
            Cancel      = True )
        # Create the request
        response = self.client.post(
                reverse('brands:edit', kwargs={'pk': oBrand.id} ), data )
        #print( 'response.status_code:', response.status_code )
        #print( 'response.__dict__:' )
        #pprint( response.__dict__ )
        self.assertEqual( response.status_code, 200 )
        # self.assertRedirects( response, reverse( 'brands:index' ) )

