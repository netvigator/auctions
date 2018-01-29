from django.core.urlresolvers   import reverse, resolve
from django.test.client         import Client
from django.test                import TestCase

from .forms                     import AddOrUpdateForm
from .models                    import Search
from .views                     import (
        SearchCreate, IndexView, SearchDetail, SearchDelete, SearchUpdate )


from core.tests                 import getDefaultMarket, BaseUserTestCase
from core.utils                 import getExceptionMessageFromResponse
from markets.models             import Market
from ebaycategories.models      import EbayCategory

from .test_big_text import sExampleResponse
from .utils         import getSearchResultGenerator

from File.Del   import DeleteIfExists
from File.Write import WriteText2File

from pprint import pprint

# Create your tests here.



class SearchViewsTests(BaseUserTestCase):

    def test_no_search_yet(self):
        #
        """
        If no search exists, an appropriate message is displayed.
        """
        self.client = Client()
        
        self.client.login(username='username1', password='mypassword')
        #
        response = self.client.get(reverse('searching:index'))
        #response = self.client.get('/searching/')
        
        #pprint( 'printing response:')
        #pprint( response )
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['search_list'], [])
        self.assertContains(response, "No searches are available.")


    def test_got_search(self):
        #
        """
        If no search exist, an appropriate message is displayed.
        """
        self.client = Client()
        
        self.client.login(username='username1', password='mypassword')
        #
        sSearch = "Great Widgets"
        oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        
        sSearch = "Phenominal Gadgets"
        oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        sGadgetID = str( oSearch.id )

        response = self.client.get(reverse('searching:index'))
        #response = self.client.get('/searching/')
        
        #print( 'printing response:')
        #pprint( response.context )
        #print( response.context['search_list'])
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['search_list'],
                ['<Search: Phenominal Gadgets>', '<Search: Great Widgets>'],
                ordered=False )
        self.assertContains(response, "Phenominal Gadgets")
        #
        response = self.client.get(
                reverse( 'searching:detail', kwargs={ 'pk': sGadgetID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phenominal Gadgets")
        
        self.client.logout()
        self.client.login(username='username2', password='mypassword')
        
        response = self.client.get(
                reverse( 'searching:detail', kwargs={ 'pk': sGadgetID } ) )

        self.assertEqual(response.status_code, 403) # forbidden
        self.assertEqual(
            getExceptionMessageFromResponse( response ),
            "Permission Denied -- that's not your record!" )

        self.client.logout()
        self.client.login(username='username3', password='mypassword')
        
        response = self.client.get(
                reverse( 'searching:detail', kwargs={ 'pk': sGadgetID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phenominal Gadgets")

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
                which           = 'Create',
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertTrue(valid)        
        
        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                iDummyCategory  = 1,
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertTrue(valid)
        
        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertFalse(valid)

        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                iDummyCategory  = 'abc',
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertFalse(valid)






sExampleFile = '/tmp/search_results.json'

class getImportSearchResultsTest(TestCase):
    #
    def test_get_search_results(self):
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        WriteText2File( sExampleResponse, sExampleFile )
        #
        itemResultsIterator = getSearchResultGenerator( sExampleFile )
        #
        dThisItem = next( itemResultsIterator )
        #
        self.assertEqual( dThisItem["itemId"],  "253313715173" )
        self.assertEqual( dThisItem["title" ],
            "Simpson 360-2 Digital Volt-Ohm Milliammeter Operator's Manual" )
        self.assertEqual( dThisItem["location"],"Ruskin,FL,USA" )
        self.assertEqual( dThisItem["country"], "US" )
        self.assertEqual( dThisItem["postalCode"], "33570" )
        self.assertEqual( dThisItem["globalId"], "EBAY-US" )
        self.assertEqual( dThisItem["galleryURL"], 
            "http://thumbs2.ebaystatic.com/m/m0WO4pWRZTzusBvJHT07rtw/140.jpg" )
        self.assertEqual( dThisItem["viewItemURL"],
            "http://www.ebay.com/itm/Simpson-360-2-Digital-Volt-Ohm-"
            "Milliammeter-Operators-Manual-/253313715173" )
        #
        dListingInfo    = dThisItem["listingInfo"]
        self.assertEqual( dListingInfo["startTime"], "2017-12-15T05:22:47.000Z" )
        self.assertEqual( dListingInfo[ "endTime" ], "2018-01-14T05:22:47.000Z" )
        self.assertEqual( dListingInfo["bestOfferEnabled" ], "false" )
        self.assertEqual( dListingInfo["buyItNowAvailable"], "false" )
        #
        dPrimaryCategory= dThisItem["primaryCategory"]
        self.assertEqual( dPrimaryCategory["categoryId"  ], "58277"       )
        self.assertEqual( dPrimaryCategory["categoryName"], "Multimeters" )
        #
        dCondition      = dThisItem["condition"]
        self.assertEqual( dCondition["conditionDisplayName"  ], "Used" )
        self.assertEqual( dCondition["conditionId"           ], "3000" )
        #
        dSellingStatus  = dThisItem["sellingStatus"]
        self.assertEqual( dSellingStatus["sellingState"], "Active" )
        
        dCurrentPrice   = dSellingStatus["currentPrice"]
        self.assertEqual( dCurrentPrice["@currencyId"], "USD" )
        self.assertEqual( dCurrentPrice["__value__"  ], "10.0")
        #
        dConvertPrice   = dSellingStatus["convertedCurrentPrice"]
        self.assertEqual( dConvertPrice["@currencyId"], "USD" )
        self.assertEqual( dConvertPrice["__value__"  ], "10.0")
        #
        dPagination     = dThisItem["paginationOutput"]
        self.assertEqual( dPagination["totalEntries"], "4" )
        self.assertEqual( dPagination["thisEntry"   ], "1" )
        #
        iItems = 1
        #
        for dThisItem in itemResultsIterator:
            #
            iItems += 1
            #
        self.assertEqual( iItems, 4 )
        #
        DeleteIfExists( sExampleFile )




