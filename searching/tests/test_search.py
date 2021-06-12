from os.path                import join, split

from django.db.models       import Max
from django.http            import HttpResponseRedirect
from django.urls            import reverse, reverse_lazy

from core.tests.base        import ( setup_view_for_tests,
                                     GetEbayCategoriesWebTestSetUp,
                                     AssertEmptyMixin, TestCasePlus,
                                     BaseUserWebTestCase )

from core.utils             import getShrinkItemURL

from finders.models         import ItemFound, UserItemFound

from searching              import RESULTS_FILE_NAME_PATTERN
from searching              import SEARCH_FILES_ROOT
from searching              import getPriorityChoices, ALL_PRIORITIES

from .base                  import StoreSearchResultsTestsWebTestSetUp, sTODAY

from ..models               import Search, SearchLog
from ..tests                import ( sExampleResponse, sLastPageZeroEntries,
                                     iExampleResponseCount,
                                     sSuccessButZeroResults )
from ..utils                import ( getIdStrZeroFilled, getSearchIdStr,
                                     getHowManySearchDigitsNeeded,
                                     storeSearchResultsInFinders )
from ..utilsearch           import ( getSearchRootFolders,
                                     getSearchResultGenerator )
from ..views                import SearchCreateView

from pyPks.Dir.Get          import getMakeDir
from pyPks.File.Del         import DeleteIfExists
from pyPks.File.Write       import QuietDump
from pyPks.String.Get       import getTextBefore
from pyPks.Time.Test        import isISOdatetime
from pyPks.Utils.Both2n3    import getThisFileSpec


tExampleFile = (
        join( SEARCH_FILES_ROOT, sTODAY, ),
        'search_results_____0_.json' )

getMakeDir( getThisFileSpec( tExampleFile[0] ) )


class BaseUserWebTestCaseCanAddSearches( BaseUserWebTestCase ):
    ''' test getPriorityChoices() '''
    #
    def setUp( self ):
        #
        super().setUp()
        #
        self.addSearch( "My clever search c", 'C1', self.user1 )
        #
        self.addSearch( "My clever search D", 'D2', self.user1 )
        #
        self.addSearch( "My clever Manual search", 'A1', self.user1 )
        #
    #
    def addSearch( self, cTitle, cPriority, oUser ):
        #
        oSearch     = Search(
                        cTitle      = cTitle,
                        cPriority   = cPriority,
                        iUser       = oUser )
        #
        oSearch.save()

    #
    def getPriorityChoices( self, oUser, sThisPriority = None ):
        #
        return getPriorityChoices( Search, oUser, sThisPriority )


class TestHowManyUserDigitsNeeded( BaseUserWebTestCaseCanAddSearches ):
    ''' test getHowManySearchDigitsNeeded() '''

    def test_how_many_digits_needed( self ):
        #
        # several Searches could have been created & destroyed already
        # pk gets incrememted, could be over 100!
        #
        self.assertIn( getHowManySearchDigitsNeeded(), (1,2,3) )
        #
        for i in range( 3, 10 ):
            #
            self.addSearch( "My clever search %s" % i, 'A%s' % i, self.user1 )
        #
        self.assertIn( getHowManySearchDigitsNeeded(), ( 2, 3 ) )
        #
        for iOrd in range( 69, 81 ):
            #
            sChar = chr( iOrd )
            #
            for i in range( 1, 10 ):
                #
                self.addSearch( "My clever search %s%s" % ( sChar, str(i) ),
                                '%s%s' % ( sChar, str(i) ),
                                self.user1 )
        #
        self.assertEqual( getHowManySearchDigitsNeeded(), 3 )
        #
        data = dict(
            cTitle      = "Great Widget",
            cKeyWords   = "Blah bleh blih",
            cPriority   = 'Q1',
            iUser       = self.user1 )
        #
        request = self.factory.get(reverse('searching:add'))
        #
        request.user = self.user1
        #
        view = setup_view_for_tests( SearchCreateView(), self.request )
        #
        form = view.get_form()
        #
        url = reverse_lazy('searching:add')
        #
        response = self.client.post( url, data )
        #
        self.assertEqual(response.status_code, 302 )
        #
        # view.get_success_url() # cannot work,
        # 'SearchCreateView' object has no attribute 'object'
        #
        iLast = Search.objects.all().aggregate(Max('id'))['id__max']
        #
        # lack of success get_success_url
        self.assertRedirects( response, '/searching/' )
        #
        self.assertEqual( getHowManySearchDigitsNeeded(), 3 )
        #


    def test_get_ID_str_zero_filled( self ):
        #
        self.assertEqual( getIdStrZeroFilled(   1, 3 ),  '001' )
        #
        self.assertEqual( getIdStrZeroFilled( 100, 2 ),  '100' )
        #
        self.assertEqual( getIdStrZeroFilled( 100, 4 ), '0100' )
        #


class TestGetPriorityChoices( BaseUserWebTestCaseCanAddSearches ):
    ''' test getPriorityChoices() '''
    #
    def test_getPriorityChoices( self ):
        #
        #
        tChoices = self.getPriorityChoices( self.user1 )
        #
        tExpect = (
                         ('A2','A2'), ('A3','A3'), ('A4','A4'), ('A5','A5'), ('A6','A6'), ('A7','A7'), ('A8','A8'), ('A9','A9'),
            ('B1','B1'), ('B2','B2'), ('B3','B3'), ('B4','B4'), ('B5','B5'), ('B6','B6'), ('B7','B7'), ('B8','B8'), ('B9','B9'),
                         ('C2','C2'), ('C3','C3'), ('C4','C4'), ('C5','C5'), ('C6','C6'), ('C7','C7'), ('C8','C8'), ('C9','C9'),
            ('D1','D1'),              ('D3','D3'), ('D4','D4'), ('D5','D5'), ('D6','D6'), ('D7','D7'), ('D8','D8'), ('D9','D9'),
            ('E1','E1'), ('E2','E2'), ('E3','E3'), ('E4','E4'), ('E5','E5'), ('E6','E6'), ('E7','E7'), ('E8','E8'), ('E9','E9'),
            ('F1','F1'), ('F2','F2'), ('F3','F3'), ('F4','F4'), ('F5','F5'), ('F6','F6'), ('F7','F7'), ('F8','F8'), ('F9','F9'),
            ('G1','G1'), ('G2','G2'), ('G3','G3'), ('G4','G4'), ('G5','G5'), ('G6','G6'), ('G7','G7'), ('G8','G8'), ('G9','G9'),
            ('H1','H1'), ('H2','H2'), ('H3','H3'), ('H4','H4'), ('H5','H5'), ('H6','H6'), ('H7','H7'), ('H8','H8'), ('H9','H9'),
            ('I1','I1'), ('I2','I2'), ('I3','I3'), ('I4','I4'), ('I5','I5'), ('I6','I6'), ('I7','I7'), ('I8','I8'), ('I9','I9'),
            ('J1','J1'), ('J2','J2'), ('J3','J3'), ('J4','J4'), ('J5','J5'), ('J6','J6'), ('J7','J7'), ('J8','J8'), ('J9','J9'),
            ('K1','K1'), ('K2','K2'), ('K3','K3'), ('K4','K4'), ('K5','K5'), ('K6','K6'), ('K7','K7'), ('K8','K8'), ('K9','K9'),
            ('L1','L1'), ('L2','L2'), ('L3','L3'), ('L4','L4'), ('L5','L5'), ('L6','L6'), ('L7','L7'), ('L8','L8'), ('L9','L9'),
            ('M1','M1'), ('M2','M2'), ('M3','M3'), ('M4','M4'), ('M5','M5'), ('M6','M6'), ('M7','M7'), ('M8','M8'), ('M9','M9'),
            ('N1','N1'), ('N2','N2'), ('N3','N3'), ('N4','N4'), ('N5','N5'), ('N6','N6'), ('N7','N7'), ('N8','N8'), ('N9','N9'),
            ('O1','O1'), ('O2','O2'), ('O3','O3'), ('O4','O4'), ('O5','O5'), ('O6','O6'), ('O7','O7'), ('O8','O8'), ('O9','O9'),
            ('P1','P1'), ('P2','P2'), ('P3','P3'), ('P4','P4'), ('P5','P5'), ('P6','P6'), ('P7','P7'), ('P8','P8'), ('P9','P9'),
            ('Q1','Q1'), ('Q2','Q2'), ('Q3','Q3'), ('Q4','Q4'), ('Q5','Q5'), ('Q6','Q6'), ('Q7','Q7'), ('Q8','Q8'), ('Q9','Q9'),
            ('R1','R1'), ('R2','R2'), ('R3','R3'), ('R4','R4'), ('R5','R5'), ('R6','R6'), ('R7','R7'), ('R8','R8'), ('R9','R9'),
            ('S1','S1'), ('S2','S2'), ('S3','S3'), ('S4','S4'), ('S5','S5'), ('S6','S6'), ('S7','S7'), ('S8','S8'), ('S9','S9'),
            ('T1','T1'), ('T2','T2'), ('T3','T3'), ('T4','T4'), ('T5','T5'), ('T6','T6'), ('T7','T7'), ('T8','T8'), ('T9','T9'),
            ('U1','U1'), ('U2','U2'), ('U3','U3'), ('U4','U4'), ('U5','U5'), ('U6','U6'), ('U7','U7'), ('U8','U8'), ('U9','U9'),
            ('V1','V1'), ('V2','V2'), ('V3','V3'), ('V4','V4'), ('V5','V5'), ('V6','V6'), ('V7','V7'), ('V8','V8'), ('V9','V9'),
            ('W1','W1'), ('W2','W2'), ('W3','W3'), ('W4','W4'), ('W5','W5'), ('W6','W6'), ('W7','W7'), ('W8','W8'), ('W9','W9'),
            ('X1','X1'), ('X2','X2'), ('X3','X3'), ('X4','X4'), ('X5','X5'), ('X6','X6'), ('X7','X7'), ('X8','X8'), ('X9','X9'),
            ('Y1','Y1'), ('Y2','Y2'), ('Y3','Y3'), ('Y4','Y4'), ('Y5','Y5'), ('Y6','Y6'), ('Y7','Y7'), ('Y8','Y8'), ('Y9','Y9'),
            ('Z1','Z1'), ('Z2','Z2'), ('Z3','Z3'), ('Z4','Z4'), ('Z5','Z5'), ('Z6','Z6'), ('Z7','Z7'), ('Z8','Z8'), ('Z9','Z9'))
        #
        self.assertEqual( tChoices, tExpect )
        #
        tChoices = self.getPriorityChoices( self.user1, 'A1' )
        #
        tExpect = (
            ('A1','A1'), ('A2','A2'), ('A3','A3'), ('A4','A4'), ('A5','A5'), ('A6','A6'), ('A7','A7'), ('A8','A8'), ('A9','A9'),
            ('B1','B1'), ('B2','B2'), ('B3','B3'), ('B4','B4'), ('B5','B5'), ('B6','B6'), ('B7','B7'), ('B8','B8'), ('B9','B9'),
                         ('C2','C2'), ('C3','C3'), ('C4','C4'), ('C5','C5'), ('C6','C6'), ('C7','C7'), ('C8','C8'), ('C9','C9'),
            ('D1','D1'),              ('D3','D3'), ('D4','D4'), ('D5','D5'), ('D6','D6'), ('D7','D7'), ('D8','D8'), ('D9','D9'),
            ('E1','E1'), ('E2','E2'), ('E3','E3'), ('E4','E4'), ('E5','E5'), ('E6','E6'), ('E7','E7'), ('E8','E8'), ('E9','E9'),
            ('F1','F1'), ('F2','F2'), ('F3','F3'), ('F4','F4'), ('F5','F5'), ('F6','F6'), ('F7','F7'), ('F8','F8'), ('F9','F9'),
            ('G1','G1'), ('G2','G2'), ('G3','G3'), ('G4','G4'), ('G5','G5'), ('G6','G6'), ('G7','G7'), ('G8','G8'), ('G9','G9'),
            ('H1','H1'), ('H2','H2'), ('H3','H3'), ('H4','H4'), ('H5','H5'), ('H6','H6'), ('H7','H7'), ('H8','H8'), ('H9','H9'),
            ('I1','I1'), ('I2','I2'), ('I3','I3'), ('I4','I4'), ('I5','I5'), ('I6','I6'), ('I7','I7'), ('I8','I8'), ('I9','I9'),
            ('J1','J1'), ('J2','J2'), ('J3','J3'), ('J4','J4'), ('J5','J5'), ('J6','J6'), ('J7','J7'), ('J8','J8'), ('J9','J9'),
            ('K1','K1'), ('K2','K2'), ('K3','K3'), ('K4','K4'), ('K5','K5'), ('K6','K6'), ('K7','K7'), ('K8','K8'), ('K9','K9'),
            ('L1','L1'), ('L2','L2'), ('L3','L3'), ('L4','L4'), ('L5','L5'), ('L6','L6'), ('L7','L7'), ('L8','L8'), ('L9','L9'),
            ('M1','M1'), ('M2','M2'), ('M3','M3'), ('M4','M4'), ('M5','M5'), ('M6','M6'), ('M7','M7'), ('M8','M8'), ('M9','M9'),
            ('N1','N1'), ('N2','N2'), ('N3','N3'), ('N4','N4'), ('N5','N5'), ('N6','N6'), ('N7','N7'), ('N8','N8'), ('N9','N9'),
            ('O1','O1'), ('O2','O2'), ('O3','O3'), ('O4','O4'), ('O5','O5'), ('O6','O6'), ('O7','O7'), ('O8','O8'), ('O9','O9'),
            ('P1','P1'), ('P2','P2'), ('P3','P3'), ('P4','P4'), ('P5','P5'), ('P6','P6'), ('P7','P7'), ('P8','P8'), ('P9','P9'),
            ('Q1','Q1'), ('Q2','Q2'), ('Q3','Q3'), ('Q4','Q4'), ('Q5','Q5'), ('Q6','Q6'), ('Q7','Q7'), ('Q8','Q8'), ('Q9','Q9'),
            ('R1','R1'), ('R2','R2'), ('R3','R3'), ('R4','R4'), ('R5','R5'), ('R6','R6'), ('R7','R7'), ('R8','R8'), ('R9','R9'),
            ('S1','S1'), ('S2','S2'), ('S3','S3'), ('S4','S4'), ('S5','S5'), ('S6','S6'), ('S7','S7'), ('S8','S8'), ('S9','S9'),
            ('T1','T1'), ('T2','T2'), ('T3','T3'), ('T4','T4'), ('T5','T5'), ('T6','T6'), ('T7','T7'), ('T8','T8'), ('T9','T9'),
            ('U1','U1'), ('U2','U2'), ('U3','U3'), ('U4','U4'), ('U5','U5'), ('U6','U6'), ('U7','U7'), ('U8','U8'), ('U9','U9'),
            ('V1','V1'), ('V2','V2'), ('V3','V3'), ('V4','V4'), ('V5','V5'), ('V6','V6'), ('V7','V7'), ('V8','V8'), ('V9','V9'),
            ('W1','W1'), ('W2','W2'), ('W3','W3'), ('W4','W4'), ('W5','W5'), ('W6','W6'), ('W7','W7'), ('W8','W8'), ('W9','W9'),
            ('X1','X1'), ('X2','X2'), ('X3','X3'), ('X4','X4'), ('X5','X5'), ('X6','X6'), ('X7','X7'), ('X8','X8'), ('X9','X9'),
            ('Y1','Y1'), ('Y2','Y2'), ('Y3','Y3'), ('Y4','Y4'), ('Y5','Y5'), ('Y6','Y6'), ('Y7','Y7'), ('Y8','Y8'), ('Y9','Y9'),
            ('Z1','Z1'), ('Z2','Z2'), ('Z3','Z3'), ('Z4','Z4'), ('Z5','Z5'), ('Z6','Z6'), ('Z7','Z7'), ('Z8','Z8'), ('Z9','Z9'))
        #





class storeSearchResultGeneratorLastPageGotZeroTest( AssertEmptyMixin, GetEbayCategoriesWebTestSetUp ):
    #
    ''' class for testing getSearchResultGenerator() last page got nothing '''
    #
    '''obsolete when the changes started in June 2021 are complete'''
    #
    def setUp(self):
        #
        super().setUp()
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
                   '016' ) )
        #
        QuietDump(
                sLastPageZeroEntries,
                SEARCH_FILES_ROOT, sTODAY, self.sExampleFile )
        #
        #

    def tearDown(self):
        #
        DeleteIfExists( SEARCH_FILES_ROOT, sTODAY, self.sExampleFile )

    def test_search_result_generator_last_page_got_zero(self):
        #
        sThisFileName = join( SEARCH_FILES_ROOT, sTODAY, self.sExampleFile )
        #
        oItemIter = getSearchResultGenerator( sThisFileName, 16 )
        #
        self.assertEmpty( tuple( oItemIter ) )




class storeSearchResultGeneratorSearchGotZeroTest( AssertEmptyMixin, GetEbayCategoriesWebTestSetUp ):
    #
    ''' class for testing getSearchResultGenerator() search got nothing '''
    #
    '''obsolete when the changes started in June 2021 are complete'''
    #
    def setUp(self):
        #
        super().setUp()
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
                   '001' ) )
        #
        QuietDump(
                sSuccessButZeroResults,
                SEARCH_FILES_ROOT, sTODAY, self.sExampleFile )
        #
        #

    def tearDown(self):
        #
        DeleteIfExists( SEARCH_FILES_ROOT, sTODAY, self.sExampleFile )

    def test_search_result_generator_search_got_zero(self):
        #
        sThisFileName = join( SEARCH_FILES_ROOT, sTODAY, self.sExampleFile )
        #
        oItemIter = getSearchResultGenerator( sThisFileName, 1 )
        #
        self.assertEmpty( tuple( oItemIter ) )



class storeSearchResultsWebTests( StoreSearchResultsTestsWebTestSetUp ):
    #

    def test_store_search_results(self):
        #
        ''' test storeSearchResultsInFinders() with actual record'''
        #
        #print('')
        #print( 'self.oSearch.id:', self.oSearch.id )
        #
        iCountItems, iStoreItems, iStoreUsers = self.tMain
        #
        self.assertEqual( ItemFound.objects.count(), iCountItems )
        self.assertEqual( ItemFound.objects.count(), iStoreItems )
        #
        self.assertEqual( UserItemFound.objects.count(), iStoreUsers )
        #
        # without ordering the search result, sometimes get error
        oSearchLogs = SearchLog.objects.all().order_by( 'tEndStore' )
        #
        self.assertEqual( len( oSearchLogs ), 2 )
        #
        oSearchLog = oSearchLogs[0]
        #
        sBeforeDash = getTextBefore( str(oSearchLog), ' -' )
        #
        self.assertTrue( isISOdatetime( sBeforeDash ) )
        #
        #if oSearchLog.iStoreItems != iExampleResponseCount:
            #print( 'got wrong store items count for id %s' % oSearchLog.id )
        self.assertEqual( oSearchLog.iItems,      iExampleResponseCount )
        self.assertEqual( oSearchLog.iStoreItems, iExampleResponseCount )
        self.assertEqual( oSearchLog.iStoreUsers, iExampleResponseCount )
        #
        # try again with the same data
        #
        #print( 'storing items in test_search' )
        t = ( storeSearchResultsInFinders(
                        self.oSearchMainLog.id,
                        self.sMarket,
                        self.user1.username,
                        self.oSearchMain.id,
                        self.oSearchMain.cTitle,
                        sTODAY,
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




class getImportSearchResultsTests( TestCasePlus ):
    #
    def test_get_search_results(self):
        '''test readin an example search results file'''
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        QuietDump( sExampleResponse, *tExampleFile )
        #
        itemResultsIterator = getSearchResultGenerator(
             join( *tExampleFile ), 0 )
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
        # DeleteIfExists( SEARCH_FILES_ROOT, sTODAY, sExampleFile )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )




class SearchFilesTesting( TestCasePlus ):
    '''test new scheme for storing search files'''

    def test_got_search_file_dirs( self ):
        #
        sTestSearchSubDir = split( tExampleFile[0] )[ -1 ]
        #
        self.assertIn( sTestSearchSubDir, getSearchRootFolders() )
