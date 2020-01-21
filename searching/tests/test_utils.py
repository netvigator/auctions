import inspect
import logging

from os                 import rename
from os.path            import realpath, join
from datetime           import timedelta

from django.test        import tag
from django.utils       import timezone
from core.tests.base    import ( getDefaultMarket,
                                 GetEbayCategoriesWebTestSetUp,
                                 getTableFromScreenCaptureGenerator,
                                 TestCasePlus )

# from django.core.exceptions import ObjectDoesNotExist
from core.dj_import     import ObjectDoesNotExist

from ebayinfo.models    import CategoryHierarchy, EbayCategory
from ebayinfo.tests     import sEbayCategoryDump
from ebayinfo.utils     import dMarket2SiteID, getEbayCategoryHierarchies

from ebayinfo.tests.test_utils import LiveTestGotCurrentEbayCategories
# imported live test will run automatically when running live test

from searching          import RESULTS_FILE_NAME_PATTERN
from searching          import SEARCH_FILES_FOLDER

from .base              import ( StoreSearchResultsTestsWebTestSetUp,
                                 GetBrandsCategoriesModelsWebTestSetUp,
                                 StoreUserItemFoundWebTestBase,
                                 getItemHitsLog )

from ..models           import Search, SearchLog
from ..tests            import ( dSearchResult, sItemHitLog,
                                 sExampleResponse, iExampleResponseCount,
                                 sResponseItems2Test )
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

from categories.models  import Category
from models.models      import Model

from finders.models     import ItemFound, UserItemFound, ItemFoundTemp

from pyPks.Dict.Maintain import getDictValuesFromSingleElementLists
from pyPks.File.Del      import DeleteIfExists
from pyPks.File.Spec     import getPathNameExt
from pyPks.File.Test     import isFileThere
from pyPks.File.Write    import QuietDump
from pyPks.String.Get    import getTextBefore
from pyPks.Time.Convert  import getDateTimeObjFromString   as getDate
from pyPks.Time.Delta    import getDeltaDaysFromStrings, getIsoDateTimeNowPlus
from pyPks.Time.Output   import getIsoDateTimeFromDateTime as getIsoDT
from pyPks.Time.Test     import isISOdatetime



logger = logging.getLogger(__name__)
logging_level = logging.INFO

'''
this will print logging messages to the terminal
logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)
'''

sExampleFile = '/tmp/search_results_____0_.json'



def updateHitLogFile( oUserItems, sPathHere ):
    #
    sHitLogFile = join( sPathHere, 'ItemHitsLog.log' )
    sHitLogBack = join( sPathHere, 'ItemHitsLog.bak' )
    #
    if not isFileThere( sHitLogFile ):
        #
        QuietDump( sItemHitLog, sHitLogFile )
        #
    #
    lItemHits = getItemHitsLog( sHitLogFile )
    #
    iBegRows = len( lItemHits )
    #
    # discard rows that are too old
    #
    sDateTimeAgo = getIsoDateTimeNowPlus( -100 )
    #
    lItemHits = [ d for d in lItemHits if d['tTimeEnd' ] > sDateTimeAgo ]
    #
    iEndRows = len( lItemHits )
    #
    setItemNumbsAlready = set( ( int( d['iItemNumb'] ) for d in lItemHits ) )
    #
    iNew = 0
    #
    tTargetStars = ( 400, 350, 300, 250, 200 )
    #
    for iTargetStars in tTargetStars:
        #
        for oItemHit in oUserItems:
            #
            if oItemHit.iItemNumb_id in setItemNumbsAlready: continue
            #
            if oItemHit.iHitStars < iTargetStars: continue
            #
            dRow = dict(
                iItemNumb   = str(      oItemHit.iItemNumb_id ),
                tTimeEnd    = getIsoDT( oItemHit.iItemNumb.tTimeEnd ),
                iHitStars   = str(      oItemHit.iHitStars ) )
            #
            lItemHits.append( dRow )
            #
            setItemNumbsAlready.add( oItemHit.iItemNumb_id )
            #
            iNew += 1
            #
            if iNew >= 5: break
        #
    #
    if iNew > 0:
        #
        lOut = [ ' | '.join( ( d['tTimeEnd'],d['iItemNumb'],d['iHitStars'] ) )
                    for d in lItemHits ]
        #
        iEndRows = len( lOut )
        #
        lOut.sort()
        #
        lOut[0:0] = [ 'tTimeEnd            | iItemNumb    | iHitStars' ]
        #
        sOut = '%s\n' % '\n'.join( lOut )
        #
        DeleteIfExists( sHitLogBack )
        #
        rename( sHitLogFile, sHitLogBack )
        #
        QuietDump( sOut, sHitLogFile )
        #
    #
    return iBegRows, iEndRows


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
        self.assertEqual( iItems, iExampleResponseCount )
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
        iTableCount = EbayCategory.objects.all().count()
        #
        oTableIter = getTableFromScreenCaptureGenerator( sEbayCategoryDump )
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
            #
            _storeItemFound( dSearchResult, dEbayCatHierarchies )
            #
        except ItemAlreadyInTable as e:
            #
            self.assertEqual(
                    str(e),
                    'ItemID %s is already in the ItemFound table' %
                    dSearchResult['itemId'] )
            #
        else:
            #
            self.assertTrue( False ) # exception should hve been raised
            #
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
        #
        #logger.info("class storeItemFoundTests")



class storeUserItemFoundTests( StoreUserItemFoundWebTestBase ):
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
        self.assertEqual( oSearchLog.iItems,      iExampleResponseCount )
        self.assertEqual( oSearchLog.iStoreItems, iExampleResponseCount )
        self.assertEqual( oSearchLog.iStoreUsers, iExampleResponseCount )
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



    def test_oddball_item_search_results(self):
        #
        oOddBall = ItemFound.objects.get( iItemNumb = 233420619849 )
        #
        self.assertEqual(
                oOddBall.iCatHeirarchy.cCatHierarchy,
                'Consumer Electronics, Vintage Electronics, '
                'Vintage Audio & Video, Vintage Parts & Accessories, '
                'Vintage Tubes & Tube Sockets' )
        #
        self.assertEqual(
                oOddBall.i2ndCatHeirarchy.cCatHierarchy,
                'eBay Motors, Parts & Accessories, '
                'Vintage Car & Truck Parts, Radio & Speaker Systems' )

        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



class TestGenericModelOkay( GetBrandsCategoriesModelsWebTestSetUp ):

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

