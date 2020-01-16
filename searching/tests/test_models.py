from django.test.client import Client

from core.utils_test    import ( BaseUserWebTestCase,
                                 getUrlQueryStringOff, queryGotUpdated )

from core.utils_test    import TestCasePlus

from searching          import ( SEARCH_FILES_FOLDER,
                                 RESULTS_FILE_NAME_PATTERN )

from .base              import PutSearchResultsInDatabaseWebTestBase

from ..models           import Search

from ..utils            import storeSearchResultsInFinders, getSearchIdStr

from finders.models     import ItemFound, UserItemFound, ItemFoundTemp
from models.models      import Model

from pyPks.File.Del     import DeleteIfExists
from pyPks.File.Write   import QuietDump


class SearchModelTest( BaseUserWebTestCase ):

    def test_string_representation(self):
        sSearch = "My clever search 2"
        oSearch = Search( cTitle = sSearch )
        self.assertEqual( str(oSearch), oSearch.cTitle )

    def test_get_absolute_url(self):
        #
        sSearch     = "My clever search 1"
        oSearch     = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        #

        tParts = getUrlQueryStringOff( oSearch.get_absolute_url() )
        #
        self.assertEqual( tParts[0], '/searching/%s/' % oSearch.id )
        #
        self.assertTrue( queryGotUpdated( tParts[1] ) )
        #
        self.assertFalse( queryGotUpdated( tParts[0] ) )




class PutSearchResultsInDatabaseWebTest( PutSearchResultsInDatabaseWebTestBase ):

    def test_data_load( self ):
        #
        iItemFound = ItemFound.objects.all().count()
        #
        self.assertGreater( iItemFound, 60 )
        #
        iCount = Model.objects.all().count()
        #
        self.assertGreater( iCount, 160 )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_shipping_option_choices( self ):
        #
        '''test shipping choice
        was called over and over by
        core.tests.test_mixins.TestPagination
        finders.tests.test_views.FindersViewsTests
        keepers.tests.test_utils.GetAndStoreSingleItemsWebTests
        keepers.tests.test_utils.StoreSingleKeepersWebTests
        keepers.tests.test_utils.UserItemsTests
        searching.tests.test_models.PutSearchResultsInDatabaseWebTest
        searching.tests.test_stars.FindSearchHitsWebTests
        and some others
        '''
        #
        oItem = ItemFound.objects.get( iItemNumb = 254130264753 )
        #
        self.assertEqual( oItem.iShippingType, 5 )
        #
        self.assertEqual( oItem.get_iShippingType_display(), 'Pick Up ONLY!' )
        #
        #
        oItem = ItemFound.objects.get( iItemNumb = 323681140009 )
        #
        self.assertEqual( oItem.iShippingType, 0 )
        #
        self.assertEqual( oItem.get_iShippingType_display(), 'Calculated' )
        #
        #
        oItem = ItemFound.objects.get( iItemNumb = 173696834267 )
        #
        self.assertEqual( oItem.iShippingType, 1 )
        #
        self.assertEqual( oItem.get_iShippingType_display(),
                         'Calculated Domestic Flat International' )
        #
        #
        oItem = ItemFound.objects.get( iItemNumb = 323589685342 )
        #
        self.assertEqual( oItem.iShippingType, 2 )
        #
        self.assertEqual( oItem.get_iShippingType_display(), 'Flat' )
        #
        #
        oItem = ItemFound.objects.get( iItemNumb = 162988285719 )
        #
        self.assertEqual( oItem.iShippingType, 3 )
        #
        self.assertEqual( oItem.get_iShippingType_display(),
                         'Flat Domestic Calculated International' )
        #
        #
        oItem = ItemFound.objects.get( iItemNumb = 312436313310 )
        #
        self.assertEqual( oItem.iShippingType, 4 )
        #
        self.assertEqual( oItem.get_iShippingType_display(), 'Free' )
        #
        #
        oItem = ItemFound.objects.get( iItemNumb = 273380279306 )
        #
        self.assertEqual( oItem.iShippingType, 6 )
        #
        self.assertEqual( oItem.get_iShippingType_display(), 'Freight' )
        #
        # find no examples of FreightFlat & NotSpecified
        #
        oItem = ItemFound.objects.get( iItemNumb = 183953915448 )
        #
        self.assertEqual( oItem.iShippingType, 5 )
        #
        self.assertEqual( oItem.get_iShippingType_display(), 'Pick Up ONLY!' )
        #
        #
        oItem = ItemFound.objects.get( iItemNumb = 183952461011 )
        #
        self.assertEqual( oItem.iShippingType, 9 )
        #
        self.assertEqual( oItem.get_iShippingType_display(),
                          'Free Pick Up Option' ) # local pick up option
        #
        #
        oItem = ItemFound.objects.get( iItemNumb = 323984684424 )
        #
        self.assertEqual( oItem.iShippingType, 5 )
        #
        self.assertEqual( oItem.get_iShippingType_display(), 'Pick Up ONLY!' )
        #
        #
        oItem = ItemFound.objects.get( iItemNumb = 153723814561 )
        #
        self.assertEqual( oItem.iShippingType, 9 )
        #
        self.assertEqual( oItem.get_iShippingType_display(),
                          'Free Pick Up Option' )
        #
        #
        oItem = ItemFound.objects.get( iItemNumb = 184092262958 )
        #
        self.assertEqual( oItem.get_iShippingType_display(), 'Pick Up ONLY!' )
        #
        self.assertEqual( oItem.iShippingType, 5 )
        #
        #
        #
