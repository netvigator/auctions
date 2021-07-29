from json.decoder           import JSONDecodeError

from django.utils           import timezone

from core.dj_import         import ObjectDoesNotExist
from core.tests.base        import GetEbayCategoriesWebTestSetUp
from core.utils             import maybePrint

from ebayinfo.models        import EbayCategory

from brands.models          import Brand
from categories.models      import Category, BrandCategory
from models.models          import Model

from finders.models         import ItemFound, UserFinder, UserItemFound

from searching              import RESULTS_FILE_NAME_PATTERN, SEARCH_FILES_ROOT

from ..models               import Search, SearchLog
# in __init__.py
from ..tests                import ( sExampleResponse, sBrands, sModels,
                                     sResponseItems2Test, sManualItems2Test,
                                     dSearchResult, iRecordStepsForThis )

from ..utils                import ( storeSearchResultsInFinders,
                                     getSearchIdStr,
                                     _storeUserItemFound, _storeItemFound )

from ..utils_stars          import findSearchHits

from ..utilsearch           import ItemAlreadyInTable

from pyPks.Dir.Get          import getMakeDir
from pyPks.File.Del         import DeleteIfExists
from pyPks.File.Write       import QuietDump
from pyPks.Time.Output      import getIsoDate
from pyPks.Utils.Config     import getBoolOffYesNoTrueFalse
from pyPks.Utils.DataBase   import ( getNamePositionDict,
                                     getTableFromScreenCaptureGenerator )


sTODAY = getIsoDate()


def getItemHitsLog( sPathFile ):
    #
    oHitsLogIter = getTableFromScreenCaptureGenerator( open( sPathFile ) )
    #
    lHeader = next( oHitsLogIter )
    #
    d = getNamePositionDict( lHeader )
    #
    lItemHits = []
    #
    for lParts in oHitsLogIter:
        #
        dRow = dict(
                iItemNumb   = lParts[ d['iItemNumb'] ],
                tTimeEnd    = lParts[ d['tTimeEnd' ] ],
                iHitStars   = lParts[ d['iHitStars'] ] )
        #
        lItemHits.append( dRow )
        #
    #
    return lItemHits



class StoreSearchResultsTestsWebTestSetUp( GetEbayCategoriesWebTestSetUp ):
    #
    ''' class for testing storeSearchResultsInFinders() store records '''
    #
    '''obsolete when the changes started in June 2021 are complete'''
    #
    def setUp(self):
        #
        super().setUp()
        #
        sSearch = "My clever search 1"
        oSearch = Search( cTitle = sSearch, iUser = self.user1 )
        oSearch.save()
        #
        self.oSearchMain = oSearch
        #
        self.sMarket = 'EBAY-US'
        #
        self.sExampleFileMain = (
            RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
                ( self.sMarket,
                   self.user1.username,
                   getSearchIdStr( oSearch.id ),
                   '000' ) )
        #
        getMakeDir( SEARCH_FILES_ROOT, sTODAY )
        #
        QuietDump( sExampleResponse, SEARCH_FILES_ROOT, sTODAY, self.sExampleFileMain )
        #
        tNow    = timezone.now()
        tBefore = tNow - timezone.timedelta( minutes = 5 )
        #
        oSearchLog = SearchLog(
                iSearch_id  = self.oSearchMain.id,
                tBegSearch  = tBefore,
                tEndSearch  = tNow,
                cResult     = 'Success' )
        #
        oSearchLog.save()
        #
        self.oSearchMainLog = oSearchLog
        #
        #print( '\nstoring new items now, this one should work' )
        self.tMain = storeSearchResultsInFinders(
                        self.oSearchMainLog.id,
                        self.sMarket,
                        self.user1.username,
                        self.oSearchMain.id,
                        self.oSearchMain.cTitle,
                        sTODAY,
                        self.setTestCategories,
                        bCleanUpFiles = False )
        #
        #
        sSearch = "My clever Manual search"
        oSearch = Search( cTitle        = sSearch,
                          iMyCategory   = self.ManualCategory,
                          iUser         = self.user1 )
        oSearch.save()
        #
        self.oSearchManual = oSearch
        #
        self.sMarket = 'EBAY-US'
        #
        self.sExampleFileManual = (
            RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
                ( self.sMarket,
                   self.user1.username,
                   getSearchIdStr( oSearch.id ),
                   '000' ) )
        #
        QuietDump( sExampleResponse, SEARCH_FILES_ROOT, sTODAY, self.sExampleFileManual )
        #
        tNow    = timezone.now()
        tBefore = tNow - timezone.timedelta( minutes = 5 )
        #
        oSearchLog = SearchLog(
                iSearch_id  = self.oSearchManual.id,
                tBegSearch  = tBefore,
                tEndSearch  = tNow,
                cResult     = 'Success' )
        #
        oSearchLog.save()
        #
        self.oSearchManualLog = oSearchLog
        #
        #print( 'storing same items again, this one should not work' )
        self.tManual = storeSearchResultsInFinders(
                        self.oSearchManualLog.id,
                        self.sMarket,
                        self.user1.username,
                        self.oSearchManual.id,
                        self.oSearchManual.cTitle,
                        sTODAY,
                        self.setTestCategories,
                        bCleanUpFiles = False )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def tearDown(self):
        #
        DeleteIfExists( SEARCH_FILES_ROOT, sTODAY, self.sExampleFileMain )
        #
        ItemFound.objects.all().delete()
        UserFinder.objects.all().delete()
        UserItemFound.objects.all().delete()
        SearchLog.objects.all().delete()
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


def getB( sSomething ):
    #
    bReturn = False
    #
    if sSomething:
        #
        bReturn = getBoolOffYesNoTrueFalse( sSomething )
        #
    #
    return bReturn



class GetBrandsCategoriesModelsWebTestSetUp( StoreSearchResultsTestsWebTestSetUp ):
    #
    ''' base class for testing trySearchCatchExceptStoreInFile() &
    storeSearchResultsInFinders() store records '''
    #

    def setUp(self):
        #
        super().setUp()
        #
        for oUser in self.tUsers:
            #
            sSearch = "Catalin Radios"
            sKeyWords = 'catalin radio'
            #
            if Search.objects.filter(
                    cKeyWords = sKeyWords,
                    iUser = oUser ).exists():
                #
                self.oCatalinSearch = Search.objects.filter(
                                        cKeyWords = sKeyWords,
                                        iUser = oUser ).first()
                #
            else:
                #
                self.oCatalinSearch = Search(
                                cTitle      = sSearch,
                                cKeyWords   = sKeyWords,
                                iUser       = oUser )
                #
                self.oCatalinSearch.save()
                #
            #
            sSearch         = 'Tube Preamps'
            iEbayCategory   = 67807
            #
            if Search.objects.filter(
                    cTitle = sSearch,
                    iUser = oUser  ).exists():
                #
                self.oPreampSearch = Search.objects.filter(
                                        cTitle = sSearch,
                                        iUser = oUser ).first()
                #
            else:
                #
                oEbayCateID = EbayCategory.objects.get(
                        name = 'Vintage Preamps & Tube Preamps' )
                #
                self.oPreampSearch = Search(
                                cTitle          = sSearch,
                                iEbayCategory   = oEbayCateID,
                                iUser           = oUser )
                #
                self.oPreampSearch.save()
                #
            #
            sSearch         = 'Manuals'
            iEbayCategory   = 39996
            if Search.objects.filter(
                    cTitle = sSearch,
                    iUser = oUser  ).exists():
                #
                self.oManualSearch = Search.objects.filter(
                                        cTitle = sSearch,
                                        iUser = oUser ).first()
                #
            else:
                #
                oEbayCateID = EbayCategory.objects.get(
                        name = 'Vintage Manuals' )
                #
                self.oManualSearch = Search(
                                cTitle          = sSearch,
                                iEbayCategory   = oEbayCateID,
                                iMyCategory     = self.ManualCategory,
                                iUser           = oUser )
                #
                self.oManualSearch.save()
                #
            #


            #
            oCategory   = Category( cTitle      = 'Radio',
                                    iStars      = 9,
                                    cExcludeIf  = 'reproduction',
                                    iUser       = oUser )
            oCategory.save()
            #
            oRadioCategory = oCategory
            #
            #
            oCategory   = Category( cTitle      = 'Stereo System',
                                    iStars      = 3,
                                    iUser       = oUser )
            oCategory.save()
            #
            oStereoSystem = oCategory
            #
            #
            oCategory   = Category( cTitle      = 'Preamp',
                                    cLookFor    = 'preamplifier\r'
                                                  'master control\rpre amp',
                                    iStars      = 9,
                                    iFamily_id  = oStereoSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            #
            oCategory   = Category( cTitle      = 'Tube Tester',
                                    iStars      = 8,
                                    cExcludeIf  = 'tested',
                                    iUser       = oUser )
            oCategory.save()
            #
            oTubeTester = oCategory
            #
            #
            oCategory   = Category( cTitle      = 'Vacuum Tube',
                                    cLookFor    = 'tube\rtubes\rVintage Tubes',
                                    cExcludeIf  = 'tube radio\r'
                                                  'tube clock radio\r'
                                                  'tube portable radio',
                                    iStars      = 6,
                                    iUser       = oUser )
            #                       iFamily_id  = oTubeTester.id,
            oCategory.save()
            #
            oVacuumTubes = oCategory
            #
            oCategory   = Category( cTitle      = 'Book',
                                    cLookFor    = 'tube\rtubes',
                                    cExcludeIf  = 'book shelf\rdigital',
                                    iStars      = 5,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Tube Manual',
                                    iStars      = 9,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Speaker System',
                                    cLookFor    = 'speaker\rmonitor',
                                    iFamily_id  = oStereoSystem.id,
                                    iStars      = 9,
                                    iUser       = oUser )
            oCategory.save()
            #
            oSpeakerSystem = oCategory
            #
            oCategory.iFamily_id                = oCategory.id
            #
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Driver',
                                    cLookFor    = 'speaker\rdrive\rwoofer\r'
                                                  'horn driver',
                                    iStars      = 8,
                                    iFamily_id  = oSpeakerSystem.id,
                                    bComponent  = True,
                                    iUser       = oUser )
            oCategory.save()
            #
            oDriver     = oCategory
            #
            oCategory   = Category( cTitle      = 'Crossover',
                                    iStars      = 7,
                                    cLookFor    = 'X-Over\r'
                                                  'dividing network\r'
                                                  'xover\r'
                                                  'crossover network\r'
                                                  'speaker crossover network',
                                    iFamily_id  = oSpeakerSystem.id,
                                    bComponent  = True,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Amplifier',
                                    cLookFor    = 'amp',
                                    cExcludeIf  = 'Table Radio\rPre-amplifier\r'
                                                'Pre-amp\rFuse Holder\rCapacitor',
                                    iStars      = 10,
                                    iFamily_id  = oStereoSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Horn',
                                    cExcludeIf  = 'horn driver',
                                    iStars      = 6,
                                    iFamily_id  = oSpeakerSystem.id,
                                    bComponent  = True,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Tuner',
                                    iStars      = 8,
                                    iFamily_id  = oStereoSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Tuner-Preamplifier',
                                    cLookFor    = 'pre amp tuner\rtuner pre amp',
                                    iStars      = 5,
                                    iFamily_id  = oStereoSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Choke',
                                    cLookFor    = 'crossover',
                                    iStars      = 7,
                                    bComponent  = True,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Output Transformer',
                                    cLookFor    = 'Transformer\rTranformer',
                                    iStars      = 6,
                                    bComponent  = True,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Power Transformer',
                                    cLookFor    = 'Transformer\rTranformer',
                                    iStars      = 6,
                                    bComponent  = True,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category(
                    cTitle      = 'Speaker Enclosure',
                    cLookFor    = 'Enclosure\rcabinet\rspeaker cabinet',
                    iStars      = 7,
                    iFamily_id  = oSpeakerSystem.id,
                    bComponent  = True,
                    iUser       = oUser )
            #
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Accessory',
                                    cLookFor    = 'adaptor\radapter',
                                    iStars      = 5,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category(
                    cTitle      = 'Integrated Amp',
                    cLookFor    = 'Amp\rAmplifier',
                                    iStars      = 4,
                                    iUser       = oUser )
            oCategory.save()
            #
            #
            oCategory   = Category(
                    cTitle      = 'Theater Amp',
                    cLookFor    = 'Amp\rAmplifier',
                                    iStars      = 9,
                                    iUser       = oUser )
            oCategory.save()
            #
            #
            oCategory   = Category(
                    cTitle      = 'Diaphragm',
                    cLookFor    = 'Diaphram',
                    iStars      = 7,
                    iFamily_id  = oSpeakerSystem.id,
                    bComponent  = True,
                    iUser       = oUser )
            #
            oCategory.save()
            #
            #
            oCategory   = Category(
                    cTitle      = 'roll chart (tube tester)',
                    cLookFor    = 'tube testor roll chart\r'
                                  'tube tester roll chart',
                    iStars      = 5,
                    iFamily_id  = oTubeTester.id,
                    bComponent  = True,
                    iUser       = oUser )
            oCategory.save()
            #
            #
            oCategory   = Category(
                    cTitle      = 'Component',
                    iStars      = 6,
                    bComponent  = True,
                    iUser       = oUser )
            #
            oCategory.save()
            #
            #
            oCategory   = Category(
                    cTitle      = 'Power Supply',
                    cLookFor    = 'power source',
                    iStars      = 5,
                    iUser       = oUser )
            #
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Subwoofer',
                                    cLookFor    = 'speaker',
                                    iFamily_id  = oStereoSystem.id,
                                    iStars      = 7,
                                    iUser       = oUser )
            oCategory.save()
            #
            #
            #
            #
            # Capacitor Checker is in core.tests.base.py already!
            #
            if not Category.objects.filter(
                    cTitle      = 'Capacitor Checker',
                    iUser       = oUser ).exists():
                #
                oCategory   = Category(
                    cTitle      = 'Capacitor Checker',
                    cLookFor    = 'Capacitor Tester\r'
                                  'Capacitance Checker\r'
                                  'Capacitance Tester',
                    iStars      = 5,
                    iUser       = oUser )
                #
                oCategory.save()
                #
            #
            #
            #
            #
            oTableIter = getTableFromScreenCaptureGenerator( sBrands )
            #
            tHeader = next( oTableIter )
            #
            d = getNamePositionDict( tHeader )
            #
            for lParts in oTableIter:
                #
                oBrand = Brand(
                    cTitle      =      lParts[ d['cTitle'    ] ],
                    iStars      = int( lParts[ d['iStars'    ] ] ),
                    cExcludeIf  =      lParts[ d['cExcludeIf'] ],
                    cKeyWords   =      lParts[ d['cKeyWords' ] ],
                    cLookFor    =      lParts[ d['cLookFor'  ] ],
                    iUser       = oUser )
                #
                oBrand.save()
                #
            #
            oTableIter = getTableFromScreenCaptureGenerator(
                                sModels, bListOut = True )
            #
            lHeader = next( oTableIter )
            #
            d = getNamePositionDict( lHeader )
            #
            iHeaderLen = len( lHeader )
            #
            for lParts in oTableIter:
                #
                if len( lParts ) < iHeaderLen:
                    #
                    lRest = lHeader[ len( lParts ) : ]
                    #
                    for sHead in lRest:
                        #
                        if sHead.startswith( 'b' ):
                            #
                            lParts.append( 'f' ) # for getBoolOffYesNoTrueFalse()
                            #
                        else:
                            #
                            lParts.append( '' )
                            #
                        #
                    #
                #
                sBrand    = lParts[ d['Brand'   ] ]
                sCategory = lParts[ d['Category'] ]
                #
                if sBrand:
                    #
                    bHaveBrand = Brand.objects.filter(
                                    cTitle = sBrand,
                                    iUser = oUser ).exists()
                    #
                    if bHaveBrand:
                        #
                        oBrand = Brand.objects.filter(
                                    cTitle = sBrand,
                                    iUser = oUser )
                        #
                        if len( oBrand ) > 1:
                            maybePrint( '' )
                            maybePrint( 'got more than one brand %s' % sBrand )
                        #
                        oBrand = oBrand.first()
                        #
                    else:
                        #
                        maybePrint( '' )
                        maybePrint( 'do not have brand %s' % sBrand )
                        oBrand = None
                        #
                else: # not sBrand, blank, generic model
                    #
                    oBrand = None
                    #
                #
                try:
                    oCategory = Category.objects.get(
                                    cTitle = sCategory,
                                    iUser = oUser )
                except ObjectDoesNotExist:
                    if sCategory and sBrand:
                        maybePrint( 'not finding category %s for %s!' %
                            ( sCategory, sBrand ) )
                    elif sBrand:
                        maybePrint(
                            "need a category but ain't got one! (do got brand %s)" % sBrand )
                    elif sCategory:
                        maybePrint(
                            "not finding category %s!" % sCategory )
                    else:
                        maybePrint(
                            "supposed to have a brand & category here "
                            "but ain't got nothin!" )
                    raise
                #
                oModel = Model(
                    cTitle          =       lParts[ d['cTitle'        ] ],
                    cKeyWords       =       lParts[ d['cKeyWords'     ] ],
                    iStars          = int(  lParts[ d['iStars'        ] ] ),
                    bSubModelsOK    = getB( lParts[ d['bSubModelsOK'  ] ] ),
                    cLookFor        =       lParts[ d['cLookFor'      ] ],
                    cExcludeIf      =       lParts[ d['cExcludeIf'    ] ],
                    bGenericModel   = getB( lParts[ d['bGenericModel' ] ] ),
                    bMustHaveBrand  = getB( lParts[ d['bMustHaveBrand'] ] ),
                    iBrand          = oBrand,
                    iCategory       = oCategory,
                    iUser           = oUser )
                #
                oModel.save()
                #
            #
            oBrand = Brand.objects.get( cTitle = 'GE (5 Star)', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'GE', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'RCA', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oRadioCategory,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Philips', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Tung-Sol', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Mullard', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Mullard 10M', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Mullard IEC', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Mazda', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Raytheon', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Sylvania', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Marconi', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Matsushita', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Westinghouse',
                                        iUser  = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Amperex', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Amperex (Bugle Boy)',
                                        iUser  = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Amperex (gold pins)',
                                        iUser  = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Amperex (PQ)', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Ken-Rad', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Valvo', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Telefunken', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Siemens', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Lorenz', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Genalex (Gold Lion)', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Western Electric', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Cunningham', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'JBL', iUser = oUser )
            #
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oDriver,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Fada', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oRadioCategory,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Tungsram', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Concertone', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            #
            oBrand = Brand.objects.get( cTitle = 'National Union', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Servicemaster', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Osram', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            #
            #
            oBrand = Brand.objects.get( cTitle = 'Delco', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Genalex (Russian)', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Fivre', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'Brimar', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'GEC (Genalex)', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            # if you add a new brand here,
            # the brand must also be added to the list in __init__.py



class PutSearchResultsInDatabaseWebTestBase( GetBrandsCategoriesModelsWebTestSetUp ):
    #
    ''' class for testing storeSearchResultsInFinders() store records '''
    #
    def setUp( self ):
        #
        super().setUp()
        #
        self.dExampleFiles = {}
        #
        for oUser in self.tUsers:
            #
            sExampleFile = (
                RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
                ( 'EBAY-US',
                oUser.username,
                getSearchIdStr( self.oSearchMain.id ),
                '000' ) )
            #
            self.dExampleFiles[ oUser.id ] = sExampleFile
            #
            #print( 'will DeleteIfExists' )
            DeleteIfExists( SEARCH_FILES_ROOT, sTODAY, sExampleFile )
            #
            #print( 'will QuietDump' )
            QuietDump( sResponseItems2Test, SEARCH_FILES_ROOT, sTODAY, sExampleFile )
            #
            #print( 'PutSearchResultsInDatabaseWebTestBase main storing items' )
            try:
                t = storeSearchResultsInFinders(
                        self.oSearchMainLog.id,
                        self.sMarket,
                        oUser.username,
                        self.oSearchMain.id,
                        self.oSearchMain.cTitle,
                        sTODAY,
                        self.setTestCategories )
                #
            except JSONDecodeError:
                #
                maybePrint('')
                maybePrint(  '### maybe a new item title has a quote '
                        'but only a single backslash ###' )
                maybePrint(  '### or you forgot to include the comma '
                        'at the end of a new item ###' )
                #
                raise
                #
            #
            #
            sExampleFile = (
                RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
                ( 'EBAY-US',
                oUser.username,
                getSearchIdStr( self.oSearchManual.id ),
                '000' ) )
            #
            self.dExampleFiles[ oUser.id ] = sExampleFile
            #
            #print( 'will DeleteIfExists' )
            DeleteIfExists( SEARCH_FILES_ROOT, sTODAY, sExampleFile )
            #
            #print( 'will QuietDump' )
            QuietDump( sManualItems2Test, SEARCH_FILES_ROOT, sTODAY, sExampleFile )
            #
            #print( 'PutSearchResultsInDatabaseWebTestBase manual storing items' )
            try:
                t = ( storeSearchResultsInFinders(
                                self.oSearchManualLog.id,
                                self.sMarket,
                                oUser.username,
                                self.oSearchManual.id,
                                self.oSearchManual.cTitle,
                                sTODAY,
                                self.setTestCategories ) )
                #
            except JSONDecodeError:
                #
                maybePrint('')
                maybePrint(  '### maybe a new item title has a quote '
                        'but only a single backslash ###' )
                #
                raise
                #
            #
            # sManualItems2Test
            #iCountItems, iStoreItems, iStoreUsers = t
            #
            #iTempItems = ItemFoundTemp.objects.all().count()
            #iItemFound = ItemFound.objects.all().count()
            #
            #print( '\n' )
            #print( 'setting up PutSearchResultsInDatabaseWebTest' )

    def tearDown(self):
        #
        for sExampleFile in self.dExampleFiles.values():
            #
            pass # DeleteIfExists( SEARCH_FILES_ROOT, sTODAY, sExampleFile )
            #
        #
        #ItemFound.objects.all().delete()
        #UserFinder.objects.all().delete()
        #UserItemFound.objects.all().delete()
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


class SetUpForHitStarsWebTests( PutSearchResultsInDatabaseWebTestBase ):
    #
    ''' class for testing findSearchHits() hit star calculations '''
    #
    def setUp( self ):
        #
        super().setUp()
        #
        findSearchHits( self.user1.id, iRecordStepsForThis )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def tearDown(self):
        #
        #ItemFound.objects.all().delete()
        #UserFinder.objects.all().delete()
        #UserItemFound.objects.all().delete()
        #
        pass
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


class StoreUserItemFoundWebTestBase( GetEbayCategoriesWebTestSetUp ):
    #
    ''' class for testing _storeUserItemFound() '''
    #
    '''obsolete when the changes started in June 2021 are complete'''
    #

    def setUp( self ):
        #
        '''set up to test _storeUserItemFound() with actual record'''
        #
        super().setUp()
        #
        class ThisShouldNotBeHappening( Exception ): pass
        #
        self.oSearch = None
        #
        tNow        = timezone.now()
        tBefore     = tNow - timezone.timedelta( minutes = 5 )
        #
        sSearch     = "My clever search 1"
        #
        for oUser in self.tUsers:
            #
            oSearch = Search( cTitle = sSearch, iUser = oUser )
            oSearch.save()
            #
            if self.oSearch is None: self.oSearch = oSearch
            #
            try:
                #
                iItemNumb = _storeItemFound( dSearchResult, {} )
                #
            except ItemAlreadyInTable:
                #
                iItemNumb = int( dSearchResult['itemId' ] )
                #
            #
            if iItemNumb is None:
                raise ThisShouldNotBeHappening
            #
            try:
                _storeUserItemFound(
                    dSearchResult, iItemNumb, oUser, oSearch.id )
            except ItemAlreadyInTable:
                pass
            #
            self.iItemNumb  = iItemNumb
            self.tNow       = tNow
            #
            oSearchLog = SearchLog(
                    iSearch_id  = oSearch.id,
                    tBegSearch  = tBefore,
                    tEndSearch  = tNow,
                    tBegStore   = tNow,
                    cResult     = 'Success' )
            #
            oSearchLog.save()
            #
        #

