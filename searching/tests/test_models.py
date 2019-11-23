from django.test.client import Client

from core.utils_test    import ( BaseUserWebTestCase,
                                 getUrlQueryStringOff, queryGotUpdated )

from json.decoder       import JSONDecodeError

from core.utils_test    import TestCasePlus

from searching          import ( SEARCH_FILES_FOLDER,
                                 RESULTS_FILE_NAME_PATTERN )

from finders            import ( EBAY_SHIPPING_CHOICES, getChoiceCode,
                                 dEBAY_SHIPPING_CHOICE_CODE )

from .test_utils        import GetBrandsCategoriesModelsWebTestSetUp

from ..models           import Search

from ..tests            import sResponseItems2Test
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


class TestChoices(TestCasePlus):

    def test_CHOICES( self ):
        """ test the ebay shipping choices tuple """
        self.assertEqual( EBAY_SHIPPING_CHOICES[5], ( 5, 'Pick Up ONLY!' ) )

    def test_dCHOICE_CODES( self ):
        """ test the ebay shipping choices dictionary """
        self.assertEqual( dEBAY_SHIPPING_CHOICE_CODE['FreePickup'], 5 )

    def test_getChoiceCode( self ):
        """ test the ebay shipping choice code function """
        self.assertEqual( getChoiceCode('FreePickup'), 5 )


class PutSearchResultsInDatabaseWebTest( GetBrandsCategoriesModelsWebTestSetUp ):
    #
    ''' class for testing storeSearchResultsInFinders() store records '''
    #
    def setUp( self ):
        #
        super( PutSearchResultsInDatabaseWebTest, self ).setUp()
        #
        self.dExampleFiles = {}
        #
        for oUser in self.tUsers:
            #
            sExampleFile = (
                RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
                ( 'EBAY-US',
                oUser.username,
                getSearchIdStr( self.oSearch.id ),
                '000' ) )
            #
            self.dExampleFiles[ oUser.id ] = sExampleFile
            #
            #print( 'will DeleteIfExists' )
            DeleteIfExists( SEARCH_FILES_FOLDER, sExampleFile )
            #
            #print( 'will QuietDump' )
            QuietDump( sResponseItems2Test, SEARCH_FILES_FOLDER, sExampleFile )
            #
            try:
                t = ( storeSearchResultsInFinders(
                                self.oSearchLog.id,
                                self.sMarket,
                                oUser.username,
                                self.oSearch.id,
                                self.oSearch.cTitle,
                                self.setTestCategories ) )
                #
            except JSONDecodeError:
                #
                print('')
                print(  '### maybe a new item title has a quote '
                        'but only a single backslash ###' )
                #
                raise
                #
            #
            #iCountItems, iStoreItems, iStoreUsers = t
            #
            #iTempItems = ItemFoundTemp.objects.all().count()
            #iItemFound = ItemFound.objects.all().count()
            #
            # bCleanUpAfterYourself must be False or tests will fail!
            #
            #print( '\n' )
            #print( 'setting up KeyWordFindSearchHitsTests' )

    def tearDown(self):
        #
        for sExampleFile in self.dExampleFiles.values():
            #
            DeleteIfExists( SEARCH_FILES_FOLDER, sExampleFile )



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


    def test_shipping_option_choices( self ):
        #
        '''test shipping choice'''
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
