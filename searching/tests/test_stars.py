#import inspect

from os.path            import join

from django.core.urlresolvers import reverse

from django.test        import TestCase
from django.utils       import timezone

from core.utils_test    import setUpBrandsCategoriesModels, AssertEmptyMixin

from ..models           import ( ItemFound, UserItemFound, ItemFoundTemp )

from .test_models       import PutSearchResultsInDatabase

from .test_utils        import GetBrandsCategoriesModelsSetUp

from ..utils_stars      import ( getFoundItemTester, _getRegExSearchOrNone,
                                 findSearchHits, _getRowRegExpressions,
                                 getInParens )

from searching.tests    import iRecordStepsForThis

from brands.views       import BrandUpdateView
from models.models      import Model



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


# iRecordStepsForThis imported from __init__.py

class SetUpForHitStarsTests( PutSearchResultsInDatabase ):
    #
    ''' class for testing findSearchHits() hit star calculations '''
    #
    def setUp( self ):
        #
        super( SetUpForHitStarsTests, self ).setUp()
        #
        # bCleanUpAfterYourself must be False or tests will fail!
        # iRecordStepsForThis imported from __init__.py
        #
        findSearchHits( self.user1.id,
                        bCleanUpAfterYourself   = False,
                        iRecordStepsForThis     = iRecordStepsForThis )
        #
        #print( '\n' )
        #print( 'setting up KeyWordFindSearchHitsTests' )



class KeyWordFindSearchHitsTests( SetUpForHitStarsTests ):

    def print_len( self, lTest, iExpect, iItemNumb = None ):
        #
        if not lTest:
            #
            print('')
            #
            if iItemNumb:
                print( 'found nothing for %s' % iItemNumb )
            else:
                print( 'found nothing, iItemNumb not passed' )
            #
        elif len( lTest ) != iExpect:
            #
            print('')
            print(lTest[0])
            print( '%s length:' % lTest[0].iItemNumb_id,
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
                        print( ' | '.join( lPrintThis ) )
                        #
                    #
                #
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
        self.print_len( dItemsToTest[ 162988285720 ], 2 )
        #
        oTest = dItemsToTest[ 162988285720 ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        #
        self.assertEqual( oTest.iModel.cTitle, '6L6WGB' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
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
        self.print_len( dItemsToTest[ iThisOne ], 2 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Philips' )
        #
        self.assertEqual( oTest.iModel.cTitle, '6AU6A' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard' )
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
        # getting None self.assertEqual( oItemFound.cSubTitle,
        #           'Working Pair 12" Coaxial Speakers & Balance Controls' )
        #
        print('')
        print('173375697400')
        print( 'cSubTitle is None:', oItemFound.cSubTitle is None )
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
        #
        self.print_len( dItemsToTest[ 292640430401 ], 3 )
        #
        oTest = dItemsToTest[ 292640430401 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'M1131' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Choke' )
        #
        oTest = dItemsToTest[ 292640430401 ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        self.assertIn( oTest.iModel.cTitle, 'A-61' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ 292640430401 ][ 2 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-402' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
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
        self.print_len( dItemsToTest[ 163167777899 ], 3 )
        #
        oTest = dItemsToTest[ 163167777899 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'N-3000A' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ 163167777899 ][ 1 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, '601b' )
        ##
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker Enclosure' )
        #
        oTest = dItemsToTest[ 163167777899 ][ 2 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, '601a' )
        ##
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        #
        #
        self.print_len( dItemsToTest[ 292659341471 ], 3 )
        #
        oTest = dItemsToTest[ 292659341471 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'M1131' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Choke' )
        #
        oTest = dItemsToTest[ 292659341471 ][ 1 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-61' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ 292659341471 ][ 2 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-402' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
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
        self.assertEqual( oTest.iModel.cTitle, 'GRF' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        oTest = dItemsToTest[ 153121548106 ][ 0 ]
        #
        self.assertIsNotNone( oTest )
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Tannoy' )
        #
        self.assertEqual( oTest.iModel.cTitle, '15" Silver' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        iThisOne = 153124672147
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
        self.assertEqual( oTest.iModel.cTitle, '601b' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker Enclosure' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, '601a' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
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
        iThisOne = 292672067477
        #
        self.print_len( dItemsToTest[ iThisOne ], 3 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'M1131' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Choke' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-61' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-402' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
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
        self.print_len( dItemsToTest[ iThisOne ], 1 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertIsNone( oTest.iBrand )
        self.assertIsNone( oTest.iCategory )
        #
        #
        iThisOne = 163199461416
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
        self.assertEqual( oTest.iModel.cTitle, '601b' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker Enclosure' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertEqual( oTest.iModel.cTitle, '601a' )
        #
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        iThisOne = 202401940540
        #
        self.print_len( dItemsToTest[ iThisOne ], 3 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'JBL' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'N2600' )
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'D-130' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '75' )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
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
        iThisOne = 292679662673
        #
        self.print_len( dItemsToTest[ iThisOne ], 3 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Jensen' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'M1131' )
        self.assertEqual( oTest.iCategory.cTitle, 'Choke' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-61' )
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-402' )
        self.assertEqual( oTest.iCategory.cTitle, 'Crossover' )
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
        self.print_len( dItemsToTest[ iThisOne ], 5 ) # order not consistent
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Klipsch' )
        #
        self.assertEqual( oTest.iModel.cTitle, 'K-700' )
        self.assertEqual( oTest.iCategory.cTitle, 'Horn' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        setComponents = frozenset( ( 'K-77', 'K-55-V', 'K-22' ) )
        #
        self.assertIn( oTest.iModel.cTitle, setComponents )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertIn( oTest.iModel.cTitle, setComponents )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 3 ]
        #
        self.assertIn( oTest.iModel.cTitle, setComponents )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 4 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'Heresy (H700)' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
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
        self.print_len( dItemsToTest[ iThisOne ], 5 )
        #
        gotComponents = set( [] )
        gotCategories = set( [] )
        #
        setComponents = frozenset(
                ( 'C45 (Metregon)', 'H5040', 'D-130A', '275', 'N500' ) )
        setCategories = frozenset(
                ( 'Speaker Enclosure', 'Horn', 'Driver', 'Crossover' ) )
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
        #
        self.assertEqual( gotComponents, setComponents )
        self.assertEqual( gotCategories, setCategories )
        #
        #
        #
        #
        #
        iThisOne = 192659380750
        #
        self.print_len( dItemsToTest[ iThisOne ], 3 )
        #
        setComponents = frozenset( ( '288', '515A' ) )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        #
        self.assertIn( oTest.iModel.cTitle, setComponents )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertIn( oTest.iModel.cTitle, setComponents )
        self.assertEqual( oTest.iCategory.cTitle, 'Driver' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'A-5' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
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
        iThisOne = 192660195679
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
        self.print_len( dItemsToTest[ iThisOne ], 1 )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'VT-107 (6V6)' )
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
        iThisOne = 202462110744
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'XP-6A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        iThisOne = 352494035670
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        # self.assertEqual( oTest.iModel.cTitle, '12AX7-WA (Philips)' )
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
        iThisOne = 323557043166
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
        iThisOne = 192737436300
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, 'XP-6A' )
        self.assertEqual( oTest.iBrand.cTitle, 'Fisher' )
        self.assertEqual( oTest.iCategory.cTitle, 'Speaker System' )
        #
        #
        iThisOne = 312339506602
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        # should get 1005 horn
        #
        self.assertEqual( oTest.iModel.cTitle, '1005B' )
        self.assertEqual( oTest.iBrand.cTitle, 'Altec-Lansing' )
        self.assertEqual( oTest.iCategory.cTitle, 'Horn' )
        #
        iThisOne = 283272931267
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        # also listed 6267?, fixed in data
        self.assertEqual( oTest.iModel.cTitle, 'EF86' )
        self.assertEqual( oTest.iBrand.cTitle, 'Mullard' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        iThisOne = 113392158472
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
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
        self.assertEqual( oTest.iModel.cTitle, '6SN7GT (Sylvania)' )
        self.assertEqual( oTest.iBrand.cTitle, 'Sylvania' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        iThisOne = 352535627937
        #
        self.print_len( dItemsToTest[ iThisOne ], 2, iThisOne )
        #
        # should show both brands, Sylvania & Marconi
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6V6G' )
        self.assertEqual( oTest.iBrand.cTitle, 'Sylvania' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
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
        self.assertEqual( oTest.iBrand.cTitle, 'RCA' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7' )
        self.assertEqual( oTest.iBrand.cTitle, 'Tung-Sol' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '12AX7' )
        self.assertEqual( oTest.iBrand.cTitle, 'Raytheon' )
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
        self.assertEqual( oTest.iModel.cTitle, '12AU7A' )
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
        self.print_len( dItemsToTest[ iThisOne ], 4, iThisOne )
        #
        # d/n get into keepers
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6922' )
        self.assertEqual( oTest.iBrand.cTitle, 'GE' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 1 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6DJ8' )
        self.assertEqual( oTest.iBrand.cTitle, 'GE' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 2 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6922' )
        self.assertEqual( oTest.iBrand.cTitle, 'Philips' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        oTest = dItemsToTest[ iThisOne ][ 3 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '6DJ8' )
        self.assertEqual( oTest.iBrand.cTitle, 'Philips' )
        self.assertEqual( oTest.iCategory.cTitle, 'Vacuum Tube' )
        #
        #
        #
        iThisOne = 312417181299
        #
        self.print_len( dItemsToTest[ iThisOne ], 1, iThisOne )
        #
        # says Marantz 240 s/n find Marantz 2
        #
        oTest = dItemsToTest[ iThisOne ][ 0 ]
        #
        self.assertEqual( oTest.iModel.cTitle, '240' )
        self.assertIsNone( oTest.iBrand )
        self.assertIsNone( oTest.iCategory )
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
        # s/n find Marantz Model 1 !!!
        #
        #



        #
        if False:
            #
            print()
            print( iThisOne )
            #
            for oTest in dItemsToTest[ iThisOne ]:
                #
                print()
                if oTest.iBrand:    print( oTest.iBrand.cTitle )
                if oTest.iModel:    print( oTest.iModel.cTitle )
                if oTest.iCategory: print( oTest.iCategory.cTitle )
                #
            print('')
        #
        #if oTest.iBrand:    print( oTest.iBrand.cTitle )
        #if oTest.iModel:
            #print( oTest.iModel.cTitle, oTest.iModel.iCategory_id )
        #if oTest.iCategory: print( oTest.iCategory.cTitle )
        #
        #oModel = Model.objects.get( cTitle = '15" Sliver' )
        #print( '15" Sliver:', oModel.cRegExLook4Title )
        #
        # pmt searching.tests.tests.test_stars.KeyWordFindSearchHitsTests.test_find_search_hits_test
        #
        #print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_sub_models_OK_finder( self ):
        #
        oModel = Model.objects.get( cTitle = '6L6WGB' )
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
        sAuctionTitle = '"Tung-Sol 5881 6L6WG amplifier tube'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertEqual( sInTitle, '6L6WG' )
        #
        sExpect = r'6[-/ ]*L[-/ ]*6[-/ ]*WG[A-Z]{0,1}\b'
        #
        self.assertEqual( oModel.cRegExLook4Title, sExpect )
        #
        #print('')
        #print( 'sInTitle:', sInTitle )
        #print( 'oModel.cRegExLook4Title:', oModel.cRegExLook4Title )
        #print('')



class findersStorageTest( AssertEmptyMixin, setUpBrandsCategoriesModels ):

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
        oModel = Model.objects.get( cTitle = '601b' )
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
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertEmpty( sInTitle )
        #
        tFinders = ( r'\b601(?:[-/ ]*[A-Z]){0,1}\b', )
        #
        self.assertIn( oModel.cRegExLook4Title, tFinders )
        #

    def test_model_endswith_digit( self ):
        #
        oModel = Model.objects.get( cTitle = 'Model 2' )
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
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertEmpty( sInTitle )
        #
        tFinders = ( r'Model[-/ ]*2\b|Model *Two',
                     r'Model *Two|Model[-/ ]*2\b' )
        #
        self.assertIn( oModel.cRegExLook4Title, tFinders )
        #
        sAuctionTitle = 'Model 2 amplifier'
        #
        sInTitle, bExcludeThis = foundItem( sAuctionTitle )
        #
        self.assertEqual( 'Model 2', sInTitle )
        #



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
