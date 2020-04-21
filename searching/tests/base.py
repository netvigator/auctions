from pprint             import pprint

from json.decoder       import JSONDecodeError

from django.utils       import timezone

from core.tests.base    import ( GetEbayCategoriesWebTestSetUp,
                                 getNamePositionDict,
                                 getTableFromScreenCaptureGenerator )

from ebayinfo.models    import EbayCategory

from brands.models      import Brand
from categories.models  import Category, BrandCategory
from models.models      import Model

from finders.models     import ItemFound, UserFinder, UserItemFound

from searching          import RESULTS_FILE_NAME_PATTERN
from searching          import SEARCH_FILES_FOLDER

from searching.tests    import iRecordStepsForThis

from ..models           import Search, SearchLog
from ..tests            import ( sExampleResponse, sBrands, sModels,
                                 sResponseItems2Test,
                                 dSearchResult ) # in __init__.py

from ..utils            import ( storeSearchResultsInFinders,
                                 getSearchIdStr,
                                 _storeUserItemFound, _storeItemFound )

from ..utils_stars      import findSearchHits

from ..utilsearch       import ItemAlreadyInTable

from pyPks.File.Del     import DeleteIfExists
from pyPks.File.Write   import QuietDump
from pyPks.Utils.Config import getBoolOffYesNoTrueFalse



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
    def setUp(self):
        #
        super( StoreSearchResultsTestsWebTestSetUp, self ).setUp()
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
                   '000' ) )
        #
        QuietDump( sExampleResponse, SEARCH_FILES_FOLDER, self.sExampleFile )
        #
        tNow    = timezone.now()
        tBefore = tNow - timezone.timedelta( minutes = 5 )
        #
        oSearchLog = SearchLog(
                iSearch_id  = self.oSearch.id,
                tBegSearch  = tBefore,
                tEndSearch  = tNow,
                cResult     = 'Success' )
        #
        oSearchLog.save()
        #
        self.oSearchLog = oSearchLog
        #
        self.t = storeSearchResultsInFinders(
                    self.oSearchLog.id,
                    self.sMarket,
                    self.user1.username,
                    self.oSearch.id,
                    self.oSearch.cTitle,
                    self.setTestCategories,
                    bCleanUpFiles = False )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def tearDown(self):
        #
        DeleteIfExists( SEARCH_FILES_FOLDER, self.sExampleFile )
        #
        #ItemFound.objects.all().delete()
        #UserFinder.objects.all().delete()
        #UserItemFound.objects.all().delete()
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
        super( GetBrandsCategoriesModelsWebTestSetUp, self ).setUp()
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
            oCategory   = Category( cTitle      = 'Radio',
                                    iStars      = 9,
                                    cExcludeIf  = 'reproduction',
                                    iUser       = oUser )
            oCategory.save()
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
            oCategory   = Category( cTitle      = 'Vacuum Tube',
                                    cLookFor    = 'tube\rtubes\rVintage Tubes',
                                    cExcludeIf  = 'tube radio\r'
                                                   'tube clock radio\r'
                                                   'tube portable radio',
                                    iStars      = 6,
                                    iUser       = oUser )
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
            oCategory   = Category( cTitle      = 'Speaker System',
                                    cLookFor    = 'speaker',
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
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Crossover',
                                    iStars      = 7,
                                    cLookFor    = 'X-Over\rdividing network\rxover',
                                    iFamily_id  = oSpeakerSystem.id,
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
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Tuner',
                                    iStars      = 8,
                                    iFamily_id  = oStereoSystem.id,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Tube Tester',
                                    iStars      = 8,
                                    iUser       = oUser )
            oCategory.save()
            #
            oTubeTester = oCategory
            #
            #
            oCategory   = Category( cTitle      = 'Choke',
                                    cLookFor    = 'crossover',
                                    iStars      = 7,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category( cTitle      = 'Output Transformer',
                                    cLookFor    = 'Transformer\rTranformer',
                                    iStars      = 6,
                                    iUser       = oUser )
            oCategory.save()
            #
            oCategory   = Category(
                    cTitle      = 'Speaker Enclosure',
                    cLookFor    = 'Enclosure\rcabinet\rspeaker cabinet',
                    iStars      = 7,
                    iFamily_id  = oSpeakerSystem.id,
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
            lHeader = next( oTableIter )
            #
            d = getNamePositionDict( lHeader )
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
            oTableIter = getTableFromScreenCaptureGenerator( sModels )
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
                            print( '' )
                            print( 'got more than one brand %s' % sBrand )
                        #
                        oBrand = oBrand.first()
                        #
                    else:
                        #
                        print( '' )
                        print( 'do not have brand %s' % sBrand )
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
                        print( 'not finding category %s for %s!' %
                            ( sCategory, sBrand ) )
                    elif sBrand:
                        print(
                            "need a category but ain't got one! (do got brand %s)" % sBrand )
                    else:
                        print(
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
            oBrand = Brand.objects.get( cTitle = 'GE', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #
            oBrand = Brand.objects.get( cTitle = 'RCA', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
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
            oBrand = Brand.objects.get( cTitle = 'Tung-Sol', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
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
            oBrand = Brand.objects.get( cTitle = 'Mullard IEC/10M', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
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
            oBrand = Brand.objects.get( cTitle = 'Raytheon', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
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
            oBrand = Brand.objects.get( cTitle = 'Marconi', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
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
            oBrand = Brand.objects.get( cTitle = 'Amperex', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
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
            oBrand = Brand.objects.get( cTitle = 'Amperex PQ', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
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
            oBrand = Brand.objects.get( cTitle = 'Valvo', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
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
            oBrand = Brand.objects.get( cTitle = 'Siemens', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
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
            oBrand = Brand.objects.get( cTitle = 'Genalex (Gold Lion)', iUser = oUser )
            #
            oBrandCategory = BrandCategory(
                                    iBrand      = oBrand,
                                    iCategory   = oVacuumTubes,
                                    iUser       = oUser )
            #
            oBrandCategory.save()
            #



class PutSearchResultsInDatabaseWebTestBase( GetBrandsCategoriesModelsWebTestSetUp ):
    #
    ''' class for testing storeSearchResultsInFinders() store records '''
    #
    def setUp( self ):
        #
        super( PutSearchResultsInDatabaseWebTestBase, self ).setUp()
        #
        self.dExampleFiles = {}
        #
        for oUser in self.tUsers:
            #
            sExampleFile = (
                RESULTS_FILE_NAME_PATTERN % # 'Search_%s_%s_ID_%s_p_%s_.json'
                ( 'EBAY-US',
                oUser.username,
                getSearchIdStr( self.oSearch.id ),
                '000' ) )
            #
            self.dExampleFiles[ oUser.id ] = sExampleFile
            #
            #print( 'will DeleteIfExists' )
            DeleteIfExists( SEARCH_FILES_FOLDER, sExampleFile )
            #
            #print( 'will QuietDump' )
            QuietDump( sResponseItems2Test, SEARCH_FILES_FOLDER, sExampleFile )
            #
            try:
                t = ( storeSearchResultsInFinders(
                                self.oSearchLog.id,
                                self.sMarket,
                                oUser.username,
                                self.oSearch.id,
                                self.oSearch.cTitle,
                                self.setTestCategories ) )
                #
            except JSONDecodeError:
                #
                print('')
                print(  '### maybe a new item title has a quote '
                        'but only a single backslash ###' )
                #
                raise
                #
            #
            #iCountItems, iStoreItems, iStoreUsers = t
            #
            #iTempItems = ItemFoundTemp.objects.all().count()
            #iItemFound = ItemFound.objects.all().count()
            #
            # bCleanUpAfterYourself must be False or tests will fail!
            #
            #print( '\n' )
            #print( 'setting up PutSearchResultsInDatabaseWebTest' )

    def tearDown(self):
        #
        for sExampleFile in self.dExampleFiles.values():
            #
            DeleteIfExists( SEARCH_FILES_FOLDER, sExampleFile )
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
        super( SetUpForHitStarsWebTests, self ).setUp()
        #
        # bCleanUpAfterYourself must be False or tests will fail!
        # iRecordStepsForThis imported from __init__.py
        #
        findSearchHits( self.user1.id,
                        bCleanUpAfterYourself   = False,
                        iRecordStepsForThis     = iRecordStepsForThis )
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

    def setUp( self ):
        #
        '''set up to test _storeUserItemFound() with actual record'''
        #
        super( StoreUserItemFoundWebTestBase, self ).setUp()
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

