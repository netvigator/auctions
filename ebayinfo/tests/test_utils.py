from django.db          import DataError
from django.test        import TestCase, tag


from core.utils_testing import getDefaultMarket

from ..models           import EbayCategory, Market

# the following are in the tests __init__.py file
from ..tests            import sExampleCategoryVersion, sExampleCategoryList

from ..utils            import ( CATEGORY_VERSION_FILE, getCategoryVersion,
                                 UnexpectedResponse, CATEGORY_LISTING_FILE,
                                 putCategoriesInDatabase, countCategories,
                                 getMarketsIntoDatabase,
                                 getCheckCategoryVersion )

from File.Del           import DeleteIfExists
from File.Write         import WriteText2File


sMessedCategoryVersion = sExampleCategoryVersion.replace(
        'GetCategoriesResponse', 'ResponseGetCategories' )

sExampleFailureVersion = sExampleCategoryVersion.replace(
        'Success', 'Failure' )

sExampleWrongChildTag = sExampleCategoryVersion.replace(
        'Version', 'Venison' )


class CatetoryVersionMissing( Exception ): pass
class CatetoryListHasNewVers( Exception ): pass



class getCategoryVersionTest(TestCase):
    '''test getCategoryVersion()'''
    
    sFile = CATEGORY_VERSION_FILE % 'EBAY-US'

    def tearDown(self):
        DeleteIfExists( self.sFile )
        
    def test_get_category_version(self):
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        WriteText2File(
                sExampleCategoryVersion, self.sFile )
        self.assertEqual( getCategoryVersion(), 117 )

    def test_wrong_category_version(self):
        '''test with incorrect GetCategoriesResponse'''
        #
        WriteText2File(
                sMessedCategoryVersion, self.sFile )
        try:
            getCategoryVersion()
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
            getCategoryVersion()
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
            getCategoryVersion()
        except UnexpectedResponse as e:
            self.assertEqual(
                    str(e),
                    'Check file %s for tag "%s"!' % ( self.sFile , 'Version' ) )
        else:
            self.assertTrue( False )



class putCategoriesInDatabaseTest(TestCase):
    '''test getCategoryVersion()'''

    sFile = CATEGORY_LISTING_FILE % 'EBAY-US'

    def setUp(self):
        getDefaultMarket()

    def tearDown(self):
        DeleteIfExists( self.sFile )

    def test_put_categories_in_database(self):
        #
        WriteText2File(
                sExampleCategoryList, self.sFile )
        #
        putCategoriesInDatabase()
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
            putCategoriesInDatabase()
        except DataError as e:
            sMsg = str(e)
            self.assertEqual( sMsg[ - len( sLong ) : ], sLong )
        else:
            self.assertTrue( False )
        
        


    def test_wrong_category_version(self):
        #
        sWrongVersion = sExampleCategoryList.replace(
                'Version>117</Category', 'Version>118</Category' )
        WriteText2File(
                sWrongVersion, self.sFile )
        #
        try:
            putCategoriesInDatabase()
        except UnexpectedResponse as e:
            self.assertEqual(
                    str(e),
                    'Check file %s for tag "CategoryVersion" -- '
                        'should be %s!' % ( self.sFile, '117' ) )
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



class putMarketsInDatabaseTest(TestCase):
    '''test getMarketsIntoDatabase()'''
    #
    def setUp(self):
        #
        super( putMarketsInDatabaseTest, self ).setUp()
        #
        getMarketsIntoDatabase()

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
            iCurrentVersion = getCheckCategoryVersion(
                    iSiteId = oMarket.iEbaySiteID, bUseSandbox = True )
            #
        else:
            #
            iCurrentVersion = getCheckCategoryVersion(
                    sGlobalID = oMarket.cMarket, bUseSandbox = True )
            #
        #
        if iCurrentVersion != oMarket.iCategoryVer:
            #
            print( '\n' )
            print( 'testing market %s' % oMarket.cMarket )
            #
        #
        self.assertEqual( iCurrentVersion, oMarket.iCategoryVer )
        #

    @tag('ebay_api')
    def test_check_whether_any_ebay_market_list_is_updated( self ):
        #
        oUSA = Market.objects.get( cMarket = 'EBAY-US' )
        #
        oUSA.iCategoryVer = 116 # current version is actually 117
        oUSA.save()
        #
        lUpdated = getWhetherAnyEbayCategoryListsAreUpdated(
                        bUseSandbox = True )
        #
        self.assertEqual( lUpdated, [ oUSA.iEbaySiteID ] )
        #
