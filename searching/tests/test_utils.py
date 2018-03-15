from datetime           import timedelta

from django.test        import TestCase
from django.utils       import timezone
from core.utils_testing import BaseUserTestCase, getDefaultMarket
from ebayinfo.models    import EbayCategory, CategoryHierarchy
from ebayinfo.utils     import dMarket2SiteID

from ..models           import Search, ItemFound, UserItemFound
from ..utils            import ( trySearchCatchExceptions,
                                 doSearchStoreResults,
                                 ItemAlreadyInTable, findSearchHits,
                                 getSearchResultGenerator )

from brands.models      import Brand
from categories.models  import Category
from models.models      import Model

from ..tests            import sExampleResponse, sResponseSearchTooBroad
from File.Del           import DeleteIfExists
from File.Write         import WriteText2File


sExampleFile = '/tmp/search_results.json'

class getImportSearchResultsTests(TestCase):
    #
    def test_get_search_results(self):
        '''test readin an example search results file'''
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        WriteText2File( sExampleResponse, '/tmp', sExampleFile )
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



'''
['id',
 'iCategoryID',
 'name',
 'iLevel',
 'iParentID',
 'bLeafCategory',
 'iTreeVersion',
 'iMarket_id',
 'iSupercededBy',
 'lft',
 'rght',
 'tree_id',
 'level',
 'parent_id']
'''


class getEbayCategoriesSetUp(BaseUserTestCase):

    def setUp(self):
        #
        super( getEbayCategoriesSetUp, self ).setUp()
        #
        from ..tests            import sCategoryDump  # in __init__.py
        #
        from core.utils_testing import getTableFromScreenCaptureGenerator
        #
        from Utils.Config       import getBoolOffYesNoTrueFalse as getBool
        #
        self.market  = getDefaultMarket()
        #
        sMarket, sWantVersion = 'EBAY-US', '117'
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iMarket         = self.market,
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        sMarket, sWantVersion = 'EBAY-GB', '108'
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iMarket_id      = 3,
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        oTableIter = getTableFromScreenCaptureGenerator( sCategoryDump )
        #
        lHeader = next( oTableIter )
        #
        for lParts in oTableIter:
            #
            oCategory = EbayCategory(
                    iCategoryID     = int(      lParts[1] ),
                    name            =           lParts[2],
                    iLevel          = int(      lParts[3] ),
                    
                    bLeafCategory   = getBool(  lParts[5] ),
                    iTreeVersion    = int(      lParts[6] ),
                    iMarket_id      = int(      lParts[7] ), )
            #
            if lParts[3] == '1': # top level iParentID
                oCategory.iParentID = oRootCategory.iCategoryID
                oCategory.parent    = oRootCategory
            else:
                oCategory.iParentID = int(     lParts[4] )
                oCategory.parent= EbayCategory.objects.get(
                                    iCategoryID = int( lParts[4] ),
                                    iMarket     = oCategory.iMarket )
            #
            oCategory.save()


class storeItemFoundTests(getEbayCategoriesSetUp):
    #
    ''' class for testing storeItemFound() '''

    def test_store_ebay_categories(self):
        #
        ''' testing the ebay item categories '''
        #
        from ..tests            import sCategoryDump  # in __init__.py
        #
        from core.utils_testing import getTableFromScreenCaptureGenerator
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


    def test_get_ebay_category_hierarchy(self):
        #
        ''' test getEbayCategoryHierarchies() retrieval & caching '''
        #
        from ..tests        import dSearchResult # in __init__.py
        #
        from ..utils        import getEbayCategoryHierarchies
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
        iMarketEbayUS = dMarket2SiteID.get( dSearchResult.get( 'globalId' ) )
        #
        oCatHierarchy = CategoryHierarchy.objects.get(
            iCategoryID = iCategoryID,
            iMarket     = iMarketEbayUS )
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
        dExpect = { (iCategoryID, iMarketEbayUS) : oCatHierarchy.id }
        #
        self.assertEqual( dEbayCatHierarchies, dExpect )
        #
        # try again
        #
        lOrigCatHeirarchy = dEbayCatHierarchies[ (iCategoryID, iMarketEbayUS) ]
        #
        lCatHeirarchy = getEbayCategoryHierarchies(
                            dSearchResult, dEbayCatHierarchies )
        #
        self.assertIs(
            dEbayCatHierarchies[ (iCategoryID, iMarketEbayUS) ], lOrigCatHeirarchy )
        
        # try again a 3rd time
        #
        dEbayCatHierarchiesNew = {}
        #
        t = getEbayCategoryHierarchies(
                            dSearchResult, dEbayCatHierarchiesNew )
        #
        iCatHeirarchy, i2ndCatHeirarchy = t
        #
        lNewCatHeirarchy = dEbayCatHierarchiesNew[ (iCategoryID, iMarketEbayUS) ]
        #
        lCatHeirarchy = getEbayCategoryHierarchies(
                            dSearchResult, dEbayCatHierarchiesNew )
        #
        self.assertIsNot( dEbayCatHierarchies, dEbayCatHierarchiesNew )
        #
        self.assertEqual( lNewCatHeirarchy, lOrigCatHeirarchy )
        #
        self.assertEqual( dEbayCatHierarchies, dEbayCatHierarchiesNew )



    def test_store_item_found(self):
        #
        ''' test storeItemFound() with actual record'''
        #
        from ..tests    import dSearchResult # in __init__.py
        #
        from ..utils    import storeItemFound
        #
        dEbayCatHierarchies = {}
        #
        iItemNumb = storeItemFound( dSearchResult, dEbayCatHierarchies )
        #
        iCategoryID = int(
                dSearchResult.get( 'primaryCategory' ).get( 'categoryId' ) )
        #
        iEbaySiteID = dMarket2SiteID.get( dSearchResult.get( 'globalId' ) )
        #
        iCatHeirarchy = CategoryHierarchy.objects.get(
                            iCategoryID = iCategoryID,
                            iMarket     = iEbaySiteID ).pk
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
                iMarket     = iEbaySiteID )
        #
        sExpect = oExpectHierarchy.cCatHierarchy
        #
        
        #self.assertEqual( oResultRow.iCatHeirarchy.cCatHierarchy, sExpect )
        #
        try: # again
            storeItemFound( dSearchResult )
        except ItemAlreadyInTable as e:
            self.assertEqual(
                    str(e),
                    'ItemID %s is already in the ItemFound table' %
                    dSearchResult['itemId'] )
        else:
            self.assertTrue( False ) # exception should hve been raised
        #
        



class storeUserItemFoundTests(getEbayCategoriesSetUp):
    #
    ''' class for testing storeUserItemFound() '''

    def test_store_User_item_found(self):
        #
        ''' test storeUserItemFound() with actual record'''
        #
        from ..tests    import dSearchResult # in __init__.py
        from ..utils    import storeUserItemFound, storeItemFound
        #
        class ThisShouldNotBeHappening( Exception ): pass

        sSearch         = "My clever search 1"
        self.oSearch    = Search( cTitle= sSearch, iUser = self.user1 )
        self.oSearch.save()
        #
        iItemNumb = storeItemFound( dSearchResult, {} )
        #
        if iItemNumb is None:
            raise ThisShouldNotBeHappening
        #
        try:
            storeUserItemFound(
                    dSearchResult, iItemNumb, self.user1, self.oSearch.id )
        except ItemAlreadyInTable:
            pass
        #
        oResultRow = UserItemFound.objects.filter(
                            iItemNumb   = iItemNumb,
                            iUser       = self.user1 ).first()
        #
        self.assertIsNotNone( oResultRow )
        #
        try: # again
            storeUserItemFound(
                    dSearchResult, iItemNumb, self.user1, self.oSearch.id )
        except ItemAlreadyInTable as e:
            self.assertEqual(
                    str(e),
                    'ItemFound %s is already in the UserItemFound table for %s' %
                    ( iItemNumb, self.user1.username ) )
        else:
            self.assertTrue( False ) # exception should hve been raised



class storeSearchResultsTests(getEbayCategoriesSetUp):
    #
    ''' class for testing doSearchStoreResults() store records '''
    #
    def setUp(self):
        # storeSearchResultsTests, self 
        #
        from searching import sResultFileNamePattern
        #
        super().setUp()
        #
        sSearch = "My clever search 1"
        oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        #
        self.sExampleFile = (
            sResultFileNamePattern % # 'Search_%s_%s_ID_%s.json'
            ( 'EBAY-US', self.user1.username, oSearch.id ) )
        #
        WriteText2File( sExampleResponse, '/tmp', self.sExampleFile )
        
    def tearDown(self):
        #
        DeleteIfExists( '/tmp', self.sExampleFile )

    def test_store_search_results(self):
        #
        ''' test storeUserItemFound() with actual record'''
        #
        iCountItems, iStoreItems, iStoreUsers = (
                trySearchCatchExceptions( sFileName = self.sExampleFile ) )
        #
        self.assertEqual( ItemFound.objects.count(), iCountItems )
        self.assertEqual( ItemFound.objects.count(), iStoreItems )
        #
        self.assertEqual( UserItemFound.objects.count(), iStoreUsers )
        #
        # try again with the same data
        #
        iCountItems, iStoreItems, iStoreUsers = (
                trySearchCatchExceptions( sFileName = self.sExampleFile ) )
        #
        self.assertEqual( ItemFound.objects.count(), iCountItems )
        #
        self.assertEqual( iStoreItems, 0 )
        #
        self.assertEqual( iStoreUsers, 0 )
        #



class findSearchHitsTests(getEbayCategoriesSetUp):
    #
    ''' class for testing doSearchStoreResults() store records '''
    #
    def setUp(self):
        # storeSearchResultsTests, self 
        #
        from os.path    import join
        from searching  import sResultFileNamePattern
        #
        super().setUp()
        #
        sSearch = "My clever search 1"
        oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        #
        self.sExampleFile = (
            sResultFileNamePattern % # 'Search_%s_%s_ID_%s.json'
            ( 'EBAY-US', self.user1.username, oSearch.id ) )
        #
        WriteText2File( sResponseSearchTooBroad, '/tmp', self.sExampleFile )
        #
        doSearchStoreResults( sFileName = join( '/tmp', self.sExampleFile ) )
        #
        oCategory   = Category( cTitle = 'Radio', iStars = 9, iUser = self.user1 )
        #
        oCategory.save()
        #
        oBrand      = Brand( cTitle = 'Garod', cLookFor = 'Garol',
                             iStars = 5, iUser = self.user1 )
        #
        oBrand.save()
        #
        oModel      = Model( cTitle = '6AU-1',
                            iBrand = oBrand, iCategory = oCategory,
                            iStars = 5, iUser = self.user1 )
        #
        oModel.save()
        #
        oBrand      = Brand( cTitle = 'Addison', iStars = 7,
                             iUser = self.user1 )
        #
        oBrand.save()
        #
        oModel      = Model( cTitle = '5', iBrand = oBrand, iStars = 6,
                             iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        oBrand      = Brand( cTitle = 'Fada', iStars = 8, iUser = self.user1 )
        #
        oBrand.save()
        #
        oModel      = Model( cTitle = '115', cLookFor = 'bullet', iStars = 6,
                            iBrand = oBrand, iCategory = oCategory, 
                            iUser = self.user1 )
        #
        oModel.save()
        #
        oModel      = Model( cTitle = '1000', iBrand = oBrand, iStars = 6,
                            iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        oModel      = Model( cTitle = 'L-56', iBrand = oBrand, iStars = 6,
                             iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        oBrand      = Brand( cTitle = 'Emerson', iStars = 6,
                             iUser = self.user1 )
        #
        oBrand.save()
        #
        oModel      = Model( cTitle = '520', iBrand = oBrand, iStars = 6,
                            iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        oModel      = Model( cTitle = 'AX-235', iBrand = oBrand, iStars = 6,
                            iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        oBrand      = Brand( cTitle = 'DeWald', iStars = 4,
                             iUser = self.user1 )
        #
        oBrand.save()
        #
        oModel      = Model( cTitle = 'A-501', iBrand = oBrand, iStars = 6,
                             iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        
        
    def tearDown(self):
        #
        DeleteIfExists( '/tmp', self.sExampleFile )

    def test_find_search_hits(self):
        #
        ''' test storeUserItemFound() with actual record'''
        #
        findSearchHits( self.user1 )



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