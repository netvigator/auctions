import inspect
import logging

from os.path            import realpath, join
from datetime           import timedelta

from django.test        import TestCase, tag
from django.utils       import timezone
from core.utils_test    import ( BaseUserTestCase, getDefaultMarket,
                                 getEbayCategoriesSetUp,
                                 getTableFromScreenCaptureGenerator,
                                 getNamePositionDict )

from ebayinfo.models    import EbayCategory, CategoryHierarchy
from ebayinfo.utils     import dMarket2SiteID, getEbayCategoryHierarchies
#

from searching          import RESULTS_FILE_NAME_PATTERN

from ..models           import ( Search, ItemFound, UserItemFound,
                                 ItemFoundTemp, SearchLog )

from ..tests            import dSearchResult # in __init__.py
from ..tests            import ( sExampleResponse, sBrands, sModels,
                                 sResponseSearchTooBroad )
from ..utils_test       import getItemHitsLog, updateHitLogFile
from ..utils_stars      import ( getFoundItemTester,
                                 _getBrandRegExFinders4Test,
                                 _getCategoryRegExFinders4Test,
                                 findSearchHits )
from ..utils            import ( storeSearchResultsInDB,
                                 ItemAlreadyInTable,
                                 _putPageNumbInFileName,
                                 trySearchCatchExceptStoreInFile,
                                 getSearchIdStr,
                                 _storeUserItemFound, _storeItemFound )

from ..utilsearch       import ( getJsonFindingResponse, getSuccessOrNot,
                                 getPagination, _getFindingResponseGenerator,
                                 getSearchResultGenerator )

#

from brands.models      import Brand
from categories.models  import Category
from models.models      import Model

from File.Del           import DeleteIfExists
from File.Spec          import getPathNameExt
from File.Test          import isFileThere
from File.Write         import QuietDump
from String.Get         import getTextBefore
from Time.Delta         import getDeltaDaysFromStrings
from Time.Test          import isISOdatetime
from Utils.Config       import getBoolOffYesNoTrueFalse as getB

#logging_level = logging.INFO
#logging.basicConfig(level=logging.DEBUG)

'''
this will print logging messages to the terminal
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)
'''


sExampleFile = '/tmp/search_results.json'

class getImportSearchResultsTests(TestCase):
    #
    def test_get_search_results(self):
        '''test readin an example search results file'''
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        QuietDump( sExampleResponse, sExampleFile )
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
        DeleteIfExists( '/tmp', sExampleFile )
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


class storeItemFoundTests( getEbayCategoriesSetUp ):
    #
    ''' class for testing _storeItemFound() '''

    def test_store_ebay_categories(self):
        #
        ''' testing the ebay item categories '''
        #
        from ebayinfo           import sCategoryDump  # in __init__.py
        #
        iTableCount = EbayCategory.objects.all().count()
        #
        oTableIter = getTableFromScreenCaptureGenerator( sCategoryDump )
        #
        lHeader = next( oTableIter )
        #
        iExpect = 2 # getEbayCategoriesSetUp above adds root categories
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
        #logging.info("class storeItemFoundTests")


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
        sExpect = '\r'.join( lExpect )
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
        #logging.info("class storeItemFoundTests")




    def test_store_item_found(self):
        #
        ''' test _storeItemFound() with actual record'''
        #
        dEbayCatHierarchies = {}
        #
        tNow = timezone.now()
        #
        iItemNumb = _storeItemFound( dSearchResult, tNow, dEbayCatHierarchies )
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
        tNow = timezone.now()
        #
        try: # again
            _storeItemFound( dSearchResult, tNow )
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
        #logging.info("class storeItemFoundTests")



class storeUserItemFoundButDontTestYet( getEbayCategoriesSetUp ):
    #
    ''' class for testing _storeUserItemFound() '''

    def setUp( self ):
        #
        '''set up to test _storeUserItemFound() with actual record'''
        #
        super( storeUserItemFoundButDontTestYet, self ).setUp()
        #
        class ThisShouldNotBeHappening( Exception ): pass
        #
        sSearch         = "My clever search 1"
        self.oSearch    = Search( cTitle= sSearch, iUser = self.user1 )
        self.oSearch.save()
        #
        tNow = timezone.now()
        #
        iItemNumb = _storeItemFound( dSearchResult, tNow, {} )
        #
        if iItemNumb is None:
            raise ThisShouldNotBeHappening
        #
        try:
            _storeUserItemFound(
                dSearchResult, iItemNumb, tNow, self.user1, self.oSearch.id )
        except ItemAlreadyInTable:
            pass
        #
        self.iItemNumb  = iItemNumb
        self.tNow       = tNow


class storeUserItemFoundTests( storeUserItemFoundButDontTestYet ):
    #
    ''' class for testing _storeUserItemFound() '''

    def test_store_User_item_found(self):
        #
        ''' test _storeUserItemFound() with actual record'''
        #
        iItemNumb   = self.iItemNumb
        tNow        = self.tNow
        #
        oResultRow = UserItemFound.objects.filter(
                            iItemNumb   = iItemNumb,
                            iUser       = self.user1 ).first()
        #
        self.assertIsNotNone( oResultRow )
        #
        try: # again
            _storeUserItemFound(
                dSearchResult, iItemNumb, tNow, self.user1, self.oSearch.id )
        except ItemAlreadyInTable as e:
            self.assertEqual(
                    str(e),
                    'ItemFound %s is already in the UserItemFound table for %s' %
                    ( iItemNumb, self.user1.username ) )
        else:
            self.assertTrue( False ) # exception should hve been raised
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



class storeSearchResultsTestsSetUp(getEbayCategoriesSetUp):
    #
    ''' class for testing storeSearchResultsInDB() store records '''
    #
    def setUp(self):
        # storeSearchResultsTests, self 
        #
        super( storeSearchResultsTestsSetUp, self ).setUp()
        #
        sSearch = "My clever search 1"
        oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        #
        self.oSearch = oSearch
        #
        self.sExampleFile = (
            RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
                ( 'EBAY-US',
                   self.user1.username,
                   getSearchIdStr( oSearch.id ),
                   '000' ) )
        #
        QuietDump( sExampleResponse, self.sExampleFile )
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
        self.sMarket = 'EBAY-US'

    def tearDown(self):
        #
        pass # DeleteIfExists( '/tmp', self.sExampleFile )


class storeSearchResultsTests(storeSearchResultsTestsSetUp):
    #
    def test_store_search_results(self):
        #
        ''' test storeSearchResultsInDB() with actual record'''
        #
        t = ( storeSearchResultsInDB(   self.oSearchLog.id,
                                        self.sMarket,
                                        self.user1.username,
                                        self.oSearch.id,
                                        self.oSearch.cTitle ) )
        #
        iCountItems, iStoreItems, iStoreUsers = t
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
        self.assertEqual( oSearchLog.iItems,      4 )
        self.assertEqual( oSearchLog.iStoreItems, 4 )
        self.assertEqual( oSearchLog.iStoreUsers, 4 )
        #
        # try again with the same data
        #
        t = ( storeSearchResultsInDB(   self.oSearchLog.id,
                                        self.sMarket,
                                        self.user1.username,
                                        self.oSearch.id,
                                        self.oSearch.cTitle ) )
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




class GetBrandsCategoriesModelsSetUp(storeSearchResultsTestsSetUp):
    #
    ''' base class for testing trySearchCatchExceptStoreInFile() &
    storeSearchResultsInDB() store records '''
    #
    def setUp(self):
        #
        super( GetBrandsCategoriesModelsSetUp, self ).setUp()
        #
        sSearch = "Catalin Radios"
        sKeyWords = 'catalin radio'
        #
        if Search.objects.filter( cKeyWords = sKeyWords ).exists():
            #
            self.oCatalinSearch = Search.objects.get(
                                    cKeyWords = sKeyWords ).first()
            #
        else:
            #
            self.oCatalinSearch = Search(
                            cTitle      = sSearch,
                            cKeyWords   = sKeyWords,
                            iUser       = self.user1 )
            #
            self.oCatalinSearch.save()
            #
        #
        sSearch         = 'Tube Preamps'
        iEbayCategory   = 67807
        #
        if Search.objects.filter( cTitle = sSearch ).exists():
            #
            self.oPreampSearch = Search.objects.get(
                                    cTitle = sSearch ).first()
            #
        else:
            #
            oEbayCateID = EbayCategory.objects.get(
                    name = 'Vintage Preamps & Tube Preamps' )
            #
            self.oPreampSearch = Search(
                            cTitle          = sSearch,
                            iEbayCategory   = oEbayCateID,
                            iUser           = self.user1 )
            #
            self.oPreampSearch.save()
            #
        #
        oCategory   = Category( cTitle = 'Radio', iStars = 9,
                               cExcludeIf = 'reproduction', iUser = self.user1 )
        oCategory.save()
        #
        #
        oCategory   = Category( cTitle = 'Preamp', iStars = 9,
                                iUser = self.user1 )
        oCategory.save()
        #
        #
        oTableIter = getTableFromScreenCaptureGenerator( sBrands )
        #
        lHeader = next( oTableIter )
        #
        d = getNamePositionDict( lHeader )
        #
        def fRt( s ): return s.replace( r'\\r', '\r' )
        #
        for lParts in oTableIter:
            #
            oBrand = Brand(
                cTitle      =      lParts[ d['cTitle'    ] ],
                iStars      = int( lParts[ d['iStars'    ] ] ),
                cExcludeIf  = fRt( lParts[ d['cExcludeIf'] ] ),
                cLookFor    = fRt( lParts[ d['cLookFor'  ] ] ),
                iUser       = self.user1 )
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
        for lParts in oTableIter:
            #
            sBrand    = lParts[ d['Brand'   ] ]
            sCategory = lParts[ d['Category'] ]
            #
            bHaveBrand = Brand.objects.filter( cTitle = sBrand ).exists()
            #
            if bHaveBrand:
                #
                oBrand = Brand.objects.filter( cTitle = sBrand )
                #
                if len( oBrand ) > 1:
                    print( '' )
                    print( 'got more than one brand %s' % sBrand )
                #
                oBrand = oBrand.first()
                #
            else:
                print( '' )
                print( 'do not have brand %s' % sBrand )
                oBrand = None
            #
            oCategory = Category.objects.get( cTitle = sCategory )
            #
            oModel = Model(
                cTitle      =      lParts[ d['cTitle'       ] ],
                cKeyWords   =      lParts[ d['cKeyWords'    ] ],
                iStars      = int( lParts[ d['iStars'       ] ] ),
                bSubModelsOK= getB(lParts[ d['bSubModelsOK' ] ] ),
                cLookFor    = fRt( lParts[ d['cLookFor'     ] ] ),
                cExcludeIf  = fRt( lParts[ d['cExcludeIf'   ] ] ),
                iBrand      = oBrand,
                iCategory   = oCategory,
                iUser       = self.user1 )
            #
            oModel.save()
            #
        #
        #print( '\n' )
        #print( 'Model.objects.all().count():', Model.objects.all().count() )
        #print( 'ran GetBrandsCategoriesModelsSetUp %s' % inspect.getframeinfo( inspect.currentframe() ).function )
        #



class DoSearchStoreResultsTests(GetBrandsCategoriesModelsSetUp):
    #
    ''' class for testing trySearchCatchExceptStoreInFile() &
    storeSearchResultsInDB() store records '''
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
        lItemHits = getItemHitsLog( open( self.sHitLogFile ) )
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
                    msg = 'auction end dates are all past, API test is WAY OVERDUE!' )
        #


    @tag('ebay_api')
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
        iSearchID = oSearch.id
        #
        sLastFile = trySearchCatchExceptStoreInFile( iSearchID )
        #
        iLogID = SearchLog.objects.get(
                    iSearch     = oSearch,
                    tBegSearch  = oSearch.tBegSearch )
        #
        sSearchName = oSearch.cTitle
        sUserName   = oSearch.iUser.username
        sMarket     = oSearch.iUser.iEbaySiteID.cMarket
        #
        t = storeSearchResultsInDB( iLogID,
                                    sMarket,
                                    sUserName,
                                    iSearchID,
                                    sSearchName )
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
                iBegLines = len( getItemHitsLog( open( self.sHitLogFile ) ) )
            #
            findSearchHits( oUser = self.user1 )
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
            iEndLines = len( getItemHitsLog( open( self.sHitLogFile ) ) )
            #
            self.assertGreaterEqual( iBegLines + min( iLen, 5 ), iEndLines )
            
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    @tag('ebay_api')
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
        iLogID = SearchLog.objects.get(
                    iSearch     = oSearch,
                    tBegSearch  = oSearch.tBegSearch )
        #
        sSearchName = oSearch.cTitle
        sUserName   = oSearch.iUser.username
        sMarket     = oSearch.iUser.iEbaySiteID.cMarket
        #
        t = storeSearchResultsInDB( iLogID,
                                    sMarket,
                                    sUserName,
                                    iSearchID,
                                    sSearchName )
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
                iBegLines = len( getItemHitsLog( open( self.sHitLogFile ) ) )
            #
            findSearchHits( oUser = self.user1 )
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
            iEndLines = len( getItemHitsLog( open( self.sHitLogFile ) ) )
            #
            self.assertGreaterEqual( iBegLines + min( iLen, 5 ), iEndLines )
            
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


class TestFindingResponseHelpers( TestCase ):
    #
    '''test the nifty finding response info extractors'''
    
    def test_get_pagination( self ):
        #
        ''' test getPagination() '''
        #
        dGot = getPagination( sResponseSearchTooBroad )
        #
        dExpect = { 'iCount'    :  100,
                    'iEntries'  : 2374,
                    'iEntriesPP':  100,
                    'iPageNumb' :    1,
                    'iPages'    :   24 }
    
        #
        self.assertEquals( dGot, dExpect )
        #
        dGot = getPagination( '' )
        #
        self.assertNotEquals( dGot, dExpect )
            
    def test_get_success_or_not( self ):
        #
        ''' test getSuccessOrNot() '''
        #
        self.assertTrue(  getSuccessOrNot( sResponseSearchTooBroad ) )
        self.assertFalse( getSuccessOrNot( '' ) )




def getResultGeneratorTheJsonWay():
    #
    from Dict.Maintain  import getDictValuesFromSingleElementLists
    #
    dResponse = getJsonFindingResponse( sResponseSearchTooBroad )
    #
    dPagination = dResponse[  'dPagination']
    #
    iEntries    = dPagination['iEntries'   ]
    #
    iPages      = dPagination['iPages'     ]
    #
    dResultDict = dResponse[ "searchResult" ][0]
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
    getSuccessOrNot( sResponseSearchTooBroad )
    getPagination( sResponseSearchTooBroad )
    #
    return _getFindingResponseGenerator( sResponseSearchTooBroad )


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
    dOnlyPage = getPagination( sResponseSearchTooBroad )



class DoTimeTrialBetweenJsonLoadAndMechanicalWay( TestCase ):
    '''do a time trial, compare loading & using Json load with home brew job'''

    def name_must_start_with_test_to_do_time_trial( self ):
        #
        from Utils.TimeTrial import TimeTrial
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
        dJsonPage = dItem["paginationOutput"]
        #
        dOnlyPage = getPagination( sResponseSearchTooBroad )
        #
        #
        self.assertEquals( dJsonPage["iEntriesPP"], dOnlyPage["iCount"    ] )
        self.assertEquals( dJsonPage["iEntries"],   dOnlyPage["iEntries"  ] )
        self.assertEquals( dJsonPage["iPages"],     dOnlyPage["iPages"    ] )
        self.assertEquals( dJsonPage["iEntriesPP"], dOnlyPage["iEntriesPP"] )
        self.assertEquals(
                      int( dJsonPage["pageNumber"]),dOnlyPage["iPageNumb" ]  )


    def test_get_same_item_info( self ):
        #
        oIterItemsMyWay = getResultGeneratorMyWay()
        oIterItemsJson  = getResultGeneratorTheJsonWay()
        #
        dItemMyWay   = next( oIterItemsMyWay )
        dItemJsonWay = next( oIterItemsJson )
        #
        self.assertEquals( dItemMyWay["itemId"],
                                dItemJsonWay["itemId"] )
        self.assertEquals( dItemMyWay["listingInfo"],
                                dItemJsonWay["listingInfo"] )
        self.assertEquals( dItemMyWay["primaryCategory"],
                                dItemJsonWay["primaryCategory"] )
        self.assertEquals( dItemMyWay["condition"],
                                dItemJsonWay["condition"] )
        self.assertEquals( dItemMyWay["sellingStatus"],
                               dItemJsonWay["sellingStatus"] )


class FileNameUtilitiesTesting( TestCase ):
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
        self.assertEquals( lParts[6], '001' )






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

