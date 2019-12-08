import inspect
import logging

from os.path            import realpath, join
from datetime           import timedelta

from django.core.exceptions import ObjectDoesNotExist

from django.test        import tag
from django.utils       import timezone
from core.utils_test    import ( getDefaultMarket,
                                 GetEbayCategoriesWebTestSetUp,
                                 getTableFromScreenCaptureGenerator,
                                 getNamePositionDict,
                                 TestCasePlus )

from ebayinfo.models    import EbayCategory, CategoryHierarchy
from ebayinfo.utils     import dMarket2SiteID, getEbayCategoryHierarchies

from ebayinfo.tests.test_utils import LiveTestGotCurrentEbayCategories
# imported live test will run automatically when running live test

from searching          import RESULTS_FILE_NAME_PATTERN
from searching          import SEARCH_FILES_FOLDER

from ..models           import Search, SearchLog

from ..tests            import dSearchResult # in __init__.py
from ..tests            import ( sExampleResponse, sBrands, sModels,
                                 sResponseItems2Test )
from ..utils_test       import getItemHitsLog, updateHitLogFile
from ..utils_stars      import getFoundItemTester, findSearchHits
from ..utils            import ( storeSearchResultsInFinders,
                                 _putPageNumbInFileName,
                                 trySearchCatchExceptStoreInFile,
                                 getSearchIdStr,
                                 _storeUserItemFound, _storeItemFound )

from ..utilsearch       import ( getJsonFindingResponse, getSuccessOrNot,
                                 ItemAlreadyInTable,
                                 getPagination, _getFindingResponseGenerator,
                                 getSearchResultGenerator )

from brands.models      import Brand
from categories.models  import Category, BrandCategory
from models.models      import Model

from finders.models     import ItemFound, UserItemFound, ItemFoundTemp

from pyPks.Dict.Maintain import getDictValuesFromSingleElementLists
from pyPks.File.Del      import DeleteIfExists
from pyPks.File.Spec     import getPathNameExt
from pyPks.File.Test     import isFileThere
from pyPks.File.Write    import QuietDump
from pyPks.String.Get    import getTextBefore
from pyPks.Time.Delta    import getDeltaDaysFromStrings
from pyPks.Time.Test     import isISOdatetime
from pyPks.Utils.Config  import getBoolOffYesNoTrueFalse


logger = logging.getLogger(__name__)
logging_level = logging.INFO

'''
this will print logging messages to the terminal
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)
'''

def getB( sSomething ):
    #
    bReturn = False
    #
    if sSomething:
        #
        bReturn = getBoolOffYesNoTrueFalse( sSomething )
        #
    #
    return bReturn


sExampleFile = '/tmp/search_results_____0_.json'

class getImportSearchResultsTests( TestCasePlus ):
    #
    def test_get_search_results(self):
        '''test readin an example search results file'''
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        QuietDump( sExampleResponse, SEARCH_FILES_FOLDER, sExampleFile )
        #
        itemResultsIterator = getSearchResultGenerator( sExampleFile, 0 )
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
        dThisItem = next( itemResultsIterator )
        #
        dPrimaryCategory= dThisItem["primaryCategory"]
        self.assertEqual( dPrimaryCategory["categoryId"  ], "64627"       )
        self.assertEqual( dPrimaryCategory["categoryName"], "Vintage Tubes & Tube Sockets" )
        #
        dSecondyCategory= dThisItem["secondaryCategory"]
        self.assertEqual( dSecondyCategory["categoryId"  ], "80741"       )
        self.assertEqual( dSecondyCategory["categoryName"], "Radio & Speaker Systems" )
        #
        iItems = 2
        #
        for dThisItem in itemResultsIterator:
            #
            iItems += 1
            #
        #
        self.assertEqual( iItems, 5 )
        #
        # DeleteIfExists( SEARCH_FILES_FOLDER, sExampleFile )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



'''
['id',
 'iCategoryID',
 'name',
 'iLevel',
 'iParentID',
 'bLeafCategory',
 'iTreeVersion',
 'iEbaySiteID_id',
 'iSupercededBy',
 'lft',
 'rght',
 'tree_id',
 'level',
 'parent_id']
'''


class storeItemFoundTests( GetEbayCategoriesWebTestSetUp ):
    #
    ''' class for testing _storeItemFound() '''

    def test_store_ebay_categories(self):
        #
        ''' testing the ebay item categories '''
        #
        from ebayinfo.tests import sCategoryDump
        #
        iTableCount = EbayCategory.objects.all().count()
        #
        oTableIter = getTableFromScreenCaptureGenerator( sCategoryDump )
        #
        lHeader = next( oTableIter )
        #
        iExpect = 3 # GetEbayCategoriesWebTestSetUp above adds root categories
        #
        for lParts in oTableIter: iExpect += 1
        #
        oCategories = EbayCategory.objects.all()
        #
        self.assertEqual( iExpect, iTableCount )
        #
        oMultimeters = EbayCategory.objects.get( iCategoryID = 58277 )
        #
        self.assertEqual(
                str( oMultimeters ),
                'Multimeters' )
        #
        self.assertEqual(
                str( oMultimeters.parent ),
                'Electric Circuit & Multimeters' )
        #
        self.assertEqual(
                str( oMultimeters.parent.parent ),
                'Test Meters & Detectors' )
        #
        self.assertEqual(
                str( oMultimeters.parent.parent.parent ),
                'Test, Measurement & Inspection' )
        #
        self.assertEqual(
                str( oMultimeters.parent.parent.parent.parent ),
                'Electrical & Test Equipment' )
        #
        self.assertEqual(
                str( oMultimeters.parent.parent.parent.parent.parent ),
                'Business & Industrial' )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
        #
        #logger.info("class storeItemFoundTests")


    def test_get_ebay_category_hierarchy(self):
        #
        ''' test getEbayCategoryHierarchies() retrieval & caching '''
        #
        dEbayCatHierarchies = {}
        #
        iCategoryID = int(
                dSearchResult.get( 'primaryCategory' ).get( 'categoryId' ) )
        #
        t = getEbayCategoryHierarchies(
                            dSearchResult, dEbayCatHierarchies )
        #
        iCatHeirarchy, i2ndCatHeirarchy = t
        #
        iEbaySiteUS = dMarket2SiteID.get( dSearchResult.get( 'globalId' ) )
        #
        oCatHierarchy = CategoryHierarchy.objects.get(
            iCategoryID = iCategoryID,
            iEbaySiteID = iEbaySiteUS )
        #
        lExpect = [ 'Business & Industrial',
                    'Electrical & Test Equipment',
                    'Test, Measurement & Inspection',
                    'Test Meters & Detectors',
                    'Capacitance & ESR Meters' ]
        #
        sExpect = ', '.join( lExpect )
        #
        self.assertEqual( oCatHierarchy.cCatHierarchy, sExpect )
        #
        dExpect = { (iCategoryID, iEbaySiteUS) : oCatHierarchy.id }
        #
        self.assertEqual( dEbayCatHierarchies, dExpect )
        #
        # try again
        #
        lOrigCatHeirarchy = dEbayCatHierarchies[ (iCategoryID, iEbaySiteUS) ]
        #
        lCatHeirarchy = getEbayCategoryHierarchies(
                            dSearchResult, dEbayCatHierarchies )
        #
        self.assertIs(
            dEbayCatHierarchies[ (iCategoryID, iEbaySiteUS) ], lOrigCatHeirarchy )

        # try again a 3rd time
        #
        dEbayCatHierarchiesNew = {}
        #
        t = getEbayCategoryHierarchies(
                            dSearchResult, dEbayCatHierarchiesNew )
        #
        iCatHeirarchy, i2ndCatHeirarchy = t
        #
        lNewCatHeirarchy = dEbayCatHierarchiesNew[ (iCategoryID, iEbaySiteUS) ]
        #
        lCatHeirarchy = getEbayCategoryHierarchies(
                            dSearchResult, dEbayCatHierarchiesNew )
        #
        self.assertIsNot( dEbayCatHierarchies, dEbayCatHierarchiesNew )
        #
        self.assertEqual( lNewCatHeirarchy, lOrigCatHeirarchy )
        #
        self.assertEqual( dEbayCatHierarchies, dEbayCatHierarchiesNew )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
        #
        #logger.info("class storeItemFoundTests")




    def test_store_item_found(self):
        #
        ''' test _storeItemFound() with actual record'''
        #
        dEbayCatHierarchies = {}
        #
        iItemNumb = _storeItemFound( dSearchResult, dEbayCatHierarchies )
        #
        iCategoryID = int(
                dSearchResult.get( 'primaryCategory' ).get( 'categoryId' ) )
        #
        iEbaySiteID = dMarket2SiteID.get( dSearchResult.get( 'globalId' ) )
        #
        iCatHeirarchy = CategoryHierarchy.objects.get(
                            iCategoryID = iCategoryID,
                            iEbaySiteID = iEbaySiteID ).pk
        #
        self.assertEqual( dEbayCatHierarchies,
                          { ( iCategoryID, iEbaySiteID ) : iCatHeirarchy } )
        #
        oResultRow = ItemFound.objects.filter(
                            iItemNumb = int(
                                    dSearchResult['itemId'] ) ).first()
        #
        self.assertIsNotNone( oResultRow )
        #
        self.assertEqual( oResultRow.iItemNumb,
                         int( dSearchResult['itemId'] ) )
        #
        self.assertEqual( iItemNumb, oResultRow.pk )
        #
        oExpectHierarchy = CategoryHierarchy.objects.get(
                iCategoryID = iCategoryID,
                iEbaySiteID = iEbaySiteID )
        #
        sExpect = oExpectHierarchy.cCatHierarchy
        #
        #self.assertEqual( oResultRow.iCatHeirarchy.cCatHierarchy, sExpect )
        #
        try: # again
            _storeItemFound( dSearchResult )
        except ItemAlreadyInTable as e:
            self.assertEqual(
                    str(e),
                    'ItemID %s is already in the ItemFound table' %
                    dSearchResult['itemId'] )
        else:
            self.assertTrue( False ) # exception should hve been raised
        #
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
        #
        #logger.info("class storeItemFoundTests")



class storeUserItemFoundButDontWebTestYet( GetEbayCategoriesWebTestSetUp ):
    #
    ''' class for testing _storeUserItemFound() '''

    def setUp( self ):
        #
        '''set up to test _storeUserItemFound() with actual record'''
        #
        super( storeUserItemFoundButDontWebTestYet, self ).setUp()
        #
        class ThisShouldNotBeHappening( Exception ): pass
        #
        for oUser in self.tUsers:
            #
            sSearch         = "My clever search 1"
            self.oSearch    = Search( cTitle= sSearch, iUser = oUser )
            self.oSearch.save()
            #
            tNow = timezone.now()
            #
            try:
                iItemNumb = _storeItemFound( dSearchResult, {} )
            except ItemAlreadyInTable:
                iItemNumb = int( dSearchResult['itemId' ] )
            #
            if iItemNumb is None:
                raise ThisShouldNotBeHappening
            #
            try:
                _storeUserItemFound(
                    dSearchResult, iItemNumb, oUser, self.oSearch.id )
            except ItemAlreadyInTable:
                pass
            #
            self.iItemNumb  = iItemNumb
            self.tNow       = tNow
            #


class storeUserItemFoundTests( storeUserItemFoundButDontWebTestYet ):
    #
    ''' class for testing _storeUserItemFound() '''

    def test_Auction_bool_set_correctly( self ):
        #
        ''' test _storeUserItemFound() with actual record, check bAuction'''
        #
        oUserItemFound = UserItemFound.objects.filter(
                            iItemNumb = self.iItemNumb ).first()
        #
        self.assertTrue( oUserItemFound.bAuction )


    def test_store_User_item_found(self):
        #
        ''' test _storeUserItemFound() with actual record'''
        #
        iItemNumb   = self.iItemNumb
        #
        for oUser in self.tUsers:
            #
            oResultRow = UserItemFound.objects.filter(
                                iItemNumb   = iItemNumb,
                                iUser       = oUser ).first()
            #
            self.assertIsNotNone( oResultRow )
            #
            try: # again
                _storeUserItemFound(
                    dSearchResult, iItemNumb, oUser, self.oSearch.id )
            except ItemAlreadyInTable as e:
                self.assertEqual(
                        str(e),
                        'ItemFound %s is already in the UserItemFound table for %s' %
                        ( iItemNumb, oUser.username ) )
            else:
                self.assertTrue( False ) # exception should have been raised
            #
            #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
            #
            oItem = ItemFound.objects.get( iItemNumb   = iItemNumb )
            #
            self.assertIsNotNone( oItem )
            #
            self.assertIsNotNone( oItem.cGalleryURL )
            #



class StoreSearchResultsTestsWebTestSetUp( GetEbayCategoriesWebTestSetUp ):
    #
    ''' class for testing storeSearchResultsInFinders() store records '''
    #
    def setUp(self):
        #
        super( StoreSearchResultsTestsWebTestSetUp, self ).setUp()
        #
        sSearch = "My clever search 1"
        oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        #
        self.oSearch = oSearch
        #
        self.sMarket = 'EBAY-US'
        #
        self.sExampleFile = (
            RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
                ( self.sMarket,
                   self.user1.username,
                   getSearchIdStr( oSearch.id ),
                   '000' ) )
        #
        QuietDump( sExampleResponse, SEARCH_FILES_FOLDER, self.sExampleFile )
        #
        tNow    = timezone.now()
        tBefore = tNow - timezone.timedelta( minutes = 5 )
        #
        oSearchLog = SearchLog(
                iSearch_id  = self.oSearch.id,
                tBegSearch  = tBefore,
                tEndSearch  = tNow,
                cResult     = 'Success' )
        #
        oSearchLog.save()
        #
        self.oSearchLog = oSearchLog
        #
        self.t = storeSearchResultsInFinders(
                    self.oSearchLog.id,
                    self.sMarket,
                    self.user1.username,
                    self.oSearch.id,
                    self.oSearch.cTitle,
                    self.setTestCategories,
                    bCleanUpFiles = False )
        #

    def tearDown(self):
        #
        DeleteIfExists( SEARCH_FILES_FOLDER, self.sExampleFile )


class storeSearchResultsWebTests( StoreSearchResultsTestsWebTestSetUp ):
    #

    def test_store_search_results(self):
        #
        ''' test storeSearchResultsInFinders() with actual record'''
        #
        #print('')
        #print( 'self.oSearch.id:', self.oSearch.id )
        #
        iCountItems, iStoreItems, iStoreUsers = self.t
        #
        self.assertEqual( ItemFound.objects.count(), iCountItems )
        self.assertEqual( ItemFound.objects.count(), iStoreItems )
        #
        self.assertEqual( UserItemFound.objects.count(), iStoreUsers )
        #
        oSearchLogs = SearchLog.objects.all()
        #
        self.assertEqual( len( oSearchLogs ), 1 )
        #
        oSearchLog = oSearchLogs[0]
        #
        sBeforeDash = getTextBefore( str(oSearchLog), ' -' )
        #
        self.assertTrue( isISOdatetime( sBeforeDash ) )
        #
        self.assertEqual( oSearchLog.iItems,      5 )
        self.assertEqual( oSearchLog.iStoreItems, 5 )
        self.assertEqual( oSearchLog.iStoreUsers, 5 )
        #
        # try again with the same data
        #
        t = ( storeSearchResultsInFinders(
                        self.oSearchLog.id,
                        self.sMarket,
                        self.user1.username,
                        self.oSearch.id,
                        self.oSearch.cTitle,
                        self.setTestCategories ) )
        #
        iCountItems, iStoreItems, iStoreUsers = t
        #
        self.assertEqual( ItemFound.objects.count(), iCountItems )
        #
        self.assertEqual( iStoreItems, 0 )
        #
        self.assertEqual( iStoreUsers, 0 )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )




class GetBrandsCategoriesModelsWebTestSetUp( StoreSearchResultsTestsWebTestSetUp ):
    #
    ''' base class for testing trySearchCatchExceptStoreInFile() &
    storeSearchResultsInFinders() store records '''
    #

    def setUp(self):
        #
        super( GetBrandsCategoriesModelsWebTestSetUp, self ).setUp()
        #
        for oUser in self.tUsers:
            #
            sSearch = "Catalin Radios"
            sKeyWords = 'catalin radio'
            #
            if Search.objects.filter(
                    cKeyWords = sKeyWords,
                    iUser = oUser ).exists():
                #
                self.oCatalinSearch = Search.objects.filter(
                                        cKeyWords = sKeyWords,
                                        iUser = oUser ).first()
                #
            else:
                #
                self.oCatalinSearch = Search(
                                cTitle      = sSearch,
                                cKeyWords   = sKeyWords,
                                iUser       = oUser )
                #
                self.oCatalinSearch.save()
                #
            #
            sSearch         = 'Tube Preamps'
            iEbayCategory   = 67807
            #
            if Search.objects.filter(
                    cTitle = sSearch,
                    iUser = oUser  ).exists():
                #
                self.oPreampSearch = Search.objects.filter(
                                        cTitle = sSearch,
                                        iUser = oUser ).first()
                #
            else:
                #
                oEbayCateID = EbayCategory.objects.get(
                        name = 'Vintage Preamps & Tube Preamps' )
                #
                self.oPreampSearch = Search(
                                cTitle          = sSearch,
                                iEbayCategory   = oEbayCateID,
                                iUser           = oUser )
                #
                self.oPreampSearch.save()
                #
            #
            oCategory   = Category( cTitle      = 'Radio',
                                    iStars      = 9,
                                    cExcludeIf  = 'reproduction',
                                    iUser       = oUser )
            oCategory.save()
            #
            #
            oCategory   = Category( cTitle      = 'Stereo System',
                                    iStars      = 3,
                                    iUser       = oUser )
            oCategory.save()
            #
            oStereoSystem = oCategory
            #
            #
            oCategory   = Category( cTitle      = 'Preamp',
                                    cLookFor    = 'preamplifier\r'
                                                  'master control\rpre amp',
                                    iStars      = 9,
                                    iFamily_id  = oStereoSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            #
            oCategory   = Category( cTitle      = 'Vacuum Tube',
                                    cLookFor    = 'tube\rtubes\rVintage Tubes',
                                    cExcludeIf  = 'tube radio\r'
                                                   'tube clock radio\r'
                                                   'tube portable radio',
                                    iStars      = 6,
                                    iUser       = oUser )
            oCategory.save()
            #
            oVacuumTubes = oCategory
            #
            oCategory   = Category( cTitle      = 'Book',
                                    cLookFor    = 'tube\rtubes',
                                    cExcludeIf  = 'book shelf\rdigital',
                                    iStars      = 5,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Speaker System',
                                    cLookFor    = 'speaker',
                                    iFamily_id  = oStereoSystem.id,
                                    iStars      = 9,
                                    iUser       = oUser )
            oCategory.save()
            #
            oSpeakerSystem = oCategory
            #
            oCategory.iFamily_id                = oCategory.id
            #
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Driver',
                                    cLookFor    = 'speaker\rdrive\rwoofer',
                                    iStars      = 8,
                                    iFamily_id  = oSpeakerSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Crossover',
                                    iStars      = 7,
                                    cLookFor    = 'X-Over\rdividing network\rxover',
                                    iFamily_id  = oSpeakerSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Amplifier',
                                    cLookFor    = 'amp',
                                    cExcludeIf  = 'Table Radio\rPre-amplifier\r'
                                                'Pre-amp\rFuse Holder\rCapacitor',
                                    iStars      = 10,
                                    iFamily_id  = oStereoSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Horn',
                                    iStars      = 6,
                                    iFamily_id  = oSpeakerSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Tuner',
                                    iStars      = 8,
                                    iFamily_id  = oStereoSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Tube Tester',
                                    iStars      = 8,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Choke',
                                    cLookFor    = 'crossover',
                                    iStars      = 7,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Output Transformer',
                                    cLookFor    = 'Transformer\rTranformer',
                                    iStars      = 6,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category(
                    cTitle      = 'Speaker Enclosure',
                    cLookFor    = 'Enclosure\rcabinet\rspeaker cabinet',
                    iStars      = 7,
                    iFamily_id  = oSpeakerSystem.id,
                    iUser       = oUser )
            #
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Accessory',
                                    cLookFor    = 'adaptor\radapter',
                                    iStars      = 5,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category(
                    cTitle      = 'Integrated Amp',
                    cLookFor    = 'Amp\rAmplifier',
                                    iStars      = 4,
                                    iUser       = oUser )
            oCategory.save()
            #
            #
            oCategory   = Category(
                    cTitle      = 'Theater Amp',
                    cLookFor    = 'Amp\rAmplifier',
                                    iStars      = 9,
                                    iUser       = oUser )
            oCategory.save()
            #
            #
            oTableIter = getTableFromScreenCaptureGenerator( sBrands )
            #
            lHeader = next( oTableIter )
            #
            d = getNamePositionDict( lHeader )
            #
            for lParts in oTableIter:
                #
                oBrand = Brand(
                    cTitle      =      lParts[ d['cTitle'    ] ],
                    iStars      = int( lParts[ d['iStars'    ] ] ),
                    cExcludeIf  =      lParts[ d['cExcludeIf'] ],
                    cLookFor    =      lParts[ d['cLookFor'  ] ],
                    iUser       = oUser )
                #
                oBrand.save()
                #
            #
            oTableIter = getTableFromScreenCaptureGenerator( sModels )
            #
            lHeader = next( oTableIter )
            #
            d = getNamePositionDict( lHeader )
            #
            iHeaderLen = len( lHeader )
            #
            for lParts in oTableIter:
                #
                if len( lParts ) < iHeaderLen:
                    #
                    lRest = lHeader[ len( lParts ) : ]
                    #
                    for sHead in lRest:
                        #
                        if sHead.startswith( 'b' ):
                            #
                            lParts.append( 'f' ) # for getBoolOffYesNoTrueFalse()
                            #
                        else:
                            #
                            lParts.append( '' )
                            #
                        #
                    #
                #
                sBrand    = lParts[ d['Brand'   ] ]
                sCategory = lParts[ d['Category'] ]
                #
                if sBrand:
                    #
                    bHaveBrand = Brand.objects.filter(
                                    cTitle = sBrand,
                                    iUser = oUser ).exists()
                    #
                    if bHaveBrand:
                        #
                        oBrand = Brand.objects.filter(
                                    cTitle = sBrand,
                                    iUser = oUser )
                        #
                        if len( oBrand ) > 1:
                            print( '' )
                            print( 'got more than one brand %s' % sBrand )
                        #
                        oBrand = oBrand.first()
                        #
                    else:
                        #
                        print( '' )
                        print( 'do not have brand %s' % sBrand )
                        oBrand = None
                        #
                else: # not sBrand, blank, generic model
                    #
                    oBrand = None
                    #
                #
                try:
                    oCategory = Category.objects.get(
                                    cTitle = sCategory,
                                    iUser = oUser )
                except ObjectDoesNotExist:
                    if sCategory and sBrand:
                        print( 'not finding category %s for %s!' %
                            ( sCategory, sBrand ) )
                    elif sBrand:
                        print(
                            "need a category but ain't got one! (do got brand %s)" % sBrand )
                    else:
                        print(
                            "supposed to have a brand & category here "
                            "but ain't got nothin!" )
                    raise
                #
                oModel = Model(
                    cTitle          =       lParts[ d['cTitle'        ] ],
                    cKeyWords       =       lParts[ d['cKeyWords'     ] ],
                    iStars          = int(  lParts[ d['iStars'        ] ] ),
                    bSubModelsOK    = getB( lParts[ d['bSubModelsOK'  ] ] ),
                    cLookFor        =       lParts[ d['cLookFor'      ] ],
                    cExcludeIf      =       lParts[ d['cExcludeIf'    ] ],
                    bGenericModel   = getB( lParts[ d['bGenericModel' ] ] ),
                    bMustHaveBrand  = getB( lParts[ d['bMustHaveBrand'] ] ),
                    iBrand          = oBrand,
                    iCategory       = oCategory,
                    iUser           = oUser )
                #
                oModel.save()
                #
            #
            oBrand = Brand.objects.get( cTitle = 'GE', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'RCA', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Philips', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Tung-Sol', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Mullard', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Mazda', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Raytheon', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Sylvania', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Marconi', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Matsushita', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Westinghouse', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Amperex Bugle Boy', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Amperex', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #


    def test_generic_model_OK( self ):
        #
        oModel = Model.objects.get(
                        cTitle = '6L6WGB',
                        iUser  = self.user1 )
        #
        self.assertTrue( oModel.bGenericModel )


class DoSearchStoreResultsTests( GetBrandsCategoriesModelsWebTestSetUp ):
    #
    ''' class for testing trySearchCatchExceptStoreInFile() &
    storeSearchResultsInFinders() store records '''
    #
    def setUp( self ):
        #
        sThisFilePath, sName, sExt = getPathNameExt( realpath(__file__) )
        #
        self.sPathHere   = sThisFilePath
        #
        self.sHitLogFile = join( sThisFilePath, 'ItemHitsLog.log' )
        #
        super( DoSearchStoreResultsTests, self ).setUp()

    def test_already_stored_results( self ):
        #
        '''test whether it has been a while since running the ebay API tests,
        if it has been a while (mmore than 1 month), prompt to run soon
        so the list of actual item numbers can stay current enough'''
        #
        lItemHits = getItemHitsLog( self.sHitLogFile )
        #
        # list is sorted with the oldest on top, newest at bottom
        #
        sLastAuctionEndDate = lItemHits[ -1 ][ 'tTimeEnd' ]
        #
        iDaysFromNow = - getDeltaDaysFromStrings( sLastAuctionEndDate )
        #
        sSayLastEnd = ''
        #
        if iDaysFromNow >= 2:
            sSayLastEnd = ( 'last auction end date '
                            'is about %s days from now' % iDaysFromNow )
        elif iDaysFromNow == 1:
            sSayLastEnd = 'last auction end date is tomorrow'
        elif iDaysFromNow == 0:
            sSayLastEnd = 'last auction end date is TODAY!!!!'
        #
        if sSayLastEnd:
            print( '' )
            print( sSayLastEnd )
        #
        self.assertGreater( iDaysFromNow, 0,
                    msg = 'got no future auction end dates, API test is WAY OVERDUE!' )
        #


    @tag('ebay_api') # pmt script has exclude-tag param, excludes this test
    def test_key_word_only_search_store_results( self ):
        #
        '''test key words only search
        not only test store results, add to the log of actual item numbers
        which will be used later for testing getting the auction results'''
        #
        # sandbox returns 0 items, can use it to test for 0 items
        #
        oSearch = self.oCatalinSearch
        #
        # tBegSearch is set when the search begins - not yet
        #
        iSearchID = oSearch.id
        #
        sLastFile = trySearchCatchExceptStoreInFile( iSearchID )
        #
        oSearch.refresh_from_db() # this is necessary to get the updated object!
        #
        iSearchID = oSearch.id    # refresh_from_db() wipes this!
        #
        iLogID = SearchLog.objects.get(
                    iSearch     = oSearch,
                    tBegSearch  = oSearch.tBegSearch ).id
        #
        sSearchName = oSearch.cTitle
        sUserName   = oSearch.iUser.username
        sMarket     = oSearch.iUser.iEbaySiteID.cMarket
        #
        t = storeSearchResultsInFinders(
                    iLogID,
                    sMarket,
                    sUserName,
                    iSearchID,
                    sSearchName,
                    self.setTestCategories,
                    bDoNotMentionAny = True )
        #
        iItems, iStoreItems, iStoreUsers = t
        #
        self.assertTrue( iItems and iStoreItems and iStoreUsers )
        #
        if iItems and iStoreItems and iStoreUsers: # > 0 each
            #
            iBegLines = 1
            #
            if isFileThere( self.sHitLogFile ):
                #
                iBegLines = len( getItemHitsLog( self.sHitLogFile ) )
            #
            findSearchHits( iUser = self.user1.id )
            #
            oUserItems = UserItemFound.objects.filter(
                            iUser          = self.user1,
                            iHitStars__gte = 100 )
            #
            iLen = len( oUserItems )
            #
            if iLen > 0: # add to list of items to test fetching the results
                #
                iBegRows, iEndRows = updateHitLogFile(
                                        oUserItems, self.sPathHere )
                #
            #
            iEndLines = len( getItemHitsLog( self.sHitLogFile ) )
            #
            if iBegLines + max( iLen, 5 ) < iEndLines:
                #
                print()
                print( 'iBegLines:', iBegLines )
                print( 'iLen     :', iLen      )
                print( 'iEndLines:', iEndLines )
                #
            self.assertGreaterEqual( iBegLines + max( iLen, 5 ), iEndLines )

        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    @tag('ebay_api') # pmt script has exclude-tag param, excludes this test
    def test_category_only_search_store_results( self ):
        #
        '''test category only search
        not only test store results, add to the log of actual item numbers
        which will be used later for testing getting the auction results'''
        #
        # sandbox returns 0 items, can use it to test for 0 items
        #
        oSearch = self.oPreampSearch
        #
        iSearchID = oSearch.id
        #
        sLastFile = trySearchCatchExceptStoreInFile( iSearchID )
        #
        oSearch.refresh_from_db() # this is necessary to get the updated object!
        #
        iSearchID = oSearch.id    # refresh_from_db() wipes this!
        #
        iLogID = SearchLog.objects.get(
                    iSearch     = oSearch,
                    tBegSearch  = oSearch.tBegSearch ).id
        #
        sSearchName = oSearch.cTitle
        sUserName   = oSearch.iUser.username
        sMarket     = oSearch.iUser.iEbaySiteID.cMarket
        #
        t = storeSearchResultsInFinders(
                iLogID,
                sMarket,
                sUserName,
                iSearchID,
                sSearchName,
                self.setTestCategories,
                bDoNotMentionAny = True )
        #
        iItems, iStoreItems, iStoreUsers = t
        #
        self.assertTrue( iItems and iStoreItems and iStoreUsers )
        #
        if iItems and iStoreItems and iStoreUsers: # > 0 each
            #
            iBegLines = 1
            #
            if isFileThere( self.sHitLogFile ):
                #
                iBegLines = len( getItemHitsLog( self.sHitLogFile ) )
            #
            findSearchHits( iUser = self.user1.id )
            #
            oUserItems = UserItemFound.objects.filter(
                            iUser          = self.user1,
                            iHitStars__gte = 200 )
            #
            iLen = len( oUserItems )
            #
            if iLen > 0: # add to list of items to test fetching the results
                #
                iBegRows, iEndRows = updateHitLogFile(
                                        oUserItems, self.sPathHere )
                #
            #
            iEndLines = len( getItemHitsLog( self.sHitLogFile ) )
            #
            self.assertGreaterEqual( iBegLines + min( iLen, 8 ), iEndLines )

        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


class TestFindingResponseHelpers( TestCasePlus ):
    #
    '''test the nifty finding response info extractors'''

    def test_get_pagination( self ):
        #
        ''' test getPagination() '''
        #
        dGot = getPagination( sResponseItems2Test )
        #
        dExpect = { 'iPageCount'    :  100,
                    'iTotalEntries' : 2374,
                    'iEntriesPP'    :  100,
                    'iPageNumb'     :    1,
                    'iPages'        :   24 }

        #
        self.assertEqual( dGot, dExpect )
        #
        dGot = getPagination( '' )
        #
        self.assertNotEquals( dGot, dExpect )

    def test_get_success_or_not( self ):
        #
        ''' test getSuccessOrNot() '''
        #
        self.assertTrue(  getSuccessOrNot( sResponseItems2Test ) )
        self.assertFalse( getSuccessOrNot( '' ) )




def getResultGeneratorTheJsonWay():
    #
    dResponse       = getJsonFindingResponse( sResponseItems2Test )
    #
    dPagination     = dResponse[  'dPagination']
    #
    iTotalEntries   = dPagination['iTotalEntries'   ]
    #
    iPages          = dPagination['iPages'     ]
    #
    dResultDict     = dResponse[ "searchResult" ][0]
    #
    iThisItem = 0
    #
    lResults = dResultDict.get('item')
    #
    for dItem in lResults:
        #
        iThisItem += 1
        #
        getDictValuesFromSingleElementLists( dItem )
        #
        dPagination["thisEntry"] = str( iThisItem )
        #
        dItem["paginationOutput"]= dPagination
        #
        yield dItem


def getConsumedJsonItems():
    #
    oIterItems = getResultGeneratorTheJsonWay()
    #
    for dItem in oIterItems:
        #
        pass


def getResultGeneratorMyWay():
    #
    getSuccessOrNot( sResponseItems2Test )
    getPagination( sResponseItems2Test )
    #
    return _getFindingResponseGenerator( sResponseItems2Test )


def getConsumedMyWayItems():
    #
    oIterItems = getResultGeneratorMyWay()
    #
    for dItem in oIterItems:
        #
        pass


def getJsonPagination():
    #
    oIterItemsJson  = getResultGeneratorTheJsonWay()
    #
    dItem = next( oIterItemsJson )
    #
    dJsonPage = dItem["paginationOutput"]



def getOnlyPagination():
    #
    dOnlyPage = getPagination( sResponseItems2Test )



class DoTimeTrialBetweenJsonLoadAndMechanicalWay( TestCasePlus ):
    '''do a time trial, compare loading & using Json load with home brew job'''

    def name_must_start_with_test_to_do_time_trial( self ):
        #
        from pyPks.Utils.TimeTrial import TimeTrial
        #
        print( '' )
        print( 'using getJsonFindingResponse ...' )
        #
        iCallsPerSet, iSets = TimeTrial( getJsonPagination )
        #
        print( '' )
        print( 'using my way ...' )
        #
        TimeTrial( getOnlyPagination,
              iCallsPerSet=iCallsPerSet, iSets=iSets)
        #
        # my way takes less than 1/10 the time


    def test_pagination_info( self ):
        #
        oIterItemsJson  = getResultGeneratorTheJsonWay()
        #
        dItem = next( oIterItemsJson )
        #
        dPageJ = dItem["paginationOutput"]
        #
        dOnlyPage = getPagination( sResponseItems2Test )
        #
        self.assertEqual( dPageJ["iEntriesPP"],    dOnlyPage["iPageCount"] )
        self.assertEqual( dPageJ["iTotalEntries"], dOnlyPage["iTotalEntries"])
        self.assertEqual( dPageJ["iPages"],        dOnlyPage["iPages"    ] )
        self.assertEqual( dPageJ["iEntriesPP"],    dOnlyPage["iEntriesPP"] )
        self.assertEqual(
                      int( dPageJ["pageNumber"]),  dOnlyPage["iPageNumb" ]  )


    def test_get_same_item_info( self ):
        #
        oIterItemsMyWay = getResultGeneratorMyWay()
        oIterItemsJson  = getResultGeneratorTheJsonWay()
        #
        dItemMyWay   = next( oIterItemsMyWay )
        dItemJsonWay = next( oIterItemsJson )
        #
        self.assertEqual( dItemMyWay["itemId"],
                                dItemJsonWay["itemId"] )
        self.assertEqual( dItemMyWay["listingInfo"],
                                dItemJsonWay["listingInfo"] )
        self.assertEqual( dItemMyWay["primaryCategory"],
                                dItemJsonWay["primaryCategory"] )
        self.assertEqual( dItemMyWay["condition"],
                                dItemJsonWay["condition"] )
        self.assertEqual( dItemMyWay["sellingStatus"],
                               dItemJsonWay["sellingStatus"] )


class FileNameUtilitiesTesting( TestCasePlus ):
    '''test the file naming utilities'''

    def test_put_number_in_file_name( self ):
        #
        sExampleFile = (
                RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
                ( 'EBAY-US', 'oUserOne', getSearchIdStr( 10 ), '000' ) )

        sNewFileName = _putPageNumbInFileName( sExampleFile, 1 )
        #
        lParts = sNewFileName.split( '_' )
        #
        self.assertEqual( lParts[6], '001' )






'''
will need later
        iWantOlderThan = 100
        #
        oSearch = ItemFound( cTitle = self.sTitle1, iItemNumb = self.iItemID1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan -2 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        oSearch = ItemFound( cTitle = self.sTitle2, iItemNumb = self.iItemID2 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan - 9 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        oSearch = ItemFound( cTitle = self.sTitle3, iItemNumb = self.iItemID3 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan + 2 )
        oSearch.tCreate = dDropDead
        oSearch.save()


        #
        iItemID1 = 2823
        oSearch = UserItemFound( iItemNumb = iItemID1, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan -2 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        iItemID2 = 2418
        oSearch = UserItemFound( iItemNumb = iItemID2, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan + 1 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        iItemID3 = 2607
        oSearch = UserItemFound( iItemNumb = iItemID3, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan + 2 )
        oSearch.tCreate = dDropDead
        oSearch.save()

'''

