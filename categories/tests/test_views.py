from django.core.urlresolvers   import reverse

from core.utils_testing         import BaseUserTestCase

from core.utils                 import getExceptionMessageFromResponse

from ..models                   import Category



class CategoryViewsTests(BaseUserTestCase):
    """Category views tests."""
    
    urls = '.urls'
    
    def test_no_categories_yet(self):
        #
        """
        If no categories exist, an appropriate message is displayed.
        """
        self.client.login(username='username1', password='mypassword')
        #
        response = self.client.get(reverse('categories:index'))
        #response = self.client.get('/categories/')
        
        #pprint( 'printing response:')
        #pprint( response )
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['category_list'], [])
        self.assertContains(response, "No categories are available.")
    
        
    def test_got_categories(self):
        #
        """
        If categories exist, an appropriate message is displayed.
        """
        self.client.login(username ='username1', password='mypassword')
        #
        oCategory = Category( cTitle = "Widgets", iUser = self.user1 )
        oCategory.save()

        oCategory = Category( cTitle = "Gadgets", iUser = self.user1 )
        oCategory.save()
        iGadgetID = oCategory.id

        response = self.client.get(reverse('categories:index'))
        #response = self.client.get('/categories/')
        
        #pprint( 'printing response:')
        #pprint( response )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['category_list'],
                ['<Category: Widgets>', '<Category: Gadgets>'],
                ordered=False )
        self.assertContains(response, "Gadgets")
        
        #print( 'iGadgetID:', iGadgetID )
        
        response = self.client.get(
                reverse( 'categories:detail', kwargs={ 'pk': iGadgetID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gadgets")
        
        self.client.logout()
        self.client.login(username='username2', password='mypassword')
        
        response = self.client.get(
                reverse( 'categories:detail', kwargs={ 'pk': iGadgetID } ) )

        self.assertEqual(response.status_code, 403) # forbidden
        self.assertEqual(
            getExceptionMessageFromResponse( response ),
            "Permission Denied -- that's not your record!" )

        self.client.logout()
        self.client.login(username='username3', password='mypassword')
        
        response = self.client.get(
                reverse( 'categories:detail', kwargs={ 'pk': iGadgetID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gadgets")

        """
        Not logged in, cannot see form, direct to login page.
        """
        self.client.logout()
        response = self.client.get(reverse('categories:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/categories/')

