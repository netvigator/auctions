from django.test                import TestCase
from django.contrib.auth        import get_user_model
from django.core.urlresolvers   import reverse, resolve
from django.http.request        import HttpRequest

from core.tests                 import ( getDefaultMarket, BaseUserTestCase,
                                         getUrlQueryStringOff, queryGotUTC )

from core.utils                 import getExceptionMessageFromResponse

from .models                    import Category
from .forms                     import CategoryForm


# Create your tests here.


class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
        oCategory = Category(
            cTitle          = "My awesome category",
            iUser           = self.user1 )
        #
        oCategory.save()
        #
        tParts = getUrlQueryStringOff( oCategory.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/categories/%s/' % oCategory.id )
        #
        self.assertTrue( queryGotUTC( tParts[1] ) )
        #
        self.assertFalse( queryGotUTC( tParts[0] ) )

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


class TestFormValidation(BaseUserTestCase):
    
    ''' Category Form Tests '''
    
    def setUp(self):
        #
        super( TestFormValidation, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')
        #
        oCategory = Category(
            cTitle = "Gadgets", cLookFor = "thingamajig", iUser = self.user1 )
        oCategory.save()

    def test_Title_got_outside_parens(self):
        #
        form_data = dict(
            cTitle      = '(Widgets)',
            iStars      = 5,
            iUser       = self.user1
            )
        #
        form = CategoryForm(data=form_data)
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
        form_data['cTitle'] = 'Widgets'
        #
        form = CategoryForm(data=form_data)
        form.request = self.request
        self.assertTrue(form.is_valid())

        ''' test save '''
        form.instance.iUser = self.user1
        form.save()
        oCategory = Category.objects.get( cTitle = 'Widgets' )
        self.assertEqual(
            reverse('categories:detail', kwargs={ 'pk': oCategory.id } ),
            '/categories/%s/' % oCategory.id )

    def test_Title_not_there_already(self):
        #
        form_data = dict(
            cTitle      = 'Gadgets',
            iStars      = 5,
            iUser       = self.user1
            )
        #
        form = CategoryForm(data=form_data)
        form.request = self.request
        self.assertFalse(form.is_valid())
        #
        form_data['cTitle'] = 'ThingaMaJig'
        #
        form = CategoryForm(data=form_data)
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

