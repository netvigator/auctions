#import inspect

from os.path            import join

from django.core.urlresolvers import reverse

from django.test        import TestCase
from django.utils       import timezone

from core.utils_test    import setUpBrandsCategoriesModels

from searching          import RESULTS_FILE_NAME_PATTERN, SEARCH_FILES_FOLDER

from ..models           import ( ItemFound, UserItemFound,
                                 ItemFoundTemp )
from ..tests            import sResponseSearchTooBroad
from ..utils            import storeSearchResultsInDB

from .test_utils        import GetBrandsCategoriesModelsSetUp

from ..utils_stars      import ( getFoundItemTester, _getRegExSearchOrNone,
                                 findSearchHits, _getRowRegExpressions,
                                 getInParens )


from brands.views       import BrandUpdateView
from models.models      import Model

from File.Del           import DeleteIfExists
from File.Write         import QuietDump



def _getModelRegExFinders4Test( oModel ):
    #
    t = _getRowRegExpressions( oModel, bAddDash = True )
    #
    return tuple( map( _getRegExSearchOrNone, t ) )


def _getCategoryRegExFinders4Test( oCategory ):
    #
    t = _getRowRegExpressions( oCategory )
    #
    return tuple( map( _getRegExSearchOrNone, t ) )


def _getBrandRegExFinders4Test( oBrand ):
    #
    t = _getRowRegExpressions( oBrand )
    #
    sFindTitle, sFindExclude, sFindKeyWords = t
    #
    return tuple( map( _getRegExSearchOrNone, t[:2] ) )




class SetUpForKeyWordFindSearchHitsTests( GetBrandsCategoriesModelsSetUp ):
    #
    ''' class for testing storeSearchResultsInDB() store records '''
    #
    def setUp( self ):
        #
        super( SetUpForKeyWordFindSearchHitsTests, self ).setUp()
        #
        self.sExampleFile = (
            RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
            ( 'EBAY-US', self.user1.username, self.oSearch.id, '000' ) )
        #
        #print( 'will DeleteIfExists' )
        # DeleteIfExists( SEARCH_FILES_FOLDER, self.sExampleFile )
        #
        #print( 'will QuietDump' )
        QuietDump( sResponseSearchTooBroad, SEARCH_FILES_FOLDER, self.sExampleFile )
        #
        t = ( storeSearchResultsInDB(   self.oSearchLog.id,
                                        self.sMarket,
                                        self.user1.username,
                                        self.oSearch.id,
                                        self.oSearch.cTitle ) )
        #
        iCountItems, iStoreItems, iStoreUsers = t
        #
        # bCleanUpAfterYourself must be False or tests will fail!
        findSearchHits( self.user1.id, bCleanUpAfterYourself = False )
        #
        #print( '\n' )
        #print( 'setting up KeyWordFindSearchHitsTests' )

    def tearDown(self):
        #
        DeleteIfExists( SEARCH_FILES_FOLDER, self.sExampleFile )



class KeyWordFindSearchHitsTests( SetUpForKeyWordFindSearchHitsTests ):

    def test_find_search_hits_test(self):
        #
        ''' test _storeUserItemFound() with actual record'''
        #
        iTempItems = ItemFoundTemp.objects.all().count()
        #
        self.assertGreater( iTempItems, 80 )
        #
        iCount = Model.objects.all().count()
        #
        self.assertGreater( iCount, 160 )
        #
        oUserItems = UserItemFound.objects.filter(
                        iUser = self.user1 ).order_by( '-iHitStars' )
        #
        iCount = 0
        #
        dItemsToTest = dict.fromkeys(
              ( 282602694679,
                253486571279,
                123046984227,
                192509883813,
                162988285719,
                332618106572,
                162988530803,
                232745789325,
                283006362761,
                162988285720,
                162988285721,
                142842525513,
                263776955668
                ) )
        #
        for oTemp in oUserItems:
            #
            #
            if oTemp.iHitStars == 0: break
            #
            if oTemp.iItemNumb_id in dItemsToTest:
                #
                if (    dItemsToTest[ oTemp.iItemNumb_id ] and
                        oTemp.iItemNumb_id == 282602694679 ):
                    #
                    dItemsToTest[ ( 282602694679, 2 ) ] = oTemp
                    #
                else:
                    #
                    dItemsToTest[ oTemp.iItemNumb_id ] = oTemp
                    #
                #
                #print( '' )

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
                    #oTemp.tLook4Hits.strftime('%Y-%m-%d %H:%M:%S'))
                #print( 'Auction End  :', oTemp.iItemNumb.tTimeEnd)
            #
            iCount += 1
        #
        self.assertGreater( iCount, 38 )
        #
        oTest = dItemsToTest[ 253486571279 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle,    'XP-55-B' )
        #
        self.assertEqual( oTest.iBrand.cTitle,    'Fisher'  )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System')
        #
        self.assertEqual( oTest.cWhereCategory,   'title' )
        #
        self.assertTrue(   oTest.iHitStars > 100 )
        #
        oTest = dItemsToTest[ 123046984227 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle,    '5R4GA' )
        #
        self.assertEqual( oTest.iBrand.cTitle,    'GE'    )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        self.assertEqual( oTest.cWhereCategory,   'title' )
        #
        self.assertTrue(   oTest.iHitStars > 100 )
        #
        oTest = dItemsToTest[ 162988285719 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle,    '12SN7' )
        #
        self.assertEqual( oTest.iBrand.cTitle,    'RCA'   )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ 282602694679 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertIn( oTest.iModel.cTitle, ( 'N-1500A', '604E' ) )
        #
        self.assertIn( oTest.iCategory.cTitle, ( 'Driver', 'Crossover' ) )
        #
        oAltecItem1 = oTest
        #
        oTest = dItemsToTest[ ( 282602694679, 2 ) ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertIn( oTest.iModel.cTitle, ( 'N-1500A', '604E' ) )
        #
        self.assertIn( oTest.iCategory.cTitle, ( 'Driver', 'Crossover' ) )
        #
        oAltecItem2 = oTest
        #
        self.assertFalse( oAltecItem1.iModel == oAltecItem2.iModel )
        #
        self.assertFalse( oAltecItem1.iCategory == oAltecItem2.iCategory )
        #
        oTest = dItemsToTest[ 192509883813 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle,    '100 (speaker)' )
        #
        self.assertEqual( oTest.iBrand.cTitle,    'Fisher' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        oTest = dItemsToTest[ 332618106572 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle,    '6BH6' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        self.assertEqual( oTest.cWhereCategory,   'heirarchy1' )
        #
        self.assertEqual( oTest.iBrand.cTitle,    'RCA'    )
        #
        oTest = dItemsToTest[ 162988530803 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle,    '311-90' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Horn' )
        #
        self.assertEqual( oTest.cWhereCategory,   'title' )
        #
        self.assertEqual( oTest.iBrand.cTitle,    'Altec-Lansing' )
        #
        oTest = dItemsToTest[ 283006362761 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Harman-Kardon' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'Citation III-X' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Tuner' )
        #
        #
        oTest = dItemsToTest[ 162988285720 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        #
        self.assertEqual( oTest.iModel.cTitle, '5881' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ 162988285721 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        #
        self.assertEqual( oTest.iModel.cTitle, '6L6WGB' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ 142842525513 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        #
        self.assertEqual( oTest.iModel.cTitle, '6AU6A' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ 263776955668 ]
        #
        self.assertIsNotNone( oTest )
        #
        # self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        #
        # self.assertEqual( oTest.iModel.cTitle, '6AU6A' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )





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
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


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
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



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
        self.oModel.refresh_from_db()
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
        #

    def testBrandGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oBrand, dFinders )
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( sInTitle     )
        self.assertTrue(  bExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( bExcludeThis )
        #
        foundItem = dFinders[ self.oBrand.pk ]
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( bExcludeThis )
        #
        self.assertIn(     self.oBrand.cRegExLook4Title,
                            ( r'Cadillac|\bCaddy\b', r'\bCaddy\b|Cadillac') )
        #
        self.assertEqual( self.oBrand.cRegExExclude, r'\bgolf\b' )
        #
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



    def testCategoryGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oCategory, dFinders )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'Gemini Jets 1/200 Delta MD-80 Widget Livery N956DL'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( sInTitle     )
        self.assertTrue(  bExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( sInTitle     )
        self.assertFalse( bExcludeThis )
        #
        foundItem = dFinders[ self.oCategory.pk ]
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( bExcludeThis )
        #
        self.assertIn(     self.oCategory.cRegExLook4Title,
                                ( r'\bGizmo\b|Widget', r'Widget|\bGizmo\b' ) )
        #
        self.assertEqual( self.oCategory.cRegExExclude,  r'\bDelta\b'  )
        self.assertEqual( self.oCategory.cRegExKeyWords,    'Gadget' )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def testModelGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oModel, dFinders )
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( sInTitle     )
        self.assertTrue(  bExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( sInTitle     )
        self.assertFalse( bExcludeThis )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertFalse( sInTitle     )
        self.assertFalse( bExcludeThis )
        #
        foundItem = dFinders[ self.oModel.pk ]
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( bExcludeThis )
        #
        self.assertIn(     self.oModel.cRegExLook4Title,
                                ( 'Woodie|Fleetwood', 'Fleetwood|Woodie' ) )
        #
        self.assertEqual( self.oModel.cRegExExclude, r'tournament|\bgolf\b' )
        self.assertEqual( self.oModel.cRegExKeyWords, 'Eldorado' )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


class GetTextInParensTest( TestCase ):
    #
    def test_got_text_in_parens_or_not( self ):
        #
        s1 = ( 'Tung-Sol 5881 (6L6WGB) amplifier tube. '
               'TV-7 test NOS. for Bendix USA SHIPS ONLY' )
        #
        s2 = ( 'ALTEC LANSING N-800-8K CROSSOVER DIVIDING NETWORK '
               '846B VALENCIA WORKING PAIR' )
        #
        self.assertEqual( getInParens( s1 ), '6L6WGB' )
        #
        self.assertIsNone( getInParens( s2 ) )
