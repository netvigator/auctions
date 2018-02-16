from datetime                   import timedelta

from django.contrib.auth        import get_user_model
from django.core.urlresolvers   import reverse, resolve
from django.http.request        import HttpRequest
from django.test.client         import Client, RequestFactory
from django.test                import TestCase
from django.utils               import timezone

from core.tests                 import ( BaseUserTestCase, getDefaultMarket,
                                         getUrlQueryStringOff, queryGotUTC )

from core.utils                 import getExceptionMessageFromResponse
from markets.models             import Market
from ebaycategories.models      import EbayCategory

from .forms                     import SearchAddOrUpdateForm
from .models                    import Search, ItemFound
from .test_big_text             import sExampleResponse
from .utils                     import getSearchResultGenerator
from .views                     import (
        SearchCreate, IndexView, SearchDetail, SearchDelete, SearchUpdate )

from File.Del                   import DeleteIfExists
from File.Write                 import WriteText2File


# from pprint import pprint

# Create your tests here.

class SearchViewsHitButtons(BaseUserTestCase):
    """
    Test Save and Cancel
    """
    def setUp(self):
        #
        super( SearchViewsHitButtons, self ).setUp()
        #
        self.factory = RequestFactory()
    

    def test_get(self):
        """
        Test GET requests
        """
        request = self.factory.get(reverse('searching:add'))
        request.user = self.user1
        #
        response = SearchCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)
        #print( 'response.context_data has form and view, view keys:' )
        #for k in response.context_data['view'].__dict__:
            #print( k )
        #self.assertEqual(response.context_data['iUser'], self.user1)
        self.assertEqual(response.context_data['view'].__dict__['request'], request)


    # @patch('searching.models.Search.save', MagicMock(name="save"))
    def test_post(self):
        """
        Test post requests
        """
        data = dict( cTitle = "Great Widgets", iUser = self.user1 )
        # Create the request
        response = self.client.post(reverse('searching:add'), data )
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 302)
        #oSearch = Search.objects.get( cTitle = "Great Widgets" )
        #self.assertEqual( oSearch, self.searching )


        
    #def test_add_hit_cancel(self):
        ##
        #"""
        #Hit cancel when adding
        #"""
        #self.client = Client()
        ##
        #self.client.login(username='username1', password='mypassword')
        ##
        #sSearch = "Great Widgets"
        #oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        ##
        ##
    #

class SearchViewsTests(BaseUserTestCase):

    def test_no_search_yet(self):
        #
        """
        If no search exists, an appropriate message is displayed.
        """
        self.client = Client()
        #
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
        #
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

        """
        Not logged in, cannot see form, direct to login page.
        """
        self.client.logout()
        response = self.client.get(reverse('searching:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/searching/')



    #def test_get_success_url(self):
        ## Expect: '/users/testuser/', as that is the default username for
        ##   self.make_user()
        #self.assertEqual(
            #self.view.get_success_url(),
            #'/searching/index/'
        #)
    #def test_get_object(self):
        ## Expect: self.user, as that is the request's user object
        #self.assertEqual(
            #self.view.get_object(),
            #self.user
        #)


class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
        oSearch = Search(
            cTitle          = "My clever search 1",
            cKeyWords       = "Blah bleh blih",
            cPriority       = "A",
            iUser           = self.user1,
            id              = 1 )
        #
        oSearch.save()
        #
        tParts = getUrlQueryStringOff( oSearch.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/searching/%s/' % oSearch.id )
        #
        self.assertTrue( queryGotUTC( tParts[1] ) )
        #
        self.assertFalse( queryGotUTC( tParts[0] ) )

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
        sSearch = "My clever search 2"
        oSearch = Search( cTitle = sSearch )
        self.assertEqual( str(oSearch), oSearch.cTitle )

    def test_AddNewSearch(self):

        # has key words
        dData = dict(
                cTitle          = "My clever search 3",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertTrue( form.is_valid() )

        # has a category
        dData = dict(
                cTitle          = "My clever search 4",
                iDummyCategory  = 10,
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request

        self.assertTrue( form.is_valid() )
        # no key words, no category
        dData = dict(
                cTitle          = "My clever search 5",
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData ) 
        form.request = self.request
        self.assertFalse( form.is_valid() )

        # has an invalid category
        dData = dict(
                cTitle          = "My clever search 6",
                iDummyCategory  = 'abc',
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertFalse( form.is_valid() )





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




class ItemsFoundRecyclingTest(BaseUserTestCase):

    def test_fetch_oldest_of_the_old(self):
        #
        from datetime       import timedelta
        from django.utils   import timezone
        #
        from .utils         import getItemFoundForWriting
        """
        Want to recycle old records, make sure this is working!
        """
        #
        iWantOlderThan = 120
        #
        #
        sItemTitle1 = "Great Widget"
        iItemID     = 2823
        oSearch = ItemFound( cTitle = sItemTitle1,
                             iItemNumb = iItemID, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan -2 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        sItemTitle2 = "Phenominal Gadget"
        iItemID     = 2418
        oSearch = ItemFound( cTitle = sItemTitle2,
                             iItemNumb = iItemID, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan + 1 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        sItemTitle3 = "Awesome Thing a Ma Jig"
        iItemID     = 2607
        oSearch = ItemFound( cTitle = sItemTitle3,
                             iItemNumb = iItemID, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan + 2 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        oWriteable = getItemFoundForWriting()
        #
        self.assertEqual( oWriteable.cTitle, sItemTitle3 )
        #
        self.assertTrue( timezone.now() >= oWriteable.tCreate )
        
        tFuture = oWriteable.tCreate + timedelta( seconds = 1 )
        self.assertTrue( timezone.now() < tFuture )
        #
        oWriteable = getItemFoundForWriting( iWantOlderThan = 140 )
        #
        self.assertEqual( oWriteable.cTitle, '' )



class TestFormValidation(BaseUserTestCase):
    
    ''' Search Form Tests '''
    
    def setUp(self):
        #
        super( TestFormValidation, self ).setUp()
        #
        getDefaultMarket( self )
        #
        oUser = get_user_model()
        #
        self.client = Client()
        self.client.login(username ='username1', password='mypassword')
        #
        self.request = HttpRequest()
        self.request.user = self.user1
        #
    '''
    def test_save_redirect(self):
        #
        form_data = dict(
            cTitle      = 'Great Widget',
            cPriority   = "A",
            cKeyWords   = "Blah bleh blih",
            iUser       = self.user1.id
            )
        #
        form = SearchAddOrUpdateForm(data=form_data)
        form.request = self.request
            #which           = 'Create',
        self.assertTrue( form.is_valid() )
        
        # test save
        form.instance.iUser = self.user1
        form.save()
        oSearch = Search.objects.get( cTitle = 'Great Widget' )
        self.assertEqual(
            reverse('searching:detail', kwargs={ 'pk': oSearch.id } ),
            '/searching/%s/' % oSearch.id )
    '''
    def test_stuff_in_there_already(self):
        #
        dData = dict(
                cTitle          = "My clever search 7",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        #
        form = SearchAddOrUpdateForm(data=dData)
        form.request            = self.request
        form.instance.iUser     = self.user1
        form.save()        
        #
        dData = dict(
                cTitle          = "Very clever search",
                cKeyWords       = "Blah bleh blih", # same as above
                which           = 'Create',
                cPriority       = "B",
                iUser           = self.user1 )
        #
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertFalse( form.is_valid() )
        #
        dData = dict(
                cTitle          = "Very clever search",
                cKeyWords       = "Blah blih bleh", # same but different order
                which           = 'Create',
                cPriority       = "B",
                iUser           = self.user1 )
        #
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertTrue( form.is_valid() ) # not comparing sets yet
        
        #
        '''
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors at bottom!' )
        '''
