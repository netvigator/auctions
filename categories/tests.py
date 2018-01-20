from django.test                import TestCase
from django.test.client         import Client
from django.core.urlresolvers   import reverse, resolve
from django.contrib.auth        import get_user_model

from core.tests                 import getDefaultMarket, BaseUserTestCase
from core.utils                 import getExceptionMessageFromResponse

from .models                    import Category
from core.tests                 import getDefaultMarket

# Create your tests here.


class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
        oCategory = Category(
            cTitle          = "My awesome category",
            iUser           = self.user1 )
        oCategory.save()
            
        self.assertEqual(
            oCategory.get_absolute_url(),
            '/categories/%s/' % oCategory.id
        )

    def test_list_reverse(self):
        """searches:index should reverse to /categories/."""
        self.assertEqual(reverse('categories:index'), '/categories/')


    def test_list_resolve(self):
        """/categories/ should resolve to categories:index."""
        self.assertEqual(resolve('/categories/').view_name, 'categories:index')

    def test_detail_reverse(self):
        """categories:detail should reverse to /categories/<pk>/."""
        self.assertEqual(
            reverse('categories:detail', kwargs={ 'pk': 1 }),
            '/categories/1/'
        )

    def test_edit_reverse(self):
        """categories:edit should reverse to /categories/edit/."""
        self.assertEqual(reverse('categories:edit', kwargs={ 'pk': 1 }),
                         '/categories/1/edit/')

    def test_update_resolve(self):
        """/categories/~update/ should resolve to categories:update."""
        self.assertEqual(
            resolve('/categories/1/edit/').view_name,
            'categories:edit'
        )


class CategoryModelTest(TestCase):

    def test_string_representation(self):
        sCategory = "This category"
        oCategory = Category( cTitle = sCategory )
        self.assertEqual(str(sCategory), oCategory.cTitle)
    
class CategoryViewsTests(TestCase):
    """Category views tests."""
    
    urls = '.urls'
    
    def setUp(self):
        
        getDefaultMarket( self )
        
        oUser = get_user_model()

        self.user1 = oUser.objects.create_user( 'username1', 'email@ymail.com' )
        self.user1.set_password( 'mypassword')
        self.user1.first_name   = 'John'
        self.user1.last_name    = 'Citizen'
        self.user1.save()
        
        # print( 'user1.id:', user1.id )
        
        self.user2 = oUser.objects.create_user( 'username2', 'email@gmail.com' )
        self.user2.set_password( 'mypassword')
        self.user2.first_name   = 'Joe'
        self.user2.last_name    = 'Blow'
        self.user2.save()
        
        
        self.user3 = oUser.objects.create_user( 'username3', 'email@hotmail.com' )
        self.user3.set_password( 'mypassword')
        self.user3.first_name   = 'Oscar'
        self.user3.last_name    = 'Zilch'
        self.user3.is_superuser = True
        self.user3.save()

        
    def test_no_categories_yet(self):
        #
        """
        If no categories exist, an appropriate message is displayed.
        """
        self.client = Client()
        
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
        self.client = Client()
        
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
        
        # getting weird error
        # django.urls.exceptions.NoReverseMatch: 
        # Reverse for 'edit' with keyword arguments '{'pk': ''}' not found. 
        # 1 pattern(s) tried: ['brands/(?P<pk>[0-9]+)/edit/$']
        
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



