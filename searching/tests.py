from django.test                import TestCase, RequestFactory
from django.contrib.auth        import get_user_model
from django.core.urlresolvers   import reverse, resolve

from .forms                     import AddOrUpdateForm
from .models                    import Search
from .views                     import (
        SearchCreate, IndexView, SearchDetail, SearchDelete, SearchUpdate )


from core.tests                 import getDefaultMarket
from markets.models             import Market
from ebaycategories.models      import EbayCategory

# Create your tests here.

class BaseUserTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        
        getDefaultMarket( self )

        oUser = get_user_model()

        self.user1 = oUser.objects.create_user( 'username1', 'email@ymail.com' )
        self.user1.set_password( 'mypassword')
        self.user1.first_name   = 'John'
        self.user1.last_name    = 'Citizen'
        self.user1.save()
        
        if (  ( not isinstance( self.market, Market ) ) or
              ( not Market.objects.get( pk = 1 ) ) ):
            self.market = Market(
                cMarket     = 'EBAY-US',
                cCountry    = 'US',
                iEbaySiteID = 0,
                cLanguage   = 'en-US',
                iCategoryVer= 1,
                cCurrencyDef= 'USD' )
            self.market.save()
        
        self.ebc = EbayCategory(
            iCategoryID = 10,
            name        = 'hot products',
            iLevel      = 1,
            iParentID   = 1,
            iTreeVersion= 1,
            iMarket     = self.market,
            bLeafCategory = False )
        self.ebc.save()


class TestSearchCreateView(BaseUserTestCase):
    
    def setUp(self):

        # call BaseUserTestCase.setUp()
        super(TestSearchCreateView, self).setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = SearchCreate()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user1
        # Attach the request to the view
        self.view.request = request

'''
    def test_get_success_url(self):
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            self.view.get_success_url(),
            '/searching/index/'
        )
    def test_get_object(self):
        # Expect: self.user, as that is the request's user object
        self.assertEqual(
            self.view.get_object(),
            self.user
        )

'''
class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
        oSearch = Search(
            cTitle          = "My clever search",
            cKeyWords       = "Blah bleh blih",
            cPriority       = "A",
            iUser           = self.user1,
            id              = 1 )
        oSearch.save()
            
        self.assertEqual(
            oSearch.get_absolute_url(),
            '/searching/1/'
        )

    def test_list_reverse(self):
        """searches:index should reverse to /searching/."""
        self.assertEqual(reverse('searching:index'), '/searching/')


    def test_list_resolve(self):
        """/searching/ should resolve to searching:index."""
        self.assertEqual(resolve('/searching/').view_name, 'searching:index')

    def test_detail_reverse(self):
        """searching:detail should reverse to /searching/<pk>/."""
        self.assertEqual(
            reverse('searching:detail', kwargs={ 'pk': 1 }),
            '/searching/1/'
        )

    def test_edit_reverse(self):
        """searching:edit should reverse to /searching/edit/."""
        self.assertEqual(reverse('searching:edit', kwargs={ 'pk': 1 }),
                         '/searching/1/edit/')

    def test_update_resolve(self):
        """/searching/~update/ should resolve to searching:update."""
        self.assertEqual(
            resolve('/searching/1/edit/').view_name,
            'searching:edit'
        )



class SearchModelTest(BaseUserTestCase):
        
    def test_string_representation(self):
        sSearch = "My clever search"
        oSearch = Search( cTitle = sSearch )
        self.assertEqual( str(oSearch), oSearch.cTitle )
    
    def AddNewSearchTest( TescCase ):        
        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A",
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertTrue(valid)        
        
        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                iDummyCategory  = 1,
                cPriority       = "A",
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertTrue(valid)
        
        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                cPriority       = "A",
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertFalse(valid)

        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                iDummyCategory  = 'abc',
                cPriority       = "A",
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertFalse(valid)
