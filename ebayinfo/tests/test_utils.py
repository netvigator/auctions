import inspect

from os                     import rename
from random                 import randrange

from django.db              import DataError
from django.test            import tag

from core.utils             import updateMemoryTableUpdated

from core.tests.base        import getDefaultMarket, \
                                   GetEbayCategoriesWebTestSetUp
from core.tests.base_class  import TestCasePlus

from ebayinfo               import EBAY_SHIPPING_CHOICES, \
                                   dEBAY_SHIPPING_CHOICE_CODE, \
                                   getEbayShippingChoiceCode

from ..models               import EbayCategory, Market, CategoryHierarchy

# the following are in the tests __init__.py file
from ..tests                import sExampleCategoryVersion, \
                                   sExampleCategoryList, \
                                   EBAY_CURRENT_VERSION_US, \
                                   EBAY_CURRENT_VERSION_SG

from ..utils                import CATEGORY_VERSION_FILE, \
                                   _getCategoryVersionFromFile, \
                                   UnexpectedResponse, CATEGORY_LISTING_FILE, \
                                   _putCategoriesInDatabase, _countCategories, \
                                   _getCheckCategoryVersion, dSiteID2ListVers, \
                                   getWhetherAnyEbayCategoryListsAreUpdated, \
                                   getEbayCategoryHierarchies, \
                                   getShowMarketsHaveNewerCategoryVersionLists

from .base                  import PutMarketsInDatabaseTestPlusBase, \
                                   GetMarketsAndCategoriesWebTestSetUp, \
                                   GetMarketsAndCategoriesTestPlusSetUp

from .test_auth_token       import ConfFileTokenExpiredTests

from pyPks.File.Del         import DeleteIfExists
from pyPks.File.Write       import WriteText2File
from pyPks.Utils.Get        import getRandomTrueOrFalse

sMessedCategoryVersion = sExampleCategoryVersion.replace(
        'GetCategoriesResponse', 'ResponseGetCategories' )

sExampleFailureVersion = sExampleCategoryVersion.replace(
        'Success', 'Failure' )

sExampleWrongChildTag = sExampleCategoryVersion.replace(
        'Version', 'Venison' )


class CatetoryVersionMissing( Exception ): pass
class CatetoryListHasNewVers( Exception ): pass


class TestEbayShippingChoices(TestCasePlus):

    def test_CHOICES( self ):
        """ test the ebay shipping choices tuple """
        self.assertEqual( EBAY_SHIPPING_CHOICES[5], ( 5, 'Pick Up ONLY!' ) )

    def test_dCHOICE_CODES( self ):
        """ test the ebay shipping choices dictionary """
        self.assertEqual( dEBAY_SHIPPING_CHOICE_CODE['FreePickup'], 5 )

    def test_getEbayShippingChoiceCode( self ):
        """ test the ebay shipping choice code function """
        self.assertEqual( getEbayShippingChoiceCode('FreePickup'), 5 )



class TestCategoryVersionTest( TestCasePlus ):
    '''test _getCategoryVersionFromFile()'''

    sFile = CATEGORY_VERSION_FILE % 'EBAY-US'

    def tearDown(self):
        DeleteIfExists( self.sFile )

    def test_get_category_version(self):
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        WriteText2File(
                sExampleCategoryVersion, self.sFile )
        self.assertEqual(
                _getCategoryVersionFromFile(), 117 )

    def test_file_wrong_category_version(self):
        '''test with incorrect GetCategoriesResponse'''
        #
        WriteText2File(
                sMessedCategoryVersion, self.sFile )
        try:
            _getCategoryVersionFromFile()
        except UnexpectedResponse as e:
            self.assertEqual(
                    str(e),
                    'Check file %s for correct output!' % self.sFile )

    def test_Failure_not_Success(self):
        '''test without Success in Ack'''
        #
        WriteText2File(
                sExampleFailureVersion, self.sFile )
        try:
            _getCategoryVersionFromFile()
        except UnexpectedResponse as e:
            self.assertEqual(
                    str(e),
                    'Check file %s for tag "Ack" -- '
                        'should be "Success"!' % self.sFile )

    def test_wrong_child_tag(self):
        '''test with missing child tag'''
        #
        WriteText2File(
                sExampleWrongChildTag, self.sFile )
        try:
            _getCategoryVersionFromFile()
        except UnexpectedResponse as e:
            self.assertEqual(
                    str(e),
                    'Check file %s for tag "%s"!' % ( self.sFile , 'Version' ) )
        else:
            self.assertTrue( False )



class PutCategoriesInDatabaseTestCasePlus( TestCasePlus ):
    '''test _getCategoryVersionFromFile()'''

    sFile = CATEGORY_LISTING_FILE % 'EBAY-US'

    def setUp(self):
        getDefaultMarket()

    def tearDown(self):
        pass # DeleteIfExists( self.sFile )

    def test_put_categories_in_database(self):
        #
        WriteText2File(
                sExampleCategoryList, self.sFile )
        #
        _putCategoriesInDatabase( uMarket = 'EBAY-US', uWantVersion = '117' )
        #
        oGreek = EbayCategory.objects.get( iCategoryID = 37906 )
        #
        self.assertEqual( oGreek.name, 'Greek' )


    def test_category_name_too_long(self):
        #
        sLong = ( 'Greek week, Greek food, Greek mythology, '
                    'Greek way, Greek restaurant ' )
        #
        sLongName = sExampleCategoryList.replace( 'Greek', sLong )
        #
        WriteText2File( sLongName, self.sFile )
        #
        try:
            _putCategoriesInDatabase( uMarket = 'EBAY-US', uWantVersion = '117' )
        except DataError as e:
            sMsg = str(e)
            self.assertEqual( sMsg[ - len( sLong ) : ], sLong )
        else:
            self.assertTrue( False )


    def test_database_wrong_category_version(self):
        #
        sWrongVersion = sExampleCategoryList.replace(
                'Version>117</Category', 'Version>116</Category' )

        sFileName = '%s_WrongVersion' % self.sFile
        WriteText2File( sWrongVersion, sFileName )
        #
        try:
            _putCategoriesInDatabase( sFile = sFileName, uWantVersion = '117')
        except UnexpectedResponse as e:
            self.assertEqual(
                    str(e),
                    'Check file %s for tag "CategoryVersion" -- '
                        'should be %s!' % ( sFileName, '117' ) )
        else:
            self.assertTrue( False )

    def test_count_categories_in_file(self):
        #
        WriteText2File(
                sExampleCategoryList, self.sFile )
        #
        iTags, iCount = _countCategories()
        #
        self.assertEqual( 8, iCount ) #  integer count in the abbreviated file
        self.assertEqual( iTags, '19188' ) # str count in the original file



class TestWhetherHeirarchiesAreCompleteMixin( object ):

    def test_are_heirarchies_complete( self ):
        #
        oLeaves = EbayCategory.objects.filter( bLeafCategory = True )
        #
        dEbayCatHierarchies = {}
        #
        for oLeaf in oLeaves:
            #
            dItem = dict(
                primaryCategory = dict(
                    categoryId      = oLeaf.iCategoryID,
                    categoryName    = oLeaf.name ),
                secondaryCategory   = {},
                globalId            = oLeaf.iEbaySiteID.cMarket )
            #
            t = getEbayCategoryHierarchies( dItem, dEbayCatHierarchies )
            #
        #
        self.assertEqual( len( oLeaves ), len( dEbayCatHierarchies ) )
        #
        tRadiosAndSpeakers = ( 80741, 100 ) # ebay motors
        #
        self.assertTrue( tRadiosAndSpeakers in dEbayCatHierarchies )
        #
        self.assertTrue( dEbayCatHierarchies[ tRadiosAndSpeakers ] )
        #
        iCategoryHeirarchyID = dEbayCatHierarchies[ tRadiosAndSpeakers ]
        #
        oCatHier = CategoryHierarchy.objects.get( id = iCategoryHeirarchyID )
        #
        self.assertEqual( oCatHier.cCatHierarchy,
                'eBay Motors, Parts & Accessories, Vintage Car & Truck Parts, '
                'Radio & Speaker Systems' )
        #
        tTubeTesters = ( 170062, 0 ) # ebay USA
        #
        self.assertTrue( tTubeTesters in dEbayCatHierarchies )
        #
        self.assertTrue( dEbayCatHierarchies[ tTubeTesters ] )
        #
        iCategoryHeirarchyID = dEbayCatHierarchies[ tTubeTesters ]
        #
        oCatHier = CategoryHierarchy.objects.get( id = iCategoryHeirarchyID )
        #
        self.assertEqual( oCatHier.cCatHierarchy,
                'Business & Industrial, Electrical & Test Equipment, '
                'Test, Measurement & Inspection, Testers & Calibrators, '
                'Tube Testers' )
        #
        #print()
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

class TestHeirarchiesAreTheyCompleteWebTest(
        TestWhetherHeirarchiesAreCompleteMixin, GetEbayCategoriesWebTestSetUp ):
    #
    '''obsolete when the changes started in June 2021 are complete'''
    #
    # test comes in via mixin above
    #
    pass


class AreHeirarchiesCompleteWebTest(
        TestWhetherHeirarchiesAreCompleteMixin, GetMarketsAndCategoriesWebTestSetUp ):
    #
    # test comes in via mixin above
    #
    # new June 2021
    #
    pass


class AreHeirarchiesCompleteTestPlus(
        TestWhetherHeirarchiesAreCompleteMixin, GetMarketsAndCategoriesTestPlusSetUp ):
    #
    # test comes in via mixin above
    #
    # new June 2021
    #
    pass


class PutMarketsInDatabaseTest( PutMarketsInDatabaseTestPlusBase ):
    '''test getMarketsIntoDatabase()'''
    #
    # compatible with new June 2021
    #

    def test_market_count( self ):
        #
        iCount = Market.objects.all().count()
        #
        self.assertEqual( 23, iCount )

    def test_got_market_info_right( self ):
        #
        oUSA = Market.objects.get( cMarket = 'EBAY-US' )
        #
        self.assertEqual( oUSA.iEbaySiteID, 0 )
        #
        self.assertEqual( oUSA.cCurrencyDef, 'USD' )
        #
        self.assertEqual( oUSA.iCategoryVer, EBAY_CURRENT_VERSION_US )
        #
        oSG  = Market.objects.get( cMarket = 'EBAY-SG' )
        #
        self.assertEqual( oSG.iEbaySiteID, 216 )
        #
        self.assertEqual( oSG.iCategoryVer, EBAY_CURRENT_VERSION_SG )

    def test_market_count( self ):
        #
        iCount = Market.objects.all().count()
        #
        self.assertEqual( 23, iCount )

    def test_got_market_info_right( self ):
        #
        oUSA = Market.objects.get( cMarket = 'EBAY-US' )
        #
        self.assertEqual( oUSA.iEbaySiteID, 0 )
        #
        self.assertEqual( oUSA.cCurrencyDef, 'USD' )
        #
        oSG  = Market.objects.get( cMarket = 'EBAY-SG' )
        #
        self.assertEqual( oSG.iEbaySiteID, 216 )
        #
        self.assertEqual( oSG.iCategoryVer, EBAY_CURRENT_VERSION_SG )



class MarketsAndCategoriesTests( PutMarketsInDatabaseTestPlusBase ):
    '''test getMarketsIntoDatabase()'''
    #
    # compatible with new June 2021
    #

    def test_token_expiration( self ):
        #
        ConfFileTokenExpiredTests.not_here_test_token_expiration( self ) # real
        #ConfFileTokenExpiredTests.not_here_test_token_expiration( self, -10 )
        #ConfFileTokenExpiredTests.not_here_test_token_expiration( self,  10 )


    @tag('ebay_api') # pmt script has exclude-tag param, excludes this test
    def test_got_current_category_version_list( self ):
        #
        iCount = Market.objects.all().count()
        #
        iRandom = randrange( 0, iCount )
        #
        oMarket = Market.objects.all()[ iRandom ]
        #
        if getRandomTrueOrFalse(): # randomly alternate
            #
            iCurrentVersion = _getCheckCategoryVersion(
                    iSiteId = oMarket.iEbaySiteID, bUseSandbox = False )
            #
        else:
            #
            iCurrentVersion = _getCheckCategoryVersion(
                    sGlobalID = oMarket.cMarket, bUseSandbox = False )
            #
        #
        self.assertEqual( iCurrentVersion, oMarket.iCategoryVer )
        #


    def test_whether_ebay_categories_were_updated( self ):
        #
        lUpdated = getShowMarketsHaveNewerCategoryVersionLists()
        #
        if lUpdated:
            #
            print( '\n\n### ebay has updated categories ! ###\n' )
            #
            for s in lUpdated: print( s )
            #
        else:
            #
            print( '\nebay categories are up to date.' )
            #


    @tag('ebay_api') # pmt script has exclude-tag param, excludes this test
    def test_whether_ebay_market_updated_test_is_working( self ):
        #
        oUSA = Market.objects.get( cMarket = 'EBAY-US' )
        #
        oUSA.iCategoryVer = EBAY_CURRENT_VERSION_US - 1
        #
        oUSA.save()
        #
        updateMemoryTableUpdated( 'markets', sField = 'iCategoryVer' )
        #
        oSG  = Market.objects.get( cMarket = 'EBAY-SG' )
        #
        lUpdated = getWhetherAnyEbayCategoryListsAreUpdated(
                        bUseSandbox = False )
        #
        # sandbox can be ahead of the production site
        #
        oUSA = Market.objects.get( cMarket = 'EBAY-US' )
        #
        self.assertTrue( bool( lUpdated ) )
        #


class LiveTestGotCurrentEbayCategories( PutMarketsInDatabaseTest ):
    '''test getMarketsIntoDatabase()'''
    #
    # compatible with new June 2021
    #

    @tag('ebay_api') # pmt script has exclude-tag param, excludes this test
    def test_check_whether_any_ebay_market_list_is_updated( self ):
        #
        lUpdated = getWhetherAnyEbayCategoryListsAreUpdated(
                        bUseSandbox = False )
        #
        # sandbox can be ahead of the production site
        #
        #
        print( '')
        #
        if len( lUpdated ) == 0:
            #
            print( '*** auctionbot ebay categories are up to date ***' )
            #
            oUSA = Market.objects.get( cMarket = 'EBAY-US' )
            #
            self.assertEqual( oUSA.iCategoryVer, EBAY_CURRENT_VERSION_US )
            #
        else:
            #
            print( '*** ebay has updated categories, '
                   'you need to update local table in '
                   'ebayinfo/__init__.py ***' )
            #
            lDecorated = [ ( d['iSiteID'], d ) for d in lUpdated ]
            #
            lDecorated.sort()
            #
            #lDecorated[0]['iTableHas'] = EBAY_CURRENT_VERSION_US
            #
            for t in lDecorated:
                #
                print( t[1] )
                #
            #
        #
        print( '')
