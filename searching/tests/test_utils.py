from datetime           import timedelta

from django.test        import TestCase, tag
from django.utils       import timezone
from core.utils_testing import ( BaseUserTestCase, getDefaultMarket,
                                 getEbayCategoriesSetUp,
                                 setUpBrandsCategoriesModels )

from ebayinfo.models    import EbayCategory, CategoryHierarchy
from ebayinfo.utils     import dMarket2SiteID

from ..models           import Search, ItemFound, UserItemFound, ItemFoundTemp
from ..utils            import ( trySearchCatchExceptions,
                                 doSearchStoreResults, ItemAlreadyInTable,
                                 findSearchHits, getFoundItemTester,
                                 getSearchResultGenerator,
                                _getModelRegExFinders4Test,
                                _getCategoryRegExFinders4Test,
                                _getBrandRegExFinders4Test )

from brands.models      import Brand
from categories.models  import Category
from models.models      import Model

from ..tests            import sExampleResponse, sResponseSearchTooBroad
from File.Del           import DeleteIfExists
from File.Write         import WriteText2File




class findersStorageTest( setUpBrandsCategoriesModels ):
    
    #
    ''' test Finder Storage for Brands, Categories & Models '''
    
    #
    #oBrand      = Model.objects.get(    cTitle = "Cadillac"  )
    #oCategory   = Category.objects.get( cTitle = "Widgets"   )
    #oModel      = Model.objects.get(    cTitle = "Fleetwood" )
    #
    def test_BrandRegExFinderStorage(self):
        #
        t = _getBrandRegExFinders4Test( self.oBrand )
        #
        findTitle, findExclude = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #


    def test_CategoryRegExFinderStorage(self):
        #
        t = _getCategoryRegExFinders4Test( self.oCategory )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords( sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Gemini Jets 1/200 Delta MD-80 Widget Livery N956DL'
        #
        self.assertTrue(  findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertFalse( findTitle(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords( sAuctionTitle ) )
        #



    def test_ModelRegExFinderStorage(self):
        #
        t = _getModelRegExFinders4Test( self.oModel )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords( sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )

        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertFalse( findTitle(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords( sAuctionTitle ) )
        #

    def testBrandGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oBrand, dFinders )
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertTrue(  bExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        foundItem = dFinders[ self.oBrand.pk ]
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        self.assertIn(     self.oBrand.cRegExLook4Title,
                                    ( 'Cadillac|Caddy', 'Caddy|Cadillac') )
        #
        self.assertEquals( self.oBrand.cRegExExclude, 'golf' )



    def testCategoryGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oCategory, dFinders )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'Gemini Jets 1/200 Delta MD-80 Widget Livery N956DL'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertTrue(  bExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        foundItem = dFinders[ self.oCategory.pk ]
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        self.assertIn(     self.oCategory.cRegExLook4Title,
                                        ( 'Gizmo|Widget', 'Widget|Gizmo' ) )
        #
        self.assertEquals( self.oCategory.cRegExExclude,  'Delta'  )
        self.assertEquals( self.oCategory.cRegExKeyWords, 'Gadget' )


    def testModelGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oModel, dFinders )
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertTrue(  bExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        foundItem = dFinders[ self.oModel.pk ]
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        bInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  bInTitle     )
        self.assertFalse( bExcludeThis )
        #
        self.assertIn(     self.oModel.cRegExLook4Title,
                                ( 'Woodie|Fleetwood', 'Fleetwood|Woodie' ) )
        #
        self.assertEquals( self.oModel.cRegExExclude,  'golf'     )
        self.assertEquals( self.oModel.cRegExKeyWords, 'Eldorado' )



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


class storeItemFoundTests(getEbayCategoriesSetUp):
    #
    ''' class for testing storeItemFound() '''

    def test_store_ebay_categories(self):
        #
        ''' testing the ebay item categories '''
        #
        from ebayinfo           import sCategoryDump  # in __init__.py
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
        from searching import RESULTS_FILE_NAME_PATTERN
        #
        super( storeSearchResultsTests, self ).setUp()
        #
        sSearch = "My clever search 1"
        oSearch = Search( cTitle= sSearch, iUser = self.user1 )
        oSearch.save()
        #
        self.sExampleFile = (
            RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s.json'
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




class getBrandsCategoriesModelsSetUp(getEbayCategoriesSetUp):
    #
    ''' base class for testing doSearchStoreResults() store records '''
    #
    def setUp(self):
        # storeSearchResultsTests, self 
        #
        from os.path    import join
        from searching  import RESULTS_FILE_NAME_PATTERN
        #
        super( getBrandsCategoriesModelsSetUp, self ).setUp()
        #
        sSearch = "Catalin Radios"
        #
        sKeyWords = 'catalin radio'
        #
        self.oSearch = Search(
                        cTitle      = sSearch,
                        cKeyWords   = sKeyWords,
                        iUser       = self.user1 )
        #
        self.oSearch.save()
        #
        oCategory   = Category( cTitle = 'Radio', iStars = 9,
                               cExcludeIf = 'reproduction', iUser = self.user1 )
        #
        oCategory.save()
        #
        oBrand      = Brand( cTitle = 'Garod', cLookFor = 'Garol',
                             iStars = 5, iUser = self.user1 )
        #
        oBrand.save()
        #
        oModel      = Model( cTitle = '6AU1',
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
        oModel      = Model( cTitle = '115', cLookFor = 'bullet', iStars = 9,
                            iBrand = oBrand, iCategory = oCategory, 
                            iUser = self.user1 )
        #
        oModel.save()
        #
        oModel      = Model( cTitle = '1000', iBrand = oBrand, iStars = 8,
                            iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        oModel      = Model( cTitle = '188', iBrand = oBrand, iStars = 7,
                            iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        oModel      = Model( cTitle = 'L56', iBrand = oBrand, iStars = 6,
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
        oModel      = Model( cTitle = 'AX235', iBrand = oBrand, iStars = 6,
                            iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        oBrand      = Brand( cTitle = 'DeWald', iStars = 4,
                             iUser = self.user1 )
        #
        oBrand.save()
        #
        oModel      = Model( cTitle = 'A501', iBrand = oBrand, iStars = 6,
                             iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        oBrand      = Brand( cTitle = 'Crosley', iStars = 3,
                             iUser = self.user1 )
        #
        oBrand.save()
        #
        oModel      = Model( cTitle = '1465', iBrand = oBrand, iStars = 5,
                             iCategory = oCategory, iUser = self.user1 )
        #
        oModel.save()
        #
        oBrand      = Brand( cTitle = 'RCA', iStars = 6,
                             iUser = self.user1 )
        #
        oBrand.save()
        #
        oBrand      = Brand( cTitle = 'Motorola', iStars = 5,
                             iUser = self.user1 )
        #
        oBrand.save()
        #
        


class findSearchHitsTests(getBrandsCategoriesModelsSetUp):
    #
    ''' class for testing doSearchStoreResults() store records '''
    #
    def setUp(self):
        #
        super( findSearchHitsTests, self ).setUp()
        #
        self.sExampleFile = (
            RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s.json'
            ( 'EBAY-US', self.user1.username, self.oSearch.id ) )
        #
        WriteText2File( sResponseSearchTooBroad, '/tmp', self.sExampleFile )
        #
        doSearchStoreResults( sFileName = join( '/tmp', self.sExampleFile ) )
        #
        print( '\n' )
        print( 'setting up findSearchHitsTests' )

    def test_find_search_hits(self):
        #
        ''' test storeUserItemFound() with actual record'''
        #
        findSearchHits( self.user1 )
        #
        oTempItemsFound = ItemFoundTemp.objects.all()
        #
        self.assertEquals( len( oTempItemsFound ), 17 )
        #
        oUserItems = UserItemFound.objects.filter(
                        iUser = self.user1 ).order_by( '-iHitStars' )
        #
        iCount = 0
        #
        for oTemp in oUserItems:
            #
            #print( '\n' )
            ##
            if oTemp.iHitStars == 0: break
            ##
            #sSayModel = sSayBrand = sSayCategory = ''
            ##
            #if oTemp.iModel:
                #sSayModel = oTemp.iModel.cTitle
            #if oTemp.iBrand:
                #sSayBrand = oTemp.iBrand.cTitle
            #if oTemp.iCategory:
                #sSayCategory = oTemp.iCategory.cTitle
            
            #print( 'Auction Title:', oTemp.iItemNumb.cTitle )

            #print( 'ItemNumb     :', oTemp.iItemNumb.pk     )
            #print( 'iHitStars    :', oTemp.iHitStars        )
            #print( 'Model        :', sSayModel              )
            #print( 'Brand        :', sSayBrand              )
            #print( 'Category     :', sSayCategory           )
            ##
            #print( 'Search       :', oTemp.iSearch.cTitle   )
            #print( 'WhereCategory:', oTemp.cWhereCategory   )
            #print( 'Evaluated    :',
                  #oTemp.tlook4hits.strftime('%Y-%m-%d %H:%M:%S'))
            #print( 'Auction End  :', oTemp.iItemNumb.tTimeEnd)
            #
            iCount += 1
        #
        print( '\n' )
        print( 'did test_find_search_hits' )
        #
        self.assertEquals( iCount, 17 )
        #

class findSearchHitsTests(getBrandsCategoriesModelsSetUp):
    #
    ''' class for testing doSearchStoreResults() store records '''
    #

    @tag('ebay_api')
    def test_search_store_results( self ):
        #
        # sandbox returns 0 items, can use it to test for 0 items
        t = doSearchStoreResults(
                iSearchID = self.oSearch.id, bUseSandbox = False )
        #
        iItems, iStoreItems, iStoreUsers = t
        #
        print( 'iItems, iStoreItems, iStoreUsers:',
                iItems, iStoreItems, iStoreUsers )

        oUserItems = UserItemFound.objects.filter(
                        iUser = self.user1 ).order_by( '-iHitStars' )
        #

        print( '\n' )
        print( 'did do_search_store_results_test' )


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