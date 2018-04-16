from os             import rename

from django.db      import DataError
from django.test    import TestCase, tag

from core.utils     import updateMemoryTableUpdated
from core.utils_test import getDefaultMarket, getEbayCategoriesSetUp

from ..models       import EbayCategory, Market

# the following are in the tests __init__.py file
from ..tests        import sExampleCategoryVersion, sExampleCategoryList

from ..utils        import ( CATEGORY_VERSION_FILE,
                            _getCategoryVersionFromFile,
                            UnexpectedResponse, CATEGORY_LISTING_FILE,
                            _putCategoriesInDatabase, countCategories,
                            _getCheckCategoryVersion, dSiteID2ListVers,
                            getWhetherAnyEbayCategoryListsAreUpdated,
                            getEbayCategoryHierarchies )

from ..utils_test   import getMarketsIntoDatabase, PutMarketsInDatabaseTest

from File.Del       import DeleteIfExists
from File.Write     import WriteText2File


sMessedCategoryVersion = sExampleCategoryVersion.replace(
        'GetCategoriesResponse', 'ResponseGetCategories' )

sExampleFailureVersion = sExampleCategoryVersion.replace(
        'Success', 'Failure' )

sExampleWrongChildTag = sExampleCategoryVersion.replace(
        'Version', 'Venison' )


class CatetoryVersionMissing( Exception ): pass
class CatetoryListHasNewVers( Exception ): pass



class getCategoryVersionTest(TestCase):
    '''test _getCategoryVersionFromFile()'''
    
    sFile = CATEGORY_VERSION_FILE % 'EBAY-US'

    def tearDown(self):
        DeleteIfExists( self.sFile )
        
    def test_get_category_version(self):
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        WriteText2File(
                sExampleCategoryVersion, self.sFile )
        self.assertEqual( _getCategoryVersionFromFile(), 117 )

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



class _putCategoriesInDatabaseTest(TestCase):
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
        iTags, iCount = countCategories()
        #
        self.assertEqual( 8, iCount ) #  integer count in the abbreviated file
        self.assertEqual( iTags, '19188' ) # str count in the original file


class TestHeirarchiesAreTheyCompleteTest( getEbayCategoriesSetUp ):
    
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



    
class TestPutMarketsInDatabaseTest(PutMarketsInDatabaseTest):
    '''test getMarketsIntoDatabase()'''
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
        oSG  = Market.objects.get( cMarket = 'EBAY-SG' )
        #
        self.assertEqual( oSG.iEbaySiteID, 216 )
        #
        self.assertEqual( oSG.iCategoryVer, 30 )


    @tag('ebay_api')
    def test_got_current_category_version_list( self ):
        #
        from random import randrange
        #
        from Utils.Get import getRandomTrueOrFalse
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

    @tag('ebay_api')
    def test_check_whether_any_ebay_market_list_is_updated( self ):
        #
        oUSA = Market.objects.get( cMarket = 'EBAY-US' )
        #
        oUSA.iCategoryVer = 116 # current SANDBOX version is actually 118
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
        if lUpdated:
            self.assertEqual( lUpdated[0].get('iSiteID'),   oUSA.iEbaySiteID )
            self.assertEqual( lUpdated[0].get('iTableHas'), 116 )
            self.assertEqual( lUpdated[0].get('iEbayHas'),  118 )


