#import inspect

from os.path            import join

from pprint             import pprint

from django.urls        import reverse
from django.utils       import timezone

from core.utils         import maybePrint
from core.tests.base    import ( SetUpBrandsCategoriesModelsWebTest,
                                 AssertEmptyMixin, AssertNotEmptyMixin,
                                 TestCasePlus )

from finders.models     import ( ItemFound, UserItemFound, ItemFoundTemp,
                                 UserFinder )

from .base              import ( PutSearchResultsInDatabaseWebTestBase,
                                 SetUpForHitStarsWebTests,
                                 StoreUserItemFoundWebTestBase )

from ..utils_stars      import ( getFoundItemTester, findSearchHits,
                                 _getRowRegExpressions, _getRelevantTitle )

from searching.tests    import iRecordStepsForThis

from brands.views       import BrandUpdateView
from models.models      import Model

from pyPks.String.Find  import getRegExpress, getRegExObj


def _getRegExSearchOrNone( s ):
    #
    if s:
        #
        oRegExObj = getRegExObj( s )
        #
        return oRegExObj.search


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
    t = _getRowRegExpressions( oBrand, bAddDash = True  )
    #
    sFindTitle, sFindExclude, sFindKeyWords = t
    #
    return tuple( map( _getRegExSearchOrNone, t[:2] ) )


class MakeSureExampleItemGetsHit( StoreUserItemFoundWebTestBase ):
    #
    ''' class for testing dSearchResult in __init__  '''
    #

    def test_find_search_hits( self ):
        #
        qsUserItemFound = UserItemFound.objects.filter(
                            iItemNumb_id    = 282330751118,
                            iUser           = self.user1 )
        #
        findSearchHits( self.user1.id,
                        bCleanUpAfterYourself   = True,
                        iRecordStepsForThis     = iRecordStepsForThis )
        #
        qsUserFinder = UserFinder.objects.filter(
                            iItemNumb_id    = 282330751118,
                            iUser           = self.user1 )
        #
        self.assertTrue( qsUserFinder.exists() )
        #
        qsUserItemFound = UserItemFound.objects.filter(
                            iItemNumb_id    = 282330751118,
                            iUser           = self.user1 )
        #
        self.assertTrue( qsUserItemFound.exists() )
        #
        self.assertTrue(
            UserItemFound.objects.filter(
                tLook4Hits__isnull = False ).exists() )
        #




class FindSearchHitsWebTests( AssertNotEmptyMixin, SetUpForHitStarsWebTests ):

    def print_len( self, lTest, iExpect, iItemNumb = None, sExplain = None ):
        #
        if not lTest:
            #
            maybePrint('')
            #
            if iItemNumb:
                maybePrint( 'found nothing for %s' % iItemNumb )
            else:
                maybePrint( 'found nothing, iItemNumb not passed' )
            #
        elif len( lTest ) != iExpect:
            #
            maybePrint('')
            maybePrint(lTest[0])
            maybePrint( '%s length:' % lTest[0].iItemNumb_id,
                   len( lTest ),
                   'expected:',
                   iExpect )
            #
            if len( lTest ) > 1 or len( lTest ) < iExpect:
                #
                for o in lTest:
                    #
                    lPrintThis = []
                    #
                    if o.iModel:
                        lPrintThis.append( o.iModel.cTitle )
                    if o.iBrand:
                        lPrintThis.append( o.iBrand.cTitle )
                    if o.iCategory:
                        lPrintThis.append( o.iCategory.cTitle )
                    #
                    if lPrintThis:
                        #
                        maybePrint( ' | '.join( lPrintThis ) )
                        #
                    #
                #
            #
            if sExplain: maybePrint( sExplain )
            #

    def test_find_search_hits_count( self ):
        #
        self.assertGreater(
            len( UserItemFound.objects.filter(
                tLook4Hits__isnull = False ) ), 100 )
        #
        self.assertGreater(
            len( UserFinder.objects.filter( iUser = self.user1 ) ), 80 )
        #


    def test_find_search_hits_test(self):
        #
        ''' test _storeUserItemFound() with actual record'''
        #
        iTempItems = ItemFoundTemp.objects.all().count()
        #
        self.assertGreater( iTempItems, 80 )
        #
        #
        qsUserItems = UserItemFound.objects.filter(
                        iUser = self.user1,
                        iHitStars__gt = 0 ).order_by( 'iHitStars' )
        #
        iCount = 0
        #
        dItemsToTest = {}
        #
        for oTemp in qsUserItems:
            #
            if oTemp.iHitStars == 0: continue
            #
            dItemsToTest.setdefault( oTemp.iItemNumb_id, [] ).append( oTemp )
            #
            iCount += 1
            #
        #
        dTitles = {}
        #
        for iItemNumb in dItemsToTest.keys():
            #
            oItem = ItemFound.objects.get( iItemNumb = iItemNumb )
            #
            sTitle = oItem.cTitle.upper()
            #
            dTitles.setdefault( sTitle, [] ).append( iItemNumb )
            #
        #
        lDupes = []
        #
        for sTitle, lItemNumbs in dTitles.items():
            #
            if len( lItemNumbs ) > 1:
                #
                lDupes.append( sTitle )
            #
        #
        if lDupes:
            #
            maybePrint()
            maybePrint( 'Duplicated test titles:', '\n', '\n'.join( lDupes ) )
            #
        #
        self.assertGreater( iCount, 38 )
        #
        self.print_len( dItemsToTest[ 253486571279 ], 1 )
        #
        oTest = dItemsToTest[ 253486571279 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle,    'XP-55B' )
        #
        self.assertEqual( oTest.iBrand.cTitle,    'Fisher'  )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System')
        #
        self.assertEqual( oTest.cWhereCategory,   'title' )
        #
        self.assertTrue(   oTest.iHitStars > 100 )
        #
        self.print_len( dItemsToTest[ 123046984227 ], 1 )
        #
        oTest = dItemsToTest[ 123046984227 ][ 0 ]
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
        self.print_len( dItemsToTest[ 162988285719 ], 1 )
        #
        oTest = dItemsToTest[ 162988285719 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle,    '12SN7' )
        #
        self.assertEqual( oTest.iBrand.cTitle,    'RCA'   )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        self.print_len( dItemsToTest[ 282602694679 ], 2 )
        #
        #
        oTest = dItemsToTest[ 282602694679 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle,      'N-1500A' )
        #
        self.assertEqual( oTest.iCategory.cTitle,   'Crossover' )
        #
        self.assertEqual( oTest.iBrand.cTitle,      'Altec-Lansing' )
        #
        oTest = dItemsToTest[ 282602694679 ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle,      'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle,      '604E' )
        #
        self.assertEqual( oTest.iCategory.cTitle,   'Driver' )
        #
        #
        self.print_len( dItemsToTest[ 192509883813 ], 1 )
        #
        oTest = dItemsToTest[ 192509883813 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle,    '100 (speaker)' )
        #
        self.assertEqual( oTest.iBrand.cTitle,    'Fisher' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        self.print_len( dItemsToTest[ 332618106572 ], 1 )
        #
        oTest = dItemsToTest[ 332618106572 ][ 0 ]
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
        self.print_len( dItemsToTest[ 162988530803 ], 1 )
        #
        oTest = dItemsToTest[ 162988530803 ][ 0 ]
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
        self.print_len( dItemsToTest[ 283006362761 ], 1 )
        #
        oTest = dItemsToTest[ 283006362761 ][ 0 ]
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
        self.print_len( dItemsToTest[ 162988285720 ], 1 )
        #
        oTest = dItemsToTest[ 162988285720 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        #
        self.assertEqual( oTest.iModel.cTitle, '5881' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        self.print_len( dItemsToTest[ 142842525513 ], 1 )
        #
        oTest = dItemsToTest[ 142842525513 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        #
        self.assertEqual( oTest.iModel.cTitle, '6AU6A' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        self.print_len( dItemsToTest[ 263776955668 ], 1 )
        #
        oTest = dItemsToTest[ 263776955668 ][ 0 ]
        #
        # Lot of 10 should not find vacuum tube type 10
        #
        self.assertIsNotNone( oTest )
        #
        self.assertIsNone( oTest.iModel )
        #
        iThisOne = 192577735613
        #
        self.print_len( dItemsToTest[ iThisOne ], 2,
                       'expecting both Philips & Mullard' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertIn( oTest.iBrand.cTitle, ( 'Philips', 'Mullard' ) )
        #
        self.assertEqual( oTest.iModel.cTitle, '6AU6A' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIn( oTest.iBrand.cTitle, ( 'Philips', 'Mullard' ) )
        #
        self.assertEqual( oTest.iModel.cTitle, '6AU6A' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        self.print_len( dItemsToTest[ 173375697400 ], 1 )
        #
        oTest = dItemsToTest[ 173375697400 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        oItemFound = ItemFound.objects.get( pk = oTest.iItemNumb_id )
        #
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        #
        self.assertEqual( oTest.iModel.cTitle, 'H-222' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        self.print_len( dItemsToTest[ 162988285721 ], 2 )
        #
        oTest = dItemsToTest[ 162988285721 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        #
        self.assertEqual( oTest.iModel.cTitle, '5881' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ 162988285721 ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        #
        self.assertEqual( oTest.iModel.cTitle, '6L6WGB' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        self.print_len( dItemsToTest[ 273340636575 ], 1 )
        #
        oTest = dItemsToTest[ 273340636575 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Supreme' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'TV-7' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Tube Tester' )
        #
        #
        iThisOne = 292640430401
        #
        self.print_len( dItemsToTest[ iThisOne ], 9, iThisOne,
                       'ideally should find crossovers' )
        #
        oTest = dItemsToTest[ 292640430401 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        #self.assertEqual( oTest.iModel.cTitle, 'M1131' )
        ##
        #self.assertEqual( oTest.iCategory.cTitle, 'Choke' )
        ##
        #oTest = dItemsToTest[ 292640430401 ][ 1 ]
        ##
        #self.assertIsNotNone( oTest )
        ##
        #self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        ##
        #self.assertIn( oTest.iModel.cTitle, 'A-61' )
        ##
        #self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        ##
        #oTest = dItemsToTest[ 292640430401 ][ 2 ]
        ##
        #self.assertIsNotNone( oTest )
        ##
        #self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        ##
        #self.assertEqual( oTest.iModel.cTitle, 'A-402' )
        ##
        #self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        ##
        #oTest = dItemsToTest[ 292640430401 ][ 3 ]
        ##
        #self.assertIsNotNone( oTest )
        ##
        #self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        #self.assertEqual( oTest.iModel.cTitle, 'Imperial' )
        ##
        #self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        self.print_len( dItemsToTest[ 113173838358 ], 2 )
        #
        oTest = dItemsToTest[ 113173838358 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, '811B' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Horn' )
        #
        oTest = dItemsToTest[ 113173838358 ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle, '806A' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        #
        #
        #
        #
        #
        self.print_len( dItemsToTest[ 273380279306 ], 2 )
        #
        oTest = dItemsToTest[ 273380279306 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, '542' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Horn' )
        #
        oTest = dItemsToTest[ 273380279306 ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, '288-8F' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        self.print_len( dItemsToTest[ 153121548106 ], 2 )
        #
        oTest = dItemsToTest[ 153121548106 ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tannoy' )
        #
        self.assertIn( oTest.iModel.cTitle, ( 'GRF', '15" Silver' ) )
        #
        self.assertIn( oTest.iCategory.cTitle, ( 'Speaker Enclosure', 'Driver' ) )
        #
        oTest = dItemsToTest[ 153121548106 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tannoy' )
        #
        self.assertIn( oTest.iModel.cTitle, ( 'GRF', '15" Silver' ) )
        #
        self.assertIn( oTest.iCategory.cTitle, ( 'Speaker Enclosure', 'Driver' ) )
        #
        #
        #
        #
        iThisOne = 263861079618
        #
        self.print_len( dItemsToTest[ iThisOne ], 1 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'RCA' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        self.assertIsNone( oTest.iModel )
        #
        #
        #
        #
        iThisOne = 223093061969
        #
        self.print_len( dItemsToTest[ iThisOne ], 1 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'RCA' )
        #
        self.assertIsNone( oTest.iModel )
        #
        iThisOne = 263879319271
        #
        self.print_len( dItemsToTest[ iThisOne ], 1,iThisOne,
                'Marantz Model 240 Power Stereo Amplifier - not of interest' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '240' )
        self.assertIsNone( oTest.iBrand )
        self.assertIn( oTest.iCategory.cTitle, ( 'Amplifier', 'Preamp' ) )
        #
        #
        #
        #
        iThisOne = 163199461416 # keep this
        #
        self.print_len( dItemsToTest[ iThisOne ], 3 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'N-3000A' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, '601B (enclosure)' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker Enclosure' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, '601a (driver)' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        iThisOne = 202401940540
        #
        self.print_len( dItemsToTest[ iThisOne ], 3,
                       "JBL D130, 075 & N2600 X-Over" )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        #
        self.assertIn( oTest.iModel.cTitle, ( 'N2600', 'D-130', '75' ) )
        self.assertIn( oTest.iCategory.cTitle, ( 'Crossover', 'Driver' ) )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIn( oTest.iModel.cTitle, ( 'N2600', 'D-130', '75' ) )
        self.assertIn( oTest.iCategory.cTitle, ( 'Crossover', 'Driver' ) )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertIn( oTest.iModel.cTitle, ( 'N2600', 'D-130', '75' ) )
        self.assertIn( oTest.iCategory.cTitle, ( 'Crossover', 'Driver' ) )
        #
        iThisOne = 283100002617
        #
        self.print_len( dItemsToTest[ iThisOne ], 2 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Hickok' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'CA-5' )
        self.assertEqual( oTest.iCategory.cTitle, 'Accessory' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '539-B' )
        self.assertEqual( oTest.iCategory.cTitle, 'Tube Tester' )
        #
        #
        #
        #
        #
        iThisOne = 192633431454
        #
        self.print_len( dItemsToTest[ iThisOne ], 4 )
        #
        gotComponents = set( [] )
        gotCategories = set( [] )
        #
        setComponents = frozenset(
                ( 'C38 (Baron)', 'N2400', 'D-130', '75' ) )
        setCategories = frozenset(
                ( 'Crossover', 'Speaker Enclosure', 'Driver' ) )
        #
        for i in range( len( dItemsToTest[ iThisOne ] ) ):
            #
            oTest = dItemsToTest[ iThisOne ][ i ]
            #
            self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
            #
            self.assertIn( oTest.iModel.cTitle,    setComponents )
            self.assertIn( oTest.iCategory.cTitle, setCategories )
            #
            gotComponents.add( oTest.iModel.cTitle    )
            gotCategories.add( oTest.iCategory.cTitle )
        #
        self.assertEqual( gotComponents, setComponents )
        self.assertEqual( gotCategories, setCategories )
        #
        #
        iThisOne = 232913976977
        #
        self.print_len( dItemsToTest[ iThisOne ], 2 )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        #
        self.assertEqual( oTest.iModel.cTitle, '175' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '1217-1290' )
        self.assertEqual( oTest.iCategory.cTitle, 'Horn' )
        #
        #
        #
        #
        iThisOne = 323425124965
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne,
                       'ideally should find components' )
        # order not consistent
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Klipsch' )
        #
        setComponents = frozenset(
            ( 'Heresy (H700)', 'K-700', 'K-77', 'K-55-V', 'K-22' ) )
        #
        self.assertIn( oTest.iModel.cTitle, setComponents )
        self.assertIn( oTest.iCategory.cTitle, (
                'Horn', 'Driver', 'Speaker System' ) )
        #
        #oTest = dItemsToTest[ iThisOne ][ 1 ]
        ##
        #self.assertIn( oTest.iModel.cTitle, setComponents )
        #self.assertIn( oTest.iCategory.cTitle, (
                #'Horn', 'Driver', 'Speaker System' ) )
        ##
        #oTest = dItemsToTest[ iThisOne ][ 2 ]
        ##
        #self.assertIn( oTest.iModel.cTitle, setComponents )
        #self.assertIn( oTest.iCategory.cTitle, (
                #'Horn', 'Driver', 'Speaker System' ) )
        ##
        #oTest = dItemsToTest[ iThisOne ][ 3 ]
        ##
        #self.assertIn( oTest.iModel.cTitle, setComponents )
        #self.assertIn( oTest.iCategory.cTitle, (
                #'Horn', 'Driver', 'Speaker System' ) )
        ##
        #oTest = dItemsToTest[ iThisOne ][ 4 ]
        ##
        #self.assertIn( oTest.iModel.cTitle, setComponents )
        #self.assertIn( oTest.iCategory.cTitle, (
                #'Horn', 'Driver', 'Speaker System' ) )
        #
        #
        #
        iThisOne = 202430076409
        #
        self.print_len( dItemsToTest[ iThisOne ], 1 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Western Electric' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'KS-15874' )
        self.assertEqual( oTest.iCategory.cTitle, 'Tube Tester' )
        #
        #
        iThisOne = 323437473473
        #
        self.print_len( dItemsToTest[ iThisOne ], 1 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        self.assertEqual( oTest.iModel.cTitle, 'C45 (Metregon)' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker Enclosure' )
        #
        #
        #
        #
        #
        iThisOne = 192659380750
        #
        self.print_len( dItemsToTest[ iThisOne ], 1 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-5' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        #
        iThisOne = 183436307728
        #
        self.print_len( dItemsToTest[ iThisOne ], 2 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Hickok' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'CA-3' )
        self.assertEqual( oTest.iCategory.cTitle, 'Accessory' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '539-B' )
        self.assertEqual( oTest.iCategory.cTitle, 'Tube Tester' )
        #
        #
        #
        iThisOne = 192660195679 # keep this one
        #
        self.print_len( dItemsToTest[ iThisOne ], 1 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'XP-6A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        iThisOne = 173544935496
        #
        self.print_len( dItemsToTest[ iThisOne ], 2 )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'VT-107 (6V6 metal)' )
        self.assertEqual( oTest.iBrand.cTitle, 'RCA' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        iThisOne = 153200191510
        #
        self.print_len( dItemsToTest[ iThisOne ], 1 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        # should find 604 8G only
        self.assertEqual( oTest.iModel.cTitle, '604-8G' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        iThisOne = 192675470270
        #
        self.print_len( dItemsToTest[ iThisOne ], 1 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        # should not find A-8
        self.assertEqual(  oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertIsNone( oTest.iModel )
        self.assertIsNone( oTest.iCategory )
        #
        #
        #
        #
        #
        iThisOne = 352494035670
        #
        # Philips ECG JAN 12AX7WA 7025 12ax7 Vacuum Tubes
        #
        self.print_len( dItemsToTest[ iThisOne ], 3, iThisOne,
                        '12ax7 and 12AX7WA both are in the title' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7' )
        self.assertEqual( oTest.iBrand.cTitle, 'Philips' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '7025 (12AX7A)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Philips' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7-WA (Philips)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Philips' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 332849161811
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'XP-1A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        iThisOne = 323589685342 # also accessed in test_models.py
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'XP-1A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        iThisOne = 264048401593
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'XP-7A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        iThisOne = 382632483507
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'XP-7A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        iThisOne = 312339506602
        #
        self.print_len( dItemsToTest[ iThisOne ], 2, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        # should get 1005 horn
        #
        self.assertEqual( oTest.iModel.cTitle, '1005B' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Horn' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        # should get 1005 horn
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-7' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        iThisOne = 283272931267
        #
        self.print_len( dItemsToTest[ iThisOne ], 2, iThisOne,
                       'expecting both Valvo & Mullard ' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        # also listed 6267?, fixed in data
        self.assertEqual( oTest.iModel.cTitle, 'EF86' )
        self.assertEqual( oTest.iBrand.cTitle, 'Valvo' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        # also listed 6267?, fixed in data
        self.assertEqual( oTest.iModel.cTitle, 'EF86' )
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        iThisOne = 113392158472
        #
        self.print_len( dItemsToTest[ iThisOne ], 2, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        # should list 6L6GC, s/n list 6L6
        #
        self.assertEqual( oTest.iModel.cTitle, '6L6GC' )
        self.assertEqual( oTest.iBrand.cTitle, 'Raytheon' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 192748949221
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        # should list XP-6 not XP-8
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'XP-6A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        iThisOne = 192748960622
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        # fine point: should not list Sylvania 6SN7 GTB twice
        # for now, TOO fine!!!
        # another too fine for now below
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertIn( oTest.iModel.cTitle, ('6SN7GTB', '6SN7GT (Sylvania)' ))
        self.assertEqual( oTest.iBrand.cTitle, 'Sylvania' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        iThisOne = 352535627937
        #
        self.print_len( dItemsToTest[ iThisOne ], 4, iThisOne,
                       'should find both Sylvania & Marconi' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6V6G' )
        self.assertEqual( oTest.iBrand.cTitle, 'Sylvania' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6V6G' )
        self.assertEqual( oTest.iBrand.cTitle, 'Marconi' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        iThisOne = 123550734798
        #
        self.print_len( dItemsToTest[ iThisOne ], 3, iThisOne )
        #
        # should get all 3 brands, Tung-Sol, RCA & Raytheon
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7' )
        self.assertIn( oTest.iBrand.cTitle, ( 'Raytheon', 'Tung-Sol', 'RCA' ) )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7' )
        self.assertIn( oTest.iBrand.cTitle, ( 'Raytheon', 'Tung-Sol', 'RCA' ) )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7' )
        self.assertIn( oTest.iBrand.cTitle, ( 'Raytheon', 'Tung-Sol', 'RCA' ) )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        iThisOne = 303000971114
        #
        self.print_len( dItemsToTest[ iThisOne ], 2, iThisOne )
        #
        # should list 2 hits: 6CA7 & EL34
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'EL34' )
        self.assertEqual( oTest.iBrand.cTitle, 'Matsushita' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6CA7' )
        self.assertEqual( oTest.iBrand.cTitle, 'Matsushita' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        iThisOne = 173696834267
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        # d/n get into keepers
        #
        self.assertIn( oTest.iModel.cTitle, ( '12AU7A', 'ECC82' ) )
        self.assertEqual( oTest.iBrand.cTitle, 'Westinghouse' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        iThisOne = 372536713027
        #
        # d/n get into keepers
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6SN7GTB' )
        self.assertEqual( oTest.iBrand.cTitle, 'RCA' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        iThisOne = 303000959884
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        # d/n get into keepers
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6SN7GT (Sylvania)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Sylvania' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        # fine point: should not list Sylvania 6SN7 GTB twice
        # for now, TOO fine!!!
        # another too fine for now above
        #
        iThisOne = 173696832184
        #
        self.print_len( dItemsToTest[ iThisOne ], 4, iThisOne,
                       'should find E88CC 6922 & 6DJ8 for Philips & GE' )
        #
        setComponents   = frozenset( ( 'E88CC', '6922', '6DJ8' ) )
        setBrands       = frozenset( ( 'Philips', 'GE' ) )
        #
        gotComponents   = set( [] )
        gotBrands       = set( [] )
        #
        for i in range( len( dItemsToTest[ iThisOne ] ) ):
            #
            oTest = dItemsToTest[ iThisOne ][ i ]
            #
            self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
            #
            self.assertIn( oTest.iModel.cTitle, setComponents )
            self.assertIn( oTest.iBrand.cTitle, setBrands     )
            #
            gotComponents.add( oTest.iModel.cTitle )
            gotBrands.add(     oTest.iBrand.cTitle )
        #
        self.assertEqual( gotComponents, setComponents )
        self.assertEqual( gotBrands,     setBrands     )
        #
        #
        #
        #
        #
        iThisOne = 312417181299
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne,
                    'says Marantz 240 s/n find Marantz 2' )
        #
        #
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '240' )
        self.assertIsNone( oTest.iBrand )
        self.assertIn( oTest.iCategory.cTitle, ( 'Amplifier', 'Preamp' ) )
        #
        #
        #
        iThisOne = 312436313310
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        # says Marantz 240 s/n find Marantz 2
        #
        #
        iThisOne = 223348187115
        #
        self.print_len( dItemsToTest[ iThisOne ], 3, iThisOne )
        #
        # expecting lots of stars for 606 cabinet
        #
        gotComponents = set( [] )
        gotCategories = set( [] )
        #
        setComponents = frozenset(
                ( '602A', '606', 'N-3000A' ) )
        setCategories = frozenset(
                ( 'Speaker Enclosure', 'Driver', 'Crossover' ) )
        #
        for i in range( len( dItemsToTest[ iThisOne ] ) ):
            #
            oTest = dItemsToTest[ iThisOne ][ i ]
            #
            self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
            #
            self.assertIn( oTest.iModel.cTitle,    setComponents )
            self.assertIn( oTest.iCategory.cTitle, setCategories )
            #
            gotComponents.add( oTest.iModel.cTitle    )
            gotCategories.add( oTest.iCategory.cTitle )
            #
        #
        self.assertEqual( gotComponents, setComponents )
        self.assertEqual( gotCategories, setCategories )
        #
        #
        iThisOne = 323681140009
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        # s/n find Marantz Model 1 !!!
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Marantz' )
        self.assertIsNone( oTest.iModel )
        self.assertIsNone( oTest.iCategory )
        #
        iThisOne = 293004871422
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        # should find LE-5
        #
        self.assertEqual( oTest.iModel.cTitle, 'LE5-5' )
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        iThisOne = 133004653920
        #
        self.print_len( dItemsToTest[ iThisOne ], 2, iThisOne )
        #
        # should find driver and crossover
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'N-1600A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '604D' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        iThisOne = 202636634682
        #
        self.print_len(
            dItemsToTest[ iThisOne ], 1, iThisOne,
            'should not find AR-2' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertIsNone( oTest.iModel )
        self.assertIsNone( oTest.iBrand )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        iThisOne = 192878961826
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        # should find tweeter not speaker system
        #
        self.assertEqual( oTest.iModel.cTitle, 'RP-302A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #oTest = dItemsToTest[ iThisOne ][ 1 ]
        ##
        #self.assertIsNotNone( oTest )
        ##
        #self.assertEqual( oTest.iModel.cTitle, 'Imperial' )
        #self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        iThisOne = 401777677255
        #
        self.print_len( dItemsToTest[ iThisOne ], 2, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'N-3000A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle, '890' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker Enclosure' )
        #
        #
        iThisOne = 123790646318
        #
        self.print_len( dItemsToTest[ iThisOne ], 3, iThisOne )
        #
        # should find 601A driver not 601 enclosure!!!
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'N-3000A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle, '601B (enclosure)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker Enclosure' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '601a (driver)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        iThisOne = 223539937147
        #
        self.print_len( dItemsToTest[ iThisOne ], 2, iThisOne )
        #
        # should find both 601A driver and 601 enclosure
        # should Altec Lansing not Lansing
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '601B (enclosure)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker Enclosure' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iModel.cTitle, '601a (driver)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        iThisOne = 173922031351
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        # should find Jim Lansing driver
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '150-4B' )
        self.assertEqual( oTest.iBrand.cTitle, 'Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        iThisOne = 123795331323
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        # ALTEC 755A Loudspeaker Unit same as Western Electric 755A
        # got Altec so "same as" should exclude WE
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '755' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        iThisOne = 293128761816
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find ALTEC N-500-C NETWORK CROSSOVER w/803B WOOFER' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertIn(    oTest.iModel.cTitle, ( '803B (horn)', 'N-500B' ) )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertIn(    oTest.iCategory.cTitle, ( 'Horn', 'Crossover' ) )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIn(    oTest.iModel.cTitle, ( '803B (horn)', 'N-500B' ) )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertIn(    oTest.iCategory.cTitle, ( 'Horn', 'Crossover' ) )
        #
        #
        #
        #
        iThisOne = 264395445356
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should not find TV-7' )
        #
        # 2 RCA Type 83 JAN mil grade rectifier tubes.For Hickok,TV-7 tube testers
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '83' )
        self.assertEqual( oTest.iBrand.cTitle, 'RCA' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 383183181329
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'finding only Aperex BB brand & ECC88 + 6DJ8 BB is ideal' )
        #
        for i in range( len( dItemsToTest[ iThisOne ] ) ):
            #
            oTest = dItemsToTest[ iThisOne ][ i ]
            #
            self.assertIn(    oTest.iModel.cTitle,
                              ( '6DJ8', '6DJ8 (Bugle Boy)', 'ECC88' ) )
            self.assertEqual( oTest.iBrand.cTitle, 'Amperex (Bugle Boy)' )
            self.assertEqual( oTest.iCategory.cTitle, ( 'Vacuum Tube' ) )
        #
        #
        #
        #
        iThisOne = 323923889701
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 3, iThisOne,
                'should find 3 Fisher models FM-1000 400-CX & SA-1000' )
        #
        gotComponents = set( [] )
        gotCategories = set( [] )
        #
        setComponents = frozenset(
                ( 'FM-1000', 'SA-1000', '400-CX' ) )
        setCategories = frozenset(
                ( 'Tuner', 'Amplifier', 'Preamp' ) )
        #
        for i in range( len( dItemsToTest[ iThisOne ] ) ):
            #
            oTest = dItemsToTest[ iThisOne ][ i ]
            #
            self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
            #
            self.assertIn( oTest.iModel.cTitle,    setComponents )
            self.assertIn( oTest.iCategory.cTitle, setCategories )
            #
            gotComponents.add( oTest.iModel.cTitle    )
            gotCategories.add( oTest.iCategory.cTitle )
            #
        #
        self.assertEqual( gotComponents, setComponents )
        self.assertEqual( gotCategories, setCategories )
        #
        #
        iThisOne = 143400343473
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 3, iThisOne,
                'should find Klipsch K-77 and EV / University T35' )
        #
        gotComponents   = set( [] )
        gotCategories   = set( [] )
        gotBrands       = set( [] )
        #
        setComponents   = frozenset(( 'K-77', ) ) #  'T-35B'
        # 'Heresy (H700)',
        setCategories   = frozenset( ( 'Driver', ) )
        # 'Speaker System'
        #
        setBrands       = frozenset(
                ( 'Klipsch', 'University', 'Electro-Voice' ) )
        #
        for i in range( len( dItemsToTest[ iThisOne ] ) ):
            #
            oTest = dItemsToTest[ iThisOne ][ i ]
            #
            self.assertIn( oTest.iBrand.cTitle,    setBrands     )
            self.assertIn( oTest.iModel.cTitle,    setComponents )
            self.assertIn( oTest.iCategory.cTitle, setCategories )
            #
            gotComponents.add( oTest.iModel.cTitle    )
            gotCategories.add( oTest.iCategory.cTitle )
            gotBrands.add(     oTest.iBrand.cTitle    )
            #
        #
        self.assertEqual( gotComponents, setComponents )
        self.assertEqual( gotCategories, setCategories )
        self.assertTrue(  gotBrands   <= setBrands     )
        #
        #
        #
        iThisOne = 283636126401
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 4, iThisOne,
                'should find LE5-9 midrange' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'LE5-5' )
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        iThisOne = 202796135729
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find LK-72 integrated amp' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'LK-72' )
        self.assertEqual( oTest.iBrand.cTitle, 'Scott, H.H.' )
        self.assertEqual( oTest.iCategory.cTitle, 'Integrated Amp' )
        #
        #
        #
        iThisOne = 233369497398
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Pilot 240 integrated amp' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '240' )
        self.assertEqual( oTest.iBrand.cTitle, 'Pilot' )
        self.assertEqual( oTest.iCategory.cTitle, 'Integrated Amp' )
        #
        #
        #
        iThisOne = 123950129789
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Altec 1569A Amps' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '1569A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Theater Amp' )
        #
        #
        #
        iThisOne = 383228212021
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Patrician speaker system' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'Patrician' )
        self.assertEqual( oTest.iBrand.cTitle, 'Electro-Voice' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        iThisOne = 133227447968
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Altec A-7' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-7' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        iThisOne = 113945886050
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 3, iThisOne,
                'should find JBL L220' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'LE5-5' )
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '76' )
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'L220 (Oracle)' )
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        iThisOne = 193189027590
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find 604D & N-1600-B' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '604D' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        #
        iThisOne = 153708457263
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find 421A not 421' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '421A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        #
        iThisOne = 352786860975
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find AR-2 & AR-2x' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '2x' )
        self.assertEqual( oTest.iBrand.cTitle, 'Acoustic Research' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        iThisOne = 153684782088
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 3, iThisOne,
                'should find Heath AS-21' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertIn( oTest.iModel.cTitle, ( 'AS-21', '414E', '804A (horn)' ) )
        self.assertIn( oTest.iBrand.cTitle, ( 'Heathkit', 'Altec-Lansing' ) )
        self.assertIn( oTest.iCategory.cTitle,
                      ( 'Speaker System', 'Horn', 'Driver' ) )
        #
        #
        #
        iThisOne = 392536575491
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find JBL 175 not LE-175' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '1217-1290' )
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        self.assertEqual( oTest.iCategory.cTitle, 'Horn' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '175' )
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        iThisOne = 183953915448
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should be local pickup only' )
        #
        # tested in searching/tests/test_models.py
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'Regency' )
        self.assertEqual( oTest.iBrand.cTitle, 'Electro-Voice' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker Enclosure' )
        #
        #
        #
        iThisOne = 153723814561
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should NOT be local pickup only -- '
                'ships to USA w local p/u option' )
        #
        # tested in searching/tests/test_models.py
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'R-200' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Tuner' )
        #
        #
        #
        #
        iThisOne = 123987878353
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Altec 415C not Lansing 415' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '415C' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        iThisOne = 233407527461
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 8, iThisOne,
                'should find 6V6 and 6V6GT for GE, RCA, Tung-Sol & Ken-Rad' )
        #
        gotComponents = set( [] )
        gotBrands       = set( [] )
        #
        setComponents = frozenset(
                ( '6V6 (metal can)', '6V6GTA' ) )
        setBrands       = frozenset( ( 'RCA', 'GE', 'Tung-Sol', 'Ken-Rad' ) )
        #
        for i in range( len( dItemsToTest[ iThisOne ] ) ):
            #
            oTest = dItemsToTest[ iThisOne ][ i ]
            #
            self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
            #
            self.assertIn( oTest.iModel.cTitle, setComponents )
            self.assertIn( oTest.iBrand.cTitle, setBrands     )
            #
            gotComponents.add( oTest.iModel.cTitle    )
            gotBrands.add(     oTest.iBrand.cTitle )
            #
        #
        self.assertEqual( gotComponents, setComponents )
        self.assertEqual( gotBrands,     setBrands     )
        #
        #
        #
        #
        #
        iThisOne = 323984684424
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should be local pickup only' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '2' )
        self.assertEqual( oTest.iBrand.cTitle, 'Marantz' )
        self.assertEqual( oTest.iCategory.cTitle, 'Amplifier' )
        #
        #
        #
        iThisOne = 133251370953
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should match up PQ brand and model' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '7308 (Amperex PQ)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Amperex (PQ)' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 163972543321
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Acro TO-300' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertIn( oTest.iModel.cTitle, ( 'TO-300', 'W-3M' ) )
        self.assertIn( oTest.iBrand.cTitle, ('ACRO', 'Heathkit' ) )
        self.assertIn( oTest.iCategory.cTitle,
                      ( 'Output Transformer', 'Amplifier' ) )
        #
        #
        #
        #
        iThisOne = 183952461011
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should NOT be local pickup only -- '
                'ships to USA w local p/u option' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6SN7GTB' )
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        iThisOne = 153747946010
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Altec driver not horn' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '808-8A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        #
        iThisOne = 184089371148
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find 12AT7 (BB) & Amperex BB' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AT7 (Bugle Boy)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Amperex (Bugle Boy)' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        iThisOne = 184092262958
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should be local pick up option' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '8417' )
        self.assertEqual( oTest.iBrand.cTitle, 'GE' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        #
        iThisOne = 324020037678
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find 604-8G! production missed this recently!' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertIn(    oTest.iModel.cTitle, ( '620', '604-8G' ) )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertIn(    oTest.iCategory.cTitle,
                            ( 'Speaker Enclosure', 'Driver' ) )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIn(    oTest.iModel.cTitle, ( '620', '604-8G' ) )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertIn(    oTest.iCategory.cTitle,
                            ( 'Speaker Enclosure', 'Driver' ) )
        #
        #
        #
        #
        #
        iThisOne = 153777954483
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Stark tester not Hickok 6000' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '8-77' )
        self.assertEqual( oTest.iBrand.cTitle, 'Stark' )
        self.assertEqual( oTest.iCategory.cTitle, 'Tube Tester' )
        #
        #
        #
        #
        #
        #
        iThisOne = 174143946146
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should only find 6922 not 6DJ8 E88CC' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        #self.assertEqual( oTest.iModel.cTitle, '6922 (Amperex Gold)' )
        #self.assertEqual( oTest.iBrand.cTitle, 'Amperex (gold pins)' )
        #self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 193278712422
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find roll chart' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '600A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Hickok' )
        self.assertEqual( oTest.iCategory.cTitle, 'roll chart (tube tester)' )
        #
        #
        #
        #
        iThisOne = 114039185762
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find n-800E dividing network' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'N-800E' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        #
        #
        #
        iThisOne = 174142861539
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find EF86 (BB) Amperex BB and not the lower combos' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'EF86 (Amperex BB)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Amperex (Bugle Boy)' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        iThisOne = 174147736580
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find E88CC ONLY!' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'E88CC' )
        self.assertEqual( oTest.iBrand.cTitle, 'Valvo' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 174148034585
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find 6201 and not 12AX7' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6201' )
        self.assertEqual( oTest.iBrand.cTitle, 'GE' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 202867134038
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Mullard 10M 12AX7/ECC83 and not Mullard 12AX7/ECC83' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7' )
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard 10M' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 283743905366
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find ECC88 & 6DJ8 and disregard in parens (7DJ8 & PCC88)' )
        #
        for i in ( 0, 1 ):
            #
            oTest = dItemsToTest[ iThisOne ][ i ]
            #
            self.assertIn(    oTest.iModel.cTitle, ( 'ECC88', '6DJ8' ) )
            self.assertNotIn( oTest.iModel.cTitle, ( 'PCC88', '7DJ8' ) )
            self.assertEqual( oTest.iBrand.cTitle, 'Telefunken' )
            self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
            #
        #
        #
        #
        #
        #
        iThisOne = 352919421447
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find 6SN7GTB not 6SN7GT (Sylvania)' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6SN7GTB' )
        self.assertEqual( oTest.iBrand.cTitle, 'Sylvania' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 164044313206
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Dynaco ST 70 CAGE (I wish!)' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'Stereo 70' )
        self.assertEqual( oTest.iBrand.cTitle, 'Dynaco' )
        self.assertEqual( oTest.iCategory.cTitle, 'Amplifier' )
        #
        #
        #
        #
        iThisOne = 312953984914
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find 6189 not 12AU7WA' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6189' )
        self.assertIn(    oTest.iBrand.cTitle, ( 'Valvo', 'Siemens' ) )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        iThisOne = 312954104297
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find nothing, but 6V6G is in parens' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual(  oTest.iModel.cTitle, '6V6G' )
        self.assertIsNone( oTest.iBrand )
        self.assertEqual(  oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        iThisOne = 283752371216
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Siemens EL34' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'EL34' )
        self.assertEqual( oTest.iBrand.cTitle, 'Siemens' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        iThisOne = 164044315855
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Fisher 80-R Tuner' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '80-R' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Tuner' )
        #
        #
        #
        #
        iThisOne = 184032120009
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find Altec A7-500-II (Magnificent) not Lansing A-7' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertIn( oTest.iModel.cTitle, ( 'A7-500-II', 'A-7' ) )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIn( oTest.iModel.cTitle, ( 'A7-500-II', 'A-7' ) )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        #
        iThisOne = 202868417147
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Amperex BB 12AX7/ECC83 and not Amperex 12AX7/ECC83' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7' )
        self.assertEqual( oTest.iBrand.cTitle, 'Amperex (Bugle Boy)' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        iThisOne = 174145135158
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find GE 5 Star 5814A and not GE 12AU7' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '5814A' )
        self.assertEqual( oTest.iBrand.cTitle, 'GE (5 Star)' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 324090682443
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Genalex Gold Lion not the others' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'KT-66' )
        self.assertEqual( oTest.iBrand.cTitle, 'Genalex (Gold Lion)' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        iThisOne = 153839648277
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find A-50 not A-25' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-50' )
        self.assertEqual( oTest.iBrand.cTitle, 'Dynaco' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        #
        #
        iThisOne = 383441473993
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find 10C not the rest' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '10C3' )
        self.assertEqual( oTest.iBrand.cTitle, 'Brook' )
        self.assertEqual( oTest.iCategory.cTitle, 'Amplifier' )
        #
        #
        #
        #
        #
        iThisOne = 274222992683
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'AZ1 Valvo Pair! raised error in production?' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'AZ1' )
        self.assertEqual( oTest.iBrand.cTitle, 'Valvo' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        iThisOne = 174177597476
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'Meter was a glitch in production' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'meter' )
        self.assertIsNone( oTest.iBrand )
        self.assertIsNone( oTest.iCategory )
        #
        #
        #
        #
        iThisOne = 193390315883
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'x-100 should find X-100-B manual not amp?' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'X-100-B' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Manual' )
        #
        #
        #
        #
        #
        iThisOne = 313033073507
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                '755E now a separate model from other 755 variants' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '755E' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        #
        #
        iThisOne = 114154224682
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find EA-3 not the rest' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'EA-3' )
        self.assertEqual( oTest.iBrand.cTitle, 'Heathkit' )
        self.assertEqual( oTest.iCategory.cTitle, 'Integrated Amp' )
        #
        #
        #
        #
        #
        iThisOne = 153883438316
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'got category warning for this' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'IT-28' )
        self.assertEqual( oTest.iBrand.cTitle, 'Heathkit' )
        self.assertEqual( oTest.iCategory.cTitle, 'Manual' )
        #
        #
        #
        #
        iThisOne = 283830240734
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find 848A (Flamenco)' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '848A (Flamenco)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        #
        #
        iThisOne = 254574295997
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 3, iThisOne,
                's/n find Mullard just IEC Mullard' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'E88CC' )
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard IEC' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6922' )
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard IEC' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6DJ8' )
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard IEC' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        iThisOne = 133392165411
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find engraved base 300b' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '300B (etched base)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Western Electric' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        iThisOne = 193427753317
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should X-100-B manual' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'X-100-B' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Manual' )
        #
        #
        #
        #
        iThisOne = 362980614720
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'test "not" new DROP_AFTER_THIS' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'VT-25 (10Y)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Western Electric' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        iThisOne = 352961821505
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'got warning "model has category id 172 [Component]'
                'in dCategoryFamily" for item' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '287F' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Theater Amp' )
        #
        #
        #
        #
        #
        iThisOne = 233573519366
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should not 6550 not 6550-VI' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6550' )
        self.assertEqual( oTest.iBrand.cTitle, 'Westinghouse' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        iThisOne = 283709382058
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 9, iThisOne,
                'should find 875A Granada not Barcelona or Valencia' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        #self.assertEqual( oTest.iModel.cTitle, '875A (Granada)' )
        #self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        #
        iThisOne = 303545301410
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'listed under vintage manuals, so should find manual not amp' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'C-22' )
        self.assertEqual( oTest.iBrand.cTitle, 'McIntosh' )
        self.assertEqual( oTest.iCategory.cTitle, 'Manual' )
        #
        #
        #
        #
        #
        iThisOne = 313048572053
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find tubes not horn' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '5842' )
        self.assertEqual( oTest.iBrand.cTitle, 'Western Electric' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '417A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Western Electric' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        iThisOne = 293562589789
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should not find D130 but should find JBL' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertIsNone( oTest.iModel )
        self.assertEqual(  oTest.iBrand.cTitle, 'JBL' )
        self.assertEqual(  oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        #
        #
        iThisOne = 184168518275
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should not find Imperial' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-402' )
        self.assertEqual(  oTest.iBrand.cTitle, 'Jensen' )
        self.assertEqual(  oTest.iCategory.cTitle, 'Crossover' )
        #
        #
        #
        #
        #
        iThisOne = 153920100946
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find A-402 Crossover not rest' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-402' )
        self.assertEqual(  oTest.iBrand.cTitle, 'Jensen' )
        self.assertEqual(  oTest.iCategory.cTitle, 'Crossover' )
        #
        #
        #
        #
        #
        iThisOne = 353067866152
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 9, iThisOne,
                'should find Imperial speaker maybe not rest ?' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        #self.assertEqual( oTest.iModel.cTitle, 'Imperial' )
        self.assertEqual(  oTest.iBrand.cTitle, 'Jensen' )
        #self.assertEqual(  oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        #
        #
        iThisOne = 184281669249
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 3, iThisOne,
                'ideally would find X36 Crossover only '
                'but wording includes the rest' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'X36' )
        self.assertEqual( oTest.iBrand.cTitle, 'Electro-Voice' )
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIn   ( oTest.iModel.cTitle, ( 'T-35B', 'T-350B') )
        self.assertEqual( oTest.iBrand.cTitle, 'Electro-Voice' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertIn   ( oTest.iModel.cTitle, ( 'T-35B', 'T-350B') )
        self.assertEqual( oTest.iBrand.cTitle, 'Electro-Voice' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        #
        #
        iThisOne = 133401627353
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find metal base EL34' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6CA7' )
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'EL34 (MB Mullard)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        #
        iThisOne = 174226403478
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find 6922 not the rest' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6922' )
        self.assertEqual( oTest.iBrand.cTitle, 'RCA' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        iThisOne = 254524704215
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 4, iThisOne,
                'should find EL84 not 6BQ5' )
        #
        tGotBrands = ( 'Siemens', 'Lorenz', 'Valvo', 'Telefunken' )
        #
        for i in range( 4 ):
            #
            oTest = dItemsToTest[ iThisOne ][ i ]
            #
            self.assertEqual(    oTest.iModel.cTitle, ( 'EL84' ) )
            self.assertNotEqual( oTest.iModel.cTitle, ( '6BQ5' ) )
            self.assertIn(       oTest.iBrand.cTitle, tGotBrands )
            self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
            #
        #
        #
        #
        #
        iThisOne = 184284149755
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 3, iThisOne,
                'should find 8HD horn not the rest '
                'but living with A on end throws off logic' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '8HD' )
        self.assertEqual( oTest.iBrand.cTitle, 'Electro-Voice' )
        self.assertEqual( oTest.iCategory.cTitle, 'Horn' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIn( oTest.iModel.cTitle, ( 'T-250', 'T-25-A' ) )
        self.assertEqual( oTest.iBrand.cTitle, 'Electro-Voice' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertIn( oTest.iModel.cTitle, ( 'T-250', 'T-25-A' ) )
        self.assertEqual( oTest.iBrand.cTitle, 'Electro-Voice' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        #
        #
        iThisOne = 174253058987
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find 7DJ8 & PCC88 not 6DJ8 or ECC88' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '7DJ8' )
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'PCC88' )
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        #
        #
        iThisOne = 174236717488
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find E88CC not the rest' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'E88CC' )
        self.assertIn(    oTest.iBrand.cTitle, ( 'Mullard', 'Telefunken' ) )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'E88CC' )
        self.assertIn(    oTest.iBrand.cTitle, ( 'Mullard', 'Telefunken' ) )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        iThisOne = 174183853047
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 3, iThisOne,
                'should find 604 Driver & 605 Cabinet' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '605A (driver)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '605A (enclosure)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker Enclosure' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '604' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        #
        #
        #
        iThisOne = 174291344087
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find 7308 not CV4108 or E188CC' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '7308' )
        self.assertEqual( oTest.iBrand.cTitle, 'Raytheon' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        #
        iThisOne = 174290984997
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should only find Raytheon 12AX7A & RCA 12AX7A' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7A' )
        self.assertIn(    oTest.iBrand.cTitle, ( 'Raytheon', 'RCA' ) )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7A' )
        self.assertIn(    oTest.iBrand.cTitle, ( 'Raytheon', 'RCA' ) )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        #
        #
        iThisOne = 193480815469
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find Fada 711, note Catalin is generic' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '711' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fada' )
        self.assertEqual( oTest.iCategory.cTitle, 'Radio' )
        #
        #
        #
        #
        #
        #
        iThisOne = 233597629477
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find 2A3 (RCA single plate) not RCA 2A3' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '2A3' )
        self.assertEqual( oTest.iBrand.cTitle, 'Cunningham' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '2A3 (RCA SP)' )
        self.assertEqual( oTest.iBrand.cTitle, 'RCA' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        iThisOne = 264741220720
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 2, iThisOne,
                'should find GE 12AX7-WA and 12AX7 (GE)' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7-WA' )
        self.assertEqual( oTest.iBrand.cTitle, 'GE' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7 (GE)' )
        self.assertEqual( oTest.iBrand.cTitle, 'GE' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        #
        #
        iThisOne = 392820998298
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 1, iThisOne,
                'should find 5814A only' )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '5814A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        #
        #
        iThisOne = 164011103887
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 9, iThisOne,
                'should find diaphrams not driver' )
        #
        #
        #
        #
        #
        #
        iThisOne = 324030050981
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 9, iThisOne,
                'should find power supply ? big challenge?' )
        #
        #
        #
        #
        #
        #
        #
        iThisOne = 174302152790
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 9, iThisOne,
                'should find PAS & FM3' )
        #
        #
        #
        #
        #
        #
        #
        iThisOne = 143625858664
        #
        #
        self.print_len(
                dItemsToTest[ iThisOne ], 9, iThisOne,
                'got warning in production' )
        #
        #
        #
        #
        #
        '''
        '''
        #
        #
        #
        qsUserFinders = UserFinder.objects.all()
        #
        self.assertGreater( len( qsUserFinders ), 78 )
        #
        iThisOne = 392536575491
        #
        oUserFinder = UserFinder.objects.get(
                iItemNumb = iThisOne, iUser = self.user1 )
        #
        self.assertGreater(  oUserFinder.iHitStars,   2 )
        self.assertNotEmpty( oUserFinder.cTitle         )
        self.assertNotEmpty( oUserFinder.cMarket        )
        self.assertNotEmpty( oUserFinder.cListingType   )
        self.assertNotEmpty( oUserFinder.tTimeEnd       )
        self.assertNotEmpty( oUserFinder.iMaxModel      )
        #
        oMaxModel = Model.objects.filter( pk = oUserFinder.iMaxModel )
        #
        self.assertNotEmpty( oMaxModel                  )
        #
        if False:
            #
            maybePrint()
            maybePrint( iThisOne )
            #
            for oTest in dItemsToTest[ iThisOne ]:
                #
                maybePrint()
                if oTest.iBrand:    maybePrint( oTest.iBrand.cTitle )
                if oTest.iModel:    maybePrint( oTest.iModel.cTitle )
                if oTest.iCategory: maybePrint( oTest.iCategory.cTitle )
                #
            maybePrint()
        #
        print()
        print( "run daily:" )
        print( "1) pmt searching.tests.test_utils.DoSearchStoreResultsTests" )
        print( "2) pmt ebayinfo.tests.test_utils.MarketsAndCategoriesTests" )
        print()
        #
        #
        #if oTest.iBrand:    print( oTest.iBrand.cTitle )
        #if oTest.iModel:
            #print( oTest.iModel.cTitle, oTest.iModel.iCategory_id )
        #if oTest.iCategory: print( oTest.iCategory.cTitle )
        #
        #oModel = Model.objects.get( cTitle = '15" Sliver' )
        #print( '15" Sliver:', oModel.cRegExLook4Title )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_sub_models_OK_finder( self ):
        #
        oModel = Model.objects.get( cTitle = '6L6WGB', iUser = self.user1 )
        #
        self.assertIsNotNone( oModel )
        #
        dFinders = {}
        #
        foundItem = getFoundItemTester(
                        oModel,
                        dFinders,
                        bSubModelsOK = True,
                        bAddDash     = True )
        #
        sAuctionTitle = 'Tung-Sol 5881 6L6WG amplifier tube'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertEqual( sInTitle, '6L6WG' )
        #
        sExpect = r'6[-/ ]*L[-/ ]*6[-/ ]*WG[A-Z]{0,1}\b'
        #
        self.assertEqual( oModel.cRegExLook4Title, sExpect )
        #
        self.assertEqual( sWhatRemains, 'Tung-Sol 5881 amplifier tube' )
        #
        #print('')
        #print( 'sInTitle:', sInTitle )
        #print( 'oModel.cRegExLook4Title:', oModel.cRegExLook4Title )
        #print('')



class findersStorageTest( AssertEmptyMixin, SetUpBrandsCategoriesModelsWebTest ):

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
        t = _getBrandRegExFinders4Test( self.oBrand_hp )
        #
        findTitle, findExclude = t
        #
        sAuctionTitle = 'Vintage Hewlett Packard 200C Audio Oscillator'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Vintage Hewlett-Packard 200C Audio Oscillator'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Vintage HewlettPackard 200C Audio Oscillator'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        t = _getBrandRegExFinders4Test( self.oBrand_GT )
        #
        findTitle, findExclude = t
        #
        sAuctionTitle = 'Groove Tubes Microphone GT55 Professional Condenser Mic'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Groove-Tube Microphone GT55 Professional Condenser Mic'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        sAuctionTitle = 'GrooveTubes Microphone GT55 Professional Condenser Mic'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_CategoryRegExFinderStorage(self):
        #
        t = _getCategoryRegExFinders4Test( self.WidgetCategory )
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
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( uExcludeThis )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertEqual( sInTitle, 'Caddy' )
        self.assertTrue( uExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( uExcludeThis )
        #
        foundItem = dFinders[ self.oBrand.pk ]
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( uExcludeThis )
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
        foundItem = getFoundItemTester( self.WidgetCategory, dFinders )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( uExcludeThis )
        #
        sAuctionTitle = 'Gemini Jets 1/200 Delta MD-80 Widget Livery N956DL'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertEqual( sInTitle, 'Widget' )
        self.assertTrue(  uExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertFalse( sInTitle )
        self.assertFalse( uExcludeThis )
        #
        foundItem = dFinders[ self.WidgetCategory.pk ]
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( uExcludeThis )
        #
        self.assertIn(     self.WidgetCategory.cRegExLook4Title,
                                ( r'\bGizmo\b|Widget', r'Widget|\bGizmo\b' ) )
        #
        self.assertEqual( self.WidgetCategory.cRegExExclude,  r'\bDelta\b'  )
        self.assertEqual( self.WidgetCategory.cRegExKeyWords,    'Gadget' )
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
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( uExcludeThis )
        #
        self.assertEqual( sWhatRemains, '1976 Cadillac Eldorado Bicentennial' )
        #
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertFalse( sInTitle     )
        self.assertTrue(  uExcludeThis )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertEqual( sInTitle, 'Fleetwood' )
        self.assertFalse( uExcludeThis )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertFalse( sInTitle     )
        self.assertFalse( uExcludeThis )
        #
        foundItem = dFinders[ self.oModel.pk ]
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertTrue(  sInTitle     )
        self.assertFalse( uExcludeThis )
        #
        self.assertIn(     self.oModel.cRegExLook4Title,
                                ( 'Woodie|Fleetwood', 'Fleetwood|Woodie' ) )
        #
        # order can vary
        #
        setRegExExclude = frozenset( self.oModel.cRegExExclude.split( '|' ) )
        #
        self.assertIn( 'tournament', setRegExExclude )
        self.assertIn( r'\bgolf\b',  setRegExExclude )
        #
        self.assertEqual( self.oModel.cRegExKeyWords, 'Eldorado' )
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_generic_model_finder_OK( self ):
        #
        oModel = Model.objects.get( cTitle = '601b', iUser = self.user1 )
        #
        self.assertIsNotNone( oModel )
        #
        dFinders = {}
        #
        foundItem = getFoundItemTester(
                        oModel,
                        dFinders,
                        bAddDash = True )
        #
        sAuctionTitle = 'Altec 603 cabinet superb'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertEmpty( sInTitle )
        #
        tFinders = ( r'\b601(?:[-/ ]*[A-Z]){0,1}\b', )
        #
        self.assertIn( oModel.cRegExLook4Title, tFinders )
        #

    def test_model_endswith_digit( self ):
        #
        oModel = Model.objects.get( cTitle = 'Model 2', iUser = self.user1 )
        #
        self.assertIsNotNone( oModel )
        #
        dFinders = {}
        #
        foundItem = getFoundItemTester(
                        oModel,
                        dFinders,
                        bAddDash = True )
        #
        sAuctionTitle = 'Model 240 amplifier'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertEmpty( sInTitle )
        #
        tFinders = ( r'Model[-/ ]*2\b|Model[-/ ]*Two\b',
                     r'Model[-/ ]*Two\b|Model[-/ ]*2\b' )
        #
        self.assertIn( oModel.cRegExLook4Title, tFinders )
        #
        #
        sAuctionTitle = 'Model 2 amplifier'
        #
        t = foundItem( sAuctionTitle )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        self.assertEqual( 'Model 2', sInTitle )
        #



class GetRelevantTitleTests( AssertEmptyMixin, TestCasePlus ):
    #
    def test_get_relevant_title( self ):
        #
        sWantTitle = "ALTEC LANSING 311-90 Horn"
        sFullTitle = "ALTEC LANSING 311-90 Horn for 288 290 291 292 299 drivers"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(), sWantTitle )
        self.assertEmpty( sGotInParens )
        #
        sFullTitle = "ALTEC LANSING 311-90 Horn fits Voice of Theather Speaker System"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(), sWantTitle )
        self.assertEmpty( sGotInParens )
        #
        sFullTitle = "ALTEC LANSING 311-90 Horn from Voice of Theather Speaker System"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(), sWantTitle )
        self.assertEmpty( sGotInParens )
        #
        sFullTitle = "ALTEC LANSING 311-90 Horn used with Voice of Theather Speaker System"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(), sWantTitle )
        self.assertEmpty( sGotInParens )
        #
        #
        sWantTitle = "Supreme TV-7 TUBE TESTER military vintage"
        sFullTitle = "Supreme TV-7 TUBE TESTER military vintage test western electric 300b"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(), sWantTitle )
        self.assertEmpty( sGotInParens )
        #
        #
        sWantTitle = "PIONEER / LAFAYETTE HW-7 SUPER HORN TWEETER -"
        sFullTitle = "PIONEER / LAFAYETTE HW-7 SUPER HORN TWEETER - similar to Jensen RP302"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(), sWantTitle )
        self.assertEmpty( sGotInParens )
        #
        #
        sWantTitle = "Pilot 240 tube integrated amp stereo WORKING"
        sFullTitle = "Pilot 240 tube integrated amp stereo WORKING ala Fisher Scott"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(), sWantTitle )
        self.assertEmpty( sGotInParens )
        #
        #
        sWantTitle = "ALTEC 755A Loudspeaker Unit"
        sFullTitle = "ALTEC 755A Loudspeaker Unit same as Western Electric 755A"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(), sWantTitle )
        self.assertEmpty( sGotInParens )
        #
        #
        sWantTitle = "VT25  Western Electric Tube Valve matched pair NOS NIB"
        sFullTitle = "VT25  Western Electric Tube Valve matched pair NOS NIB not 300B 2a3 45 211"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(), sWantTitle )
        self.assertEmpty( sGotInParens )
        #
        #
        sWantTitle = "4 lot 6201 GE dual triode preamp tube,pin"
        sFullTitle = "4 lot 6201 GE dual triode preamp tube,pin compatible with 12AX7 used,tested,good"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(), sWantTitle )
        self.assertEmpty( sGotInParens )
        #
        #
        sFullTitle = "4x EL34 power tubes  RFT ( SIEMENS ) - NOS  - EL 34"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(),  sFullTitle )
        self.assertEqual( sGotInParens.strip(), '( SIEMENS )' )
        #
        #
        sFullTitle = "JBL Metregon 205 - Time Capsule! (130A, 275, N500, H5040)"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(),  sFullTitle )
        self.assertEqual( sGotInParens.strip(), '(130A, 275, N500, H5040)' )
        #
        #
        sFullTitle = "JBL M31 (looks Like D130) Needs are-Coned"
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle, 'JBL M31  ()  Needs are-Coned' )
        self.assertEqual( sGotInParens, '(looks Like D130)' )
        #
        #
        sFullTitle = ( "4x KT61 ( 6AG6 G ) tubes HALTRON ( M.O.V. ) -"
                       "NOS (~  6V6G / EL33 /  EL3 ) KT 61" )
        #
        sRetnTitle, sGotInParens = _getRelevantTitle( sFullTitle )
        #
        self.assertEqual( sRetnTitle.strip(),  sFullTitle )
        self.assertEqual( sGotInParens.strip(),
                         '( 6AG6 G )( M.O.V. )(~  6V6G / EL33 /  EL3 )' )
        #

