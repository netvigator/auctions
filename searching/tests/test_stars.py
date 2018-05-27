#import inspect

from os.path            import join

from django.core.urlresolvers import reverse

from django.utils       import timezone

from core.utils_test    import setUpBrandsCategoriesModels

from searching          import RESULTS_FILE_NAME_PATTERN, SEARCH_FILES_FOLDER

from ..models           import ( ItemFound, UserItemFound,
                                 ItemFoundTemp )
from ..tests            import sResponseSearchTooBroad
from ..utils            import storeSearchResultsInDB

from .test_utils        import GetBrandsCategoriesModelsSetUp

from ..utils_stars      import ( getFoundItemTester, _getRegExSearchOrNone,
                                 findSearchHits, _getRowRegExpressions )


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
        DeleteIfExists( SEARCH_FILES_FOLDER, self.sExampleFile )
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
        oFisherSpeakers = oTube5R4GB = oTube12SN7 = oAltecHorn = None
        oFisher100s = oAltecItem1 = oAltecItem2 = oAltecItem3 = None
        oTube6BH6 = None
        #
        setItemsToTest = frozenset(
              ( 282602694679,
                253486571279,
                123046984227,
                192509883813,
                162988285719,
                332618106572,
                162988530803,
                232745789325,
                ) )
        #
        for oTemp in oUserItems:
            #
            #
            if oTemp.iHitStars == 0: break
            #
            if oTemp.iItemNumb_id in setItemsToTest:
                #
                if oTemp.iItemNumb_id == 282602694679:

                    if oAltecItem1 is not None:

                        oAltecItem2 = oTemp

                    else:

                        oAltecItem1 = oTemp

                elif oTemp.iItemNumb_id == 253486571279 :
                    oFisherSpeakers = oTemp
                elif oTemp.iItemNumb_id == 123046984227 :
                    oTube5R4GB      = oTemp
                elif oTemp.iItemNumb_id == 192509883813 :
                    oFisher100s     = oTemp
                elif oTemp.iItemNumb_id == 162988285719 :
                    oTube12SN7      = oTemp
                elif oTemp.iItemNumb_id == 332618106572 :
                    oTube6BH6       = oTemp
                elif oTemp.iItemNumb_id == 162988530803 :
                    oAltecHorn      = oTemp
                #
                elif oTemp.iItemNumb_id == 232745789325 :
                    oAltecItem3     = oTemp
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
        #if oAltecItem1 is not None:
            #if oAltecItem1.iModel is not None:
                #print( oAltecItem1.iModel.cTitle )
            #else: print( 'oAltecItem1.iModel is None' )
            #if oAltecItem1.iCategory is not None:
                #print( oAltecItem1.iCategory.cTitle )
            #else: print( 'oAltecItem1.iCategory is None' )
            #print( oAltecItem1.iHitStars )
        #if oAltecItem3 is not None:
            #if oAltecItem3.iModel is not None:
                #print( oAltecItem3.iModel.cTitle )
            #else: print( 'oAltecItem3.iModel is None' )
            #if oAltecItem3.iCategory is not None:
                #print( oAltecItem3.iCategory.cTitle )
            #else: print( 'oAltecItem3.iCategory is None' )
            #print( 'oAltecItem3.iHitStars:', oAltecItem3.iHitStars )
        #
        self.assertGreater( iCount, 38 )
        #
        self.assertIsNotNone( oFisherSpeakers )
        #
        self.assertEqual( oFisherSpeakers.iModel.cTitle,    'XP-55-B' )
        #
        self.assertEqual( oFisherSpeakers.iBrand.cTitle,    'Fisher'  )
        #
        self.assertEqual( oFisherSpeakers.iCategory.cTitle, 'Speaker System')
        #
        self.assertEqual( oFisherSpeakers.cWhereCategory,   'title' )
        #
        self.assertTrue(   oFisherSpeakers.iHitStars > 100 )
        #
        self.assertIsNotNone( oTube5R4GB )
        #
        self.assertEqual( oTube5R4GB.iModel.cTitle,    '5R4GA' )
        #
        self.assertEqual( oTube5R4GB.iBrand.cTitle,    'GE'    )
        #
        self.assertEqual( oTube5R4GB.iCategory.cTitle, 'Vacuum Tube' )
        #
        self.assertEqual( oTube5R4GB.cWhereCategory,   'title' )
        #
        self.assertTrue(   oTube5R4GB.iHitStars > 100 )
        #
        self.assertIsNotNone( oTube12SN7 )
        #
        self.assertEqual( oTube12SN7.iModel.cTitle,    '12SN7' )
        #
        self.assertEqual( oTube12SN7.iBrand.cTitle,    'RCA'   )
        #
        self.assertEqual( oTube12SN7.iCategory.cTitle, 'Vacuum Tube' )
        #
        self.assertIsNotNone( oAltecItem1 )
        #
        self.assertIn( oAltecItem1.iModel.cTitle, ( 'N-1500A', '604E' ) )
        #
        self.assertIn( oAltecItem1.iCategory.cTitle, ( 'Driver', 'Crossover' ) )
        #
        self.assertIsNotNone( oAltecItem2 )
        #
        self.assertIn( oAltecItem2.iModel.cTitle, ( 'N-1500A', '604E' ) )
        #
        self.assertIn( oAltecItem2.iCategory.cTitle, ( 'Driver', 'Crossover' ) )
        #
        self.assertIsNotNone( oFisher100s )
        #
        self.assertEqual( oFisher100s.iModel.cTitle,    '100 (speaker)' )
        #
        self.assertEqual( oFisher100s.iBrand.cTitle,    'Fisher' )
        #
        self.assertEqual( oFisher100s.iCategory.cTitle, 'Speaker System' )
        #
        self.assertIsNotNone( oTube6BH6 )
        #
        self.assertEqual( oTube6BH6.iModel.cTitle,    '6BH6' )
        #
        self.assertEqual( oTube6BH6.iCategory.cTitle, 'Vacuum Tube' )
        #
        self.assertEqual( oTube6BH6.cWhereCategory,   'heirarchy1' )
        #
        self.assertEqual( oTube6BH6.iBrand.cTitle,    'RCA'    )
        #
        self.assertIsNotNone( oAltecHorn )
        #
        self.assertEqual( oAltecHorn.iModel.cTitle,    '311-90' )
        #
        self.assertEqual( oAltecHorn.iCategory.cTitle, 'Horn' )
        #
        self.assertEqual( oAltecHorn.cWhereCategory,   'title' )
        #
        self.assertEqual( oAltecHorn.iBrand.cTitle,    'Altec-Lansing' )
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
        self.assertEqual( self.oModel.cRegExExclude, r'\bgolf\b' )
        self.assertEqual( self.oModel.cRegExKeyWords, 'Eldorado' )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


