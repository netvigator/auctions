from os.path            import join

from core.dj_import     import reverse

from django.db.models   import Max
from django.http        import HttpResponseRedirect
from django.urls        import reverse_lazy

from core.utils_test    import ( setup_view_for_tests,
                                 GetEbayCategoriesWebTestSetUp,
                                 AssertEmptyMixin )

from core.utils         import getShrinkItemURL

from searching          import RESULTS_FILE_NAME_PATTERN
from searching          import SEARCH_FILES_FOLDER

from ..models           import Search
from ..tests            import sLastPageZeroEntries, sSuccessButZeroResults
from ..utils            import ( getIdStrZeroFilled, getSearchIdStr,
                                 getHowManySearchDigitsNeeded )
from ..utilsearch       import getPriorityChoices, getSearchResultGenerator
from ..utils_test       import BaseUserWebTestCaseCanAddSearches
from ..views            import SearchCreateView

from File.Del           import DeleteIfExists
from File.Write         import QuietDump


class TestHowManyUserDigitsNeeded( BaseUserWebTestCaseCanAddSearches ):
    ''' test getHowManySearchDigitsNeeded() '''

    def test_how_many_digits_needed( self ):
        #
        # several Searches could have been created & destroyed already
        # pk gets incrememted, could be over 10
        #
        self.assertIn( getHowManySearchDigitsNeeded(), (1,2) )
        #
        for i in range( 3, 10 ):
            #
            self.addSearch( "My clever search %s" % i, 'A%s' % i, self.user1 )
        #
        self.assertEqual( getHowManySearchDigitsNeeded(), 2 )
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
    ''' class for testing storeSearchResultsInDB() store records '''
    #
    def setUp(self):
        #
        super( storeSearchResultGeneratorLastPageGotZeroTest, self ).setUp()
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
        QuietDump( sLastPageZeroEntries, SEARCH_FILES_FOLDER, self.sExampleFile )
        #
        #

    def tearDown(self):
        #
        DeleteIfExists( SEARCH_FILES_FOLDER, self.sExampleFile )

    def test_search_result_generator_last_page_got_zero(self):
        #
        sThisFileName = join( SEARCH_FILES_FOLDER, self.sExampleFile )
        #
        oItemIter = getSearchResultGenerator( sThisFileName, 16 )
        #
        self.assertEmpty( tuple( oItemIter ) )




class storeSearchResultGeneratorSearchGotZeroTest( AssertEmptyMixin, GetEbayCategoriesWebTestSetUp ):
    #
    ''' class for testing storeSearchResultsInDB() store records '''
    #
    def setUp(self):
        #
        super( storeSearchResultGeneratorSearchGotZeroTest, self ).setUp()
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
        QuietDump( sSuccessButZeroResults, SEARCH_FILES_FOLDER, self.sExampleFile )
        #
        #

    def tearDown(self):
        #
        DeleteIfExists( SEARCH_FILES_FOLDER, self.sExampleFile )

    def test_search_result_generator_search_got_zero(self):
        #
        sThisFileName = join( SEARCH_FILES_FOLDER, self.sExampleFile )
        #
        oItemIter = getSearchResultGenerator( sThisFileName, 1 )
        #
        self.assertEmpty( tuple( oItemIter ) )
