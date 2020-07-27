import logging

from copy                   import copy, deepcopy
from pprint                 import pprint, pformat

from collections            import OrderedDict

from itertools              import chain

from django.conf            import settings
from django.db.models       import Q, Max
from django.contrib.auth    import get_user_model
from django.utils           import timezone

from core.user_one          import oUserOne
from core.utils             import ( maybePrint, maybePrettyP,
                                     getWhatsNotInParens )

from core.templatetags.core_tags import getDashForReturn

from .models                import Search, SearchLog

from brands.models          import Brand

from categories.models      import Category, BrandCategory

from finders.models         import ItemFound, UserItemFound, UserFinder

from models.models          import Model

from searching              import ( WORD_BOUNDARY_MAX, SCRIPT_TEST_FILE,
                                     DROP_AFTER_THIS, WITH_AND_JOINERS )

from pyPks.Collect.Get      import getListFromNestedLists
from pyPks.Collect.Output   import getTextSequence
from pyPks.Collect.Query    import get1stThatMeets
from pyPks.Collect.Test     import allMeet, containsAny, containsAll

from pyPks.Dict.Get         import getReverseDictCarefully, getDictSubset

from pyPks.File.Get         import getListFromFileLines
from pyPks.File.Test        import isFileThere
from pyPks.File.Write       import QuickDumpLines

from pyPks.Object.Get       import ValueContainer
from pyPks.Object.Output    import CustomPPrint

from pyPks.String.Count     import getAlphaNumCount as getLen
from pyPks.String.Dumpster  import getAlphaNumCleanNoSpaces
from pyPks.String.Eat       import eatPunctuationBegAndEnd
from pyPks.String.Get       import getTextBeforeC, getParensParts
from pyPks.String.Find      import getRegExpress, getRegExObj
from pyPks.String.Find      import oFinderCRorLFnMore as oFinderCRorLF
from pyPks.String.Replace   import getSpaceForWhiteAlsoStrip
from pyPks.String.Output    import ReadableNo, Plural
from pyPks.String.Stats     import getStrLocationsBegAndEnd

if settings.TESTING:

    from pyPks.Object.Get   import ValueContainerCanPrint as ValueContainer


logger = logging.getLogger(__name__)

logging_level = logging.WARNING


_oDropAfterThisFinder = getRegExObj( DROP_AFTER_THIS )



class HitsListClass( list ):

    tPROPERTIES = (
        'iHitStars',
        'oSearch',
        'oModel',
        'oBrand',
        'oCategory',
        'iStarsModel',
        'iStarsBrand',
        'iStarsCategory',
        'cFoundModel',
        'iFoundModelLen',
        'bModelKeyWords',
        'cModelAlphaNum',
        'cTitleLeftOver',
        'cWhereCategory',
        'bIncludeThis' ) # bIncludeThis
    #
    _dDefaults = dict(
            iStars = 1,
            iFound = 0,
            bModel = False,
            bInclu = True,
            cWhere = 'title' ) # todo: remove this, None should be OK

    # oItemFound should be here
    oItemFound          = None # ItemsFound table row (django ORM object)
    lCategoryFound      = [] # list of categories (django ORM objects)
    dGotCategories      = {} # key oCategory.id, value sInTitle
    dModelIDinTitle     = {} # key oModel.id ]
        #                      value = ValueContainer(
        #                               sInTitle    = sInTitle,
        #                               oCategory   = oCategory,
        #                               oBrand      = oModel.iBrand,
        #                               sModelTitle = oModel.cTitle )
    dGotBrandIDsInTitle = {} # key oBrand.id, value sInTitle
    oModelLocated       = None
    bGotBrandForNonGenericModel = False

    bPrintOne           = True


    def __init__( self, **kwargs ):
        #
        self.__dict__.update( kwargs )

    def appendItem( self, **kwargs ):
        #
        for sProperty in self.tPROPERTIES:
            #
            if sProperty not in kwargs:
                #
                kwargs[ sProperty ] = self._dDefaults.get( sProperty[ : 6 ] )
                #
            #
        #
        oNewHit = ValueContainer( **kwargs )
        #
        self.append( oNewHit )
        #
        return oNewHit

    def appendCopy( self, oHit ):
        #
        oNewHit = deepcopy( oHit )
        #
        self.append( oNewHit )
        #
        return oNewHit

    def appendOneObject( self, oAddThis ):
        #
        self.append( oAddThis )
        #

    def appendObjects( self, *args ):
        #
        for o in args:
            #
            self.appendOneObject( o )

    def getProperties( self ):
        #
        return copy( vars( self ) )

    def appendCopy( self, oHit ):
        #
        oNewHit = deepcopy( oHit )
        #
        self.append( oNewHit )
        #
        return oNewHit

    def getCopyWithoutItems( self ):
        #
        dProperties = self.getProperties()
        #
        return HitsListClass( **dProperties )



def _getRelevantTitle( sTitle ):
    #
    sAuctionTitleRelevantPart = _oDropAfterThisFinder.split( sTitle )[0]
    #
    sGotInParens, sNotInParens = getParensParts( sTitle )
    #
    if sGotInParens:
        #
        lSplitInParens = _oDropAfterThisFinder.split( sGotInParens )
        #
        if len( lSplitInParens ) > 1:
            #
            sAuctionTitleRelevantPart = \
                    _oDropAfterThisFinder.split( sNotInParens )[0]
            #
        #
    #
    return sAuctionTitleRelevantPart, sGotInParens





def _getTitleRegExress(
            oTableRow,
            bAddDash        = False,
            bPluralize      = False,
            bExplainVerbose = False ):
    #
    '''gets the RegEx expression for title + look for
    (comibines title & look for into one RegEx expression)'''
    #
    bSubModelsOK = ( hasattr( oTableRow, 'bSubModelsOK' ) and
                     oTableRow.bSubModelsOK )
    #
    bTitleSubModelsOK = bSubModelsOK
    bLook4SubModelsOK = bSubModelsOK
    #
    sLook4Title       = getWhatsNotInParens( oTableRow.cTitle )
    #
    if bSubModelsOK and oTableRow.cLookFor:
        #
        if (    len( oTableRow.cLookFor ) > len( sLook4Title ) and
                     oTableRow.cLookFor.startswith( sLook4Title ) ):
            #
            bTitleSubModelsOK = False
            #
        elif (  len( sLook4Title ) > len( oTableRow.cLookFor ) and
                     sLook4Title.startswith( oTableRow.cLookFor ) ):
            #
            bLook4SubModelsOK = False
            #
        #
    #
    sRegExpress = getRegExpress( sLook4Title,
                                 bAddDash       = bAddDash,
                                 bSubModelsOK   = bTitleSubModelsOK,
                                 iWordBoundChrs = WORD_BOUNDARY_MAX,
                                 bPluralize     = bPluralize )
    #
    if oTableRow.cLookFor:
        #
        sLookFor = oTableRow.cLookFor.strip()
        #
        sLook4Express = getRegExpress(
                                sLookFor,
                                bAddDash       = bAddDash,
                                bSubModelsOK   = False,
                                iWordBoundChrs = WORD_BOUNDARY_MAX )
        #
        sRegExpress = '|'.join( ( sRegExpress, sLook4Express ) )
        #
        #if bExplainVerbose:
            #maybePrint('')
            #maybePrint('sLookFor:', sLookFor)
            #maybePrint('sLook4Express:', sLook4Express)
    #
    return sRegExpress





def _getRowRegExpressions( oTableRow,
                           bAddDash         = False,
                           bPluralize       = False,
                           bExplainVerbose  = False ):
    #
    '''if the row already has RegEx expressions stored, returns them;
    otherwise, generate the RegEx expressions, store them in the row,
    & return them'''
    #
    bAnyUpdates = False
    #
    bRowHasKeyWords = hasattr( oTableRow, 'cKeyWords' )
    #
    sFindTitle = sFindKeyWords = sFindExclude = None
    #
    if not oTableRow.cRegExLook4Title:
        #
        sFindTitle = _getTitleRegExress( oTableRow,
                                         bAddDash        = bAddDash,
                                         bPluralize      = bPluralize,
                                         bExplainVerbose = bExplainVerbose )
        #
        oTableRow.cRegExLook4Title = sFindTitle
        #
        bAnyUpdates = True
        #
    else:
        #
        sFindTitle = oTableRow.cRegExLook4Title
        #
    #
    if bRowHasKeyWords:
        #
        if oTableRow.cKeyWords and not oTableRow.cRegExKeyWords:
            #
            sFindKeyWords = getRegExpress(
                            oTableRow.cKeyWords,
                            bAddDash        = bAddDash,
                            iWordBoundChrs  = WORD_BOUNDARY_MAX )
            #
            oTableRow.cRegExKeyWords = sFindKeyWords
            #
            bAnyUpdates = True
            #
            #if 'etched' in oTableRow.cExcludeIf:
                #maybePrint('')
                #maybePrint( 'sFindKeyWords:', sFindKeyWords )
            #
        else:
            #
            sFindKeyWords = oTableRow.cRegExKeyWords
            #
        #
    #
    if oTableRow.cExcludeIf and not oTableRow.cRegExExclude:
        #
        # exclude any cExcludeIf lines that are a substring of cTitle
        # longer title takes priority over substring title
        # so the substring exclude if can block the correct hit
        #
        lLines = oFinderCRorLF.split( oTableRow.cExcludeIf )
        #
        sRelevantTitle = getWhatsNotInParens( oTableRow.cTitle )
        #
        iTitleLen = len( sRelevantTitle )
        #
        def excludeThis( s ):
            #
            return len( s ) < iTitleLen and sRelevantTitle.startswith( s )
            #
        #
        tWantLines = ( s for s in lLines if not excludeThis( s ) )
        #
        if tWantLines:
            #
            sExcludeIf = '\r'.join( tWantLines )
            #
            sFindExclude = getRegExpress(
                                sExcludeIf,
                                bAddDash        = bAddDash,
                                iWordBoundChrs  = WORD_BOUNDARY_MAX,
                                bEscBegEndOfStr = False )
            #
            oTableRow.cRegExExclude   = sFindExclude
            #
            bAnyUpdates = True
            #
        #
    else:
        #
        sFindExclude = oTableRow.cRegExExclude
        #
    #
    if bAnyUpdates:
        #
        try:
            oTableRow.save()
        except DataError as e:
            logger.error( 'DataError: %s' % e )
        #
    #
    return sFindTitle, sFindExclude, sFindKeyWords



def _getAlphaNum( s ): return getAlphaNumCleanNoSpaces( s ).upper()



def _getRegExObjOrNone( s ):
    #
    if s:
        #
        oRegExObj = getRegExObj( s )
        #
        return oRegExObj



def _includeOrExclude( s, findExclude ):
    #
    if findExclude is None:
        #
        return False
        #
    else:
        #
        return findExclude( s )


def _gotKeyWordsOrNoKeyWords( s, findKeyWords ):
    #
    return findKeyWords is None or findKeyWords( s )


def _getFoundItemTester(    oTableRow, dFinders,
                            bAddDash        = False,
                            bSubModelsOK    = False,
                            bPluralize      = False,
                            bExplainVerbose = False ):
    #
    ''' pass model row instance, returns tester '''
    #
    if oTableRow.pk in dFinders:
        #
        foundItemTester = dFinders[ oTableRow.pk ]
        #
    else:
        #
        tOrig = _getRowRegExpressions(
                        oTableRow,
                        bAddDash        = bAddDash,
                        bPluralize      = bPluralize,
                        bExplainVerbose = False )
        #
        t = tuple( map( _getRegExObjOrNone, tOrig ) )
        #
        findTitle, findExclude, findKeyWords = t
        #
        searchTitle = searchExclude = searchKeyWords = None
        #
        if findTitle    : searchTitle     = findTitle.search
        if findExclude  : searchExclude   = findExclude.search
        if findKeyWords : searchKeyWords  = findKeyWords.search
        #
        def foundItemTester( s, bExplainVerbose = bExplainVerbose ):
            #
            sFoundInTitle = ''
            #
            oTitleMatch = searchTitle( s )
            #
            if oTitleMatch: sFoundInTitle = oTitleMatch.group(0)
            #
            uExcludeThis = _includeOrExclude( s, searchExclude )
            #
            uGotKeyWordsOrNoKeyWords = _gotKeyWordsOrNoKeyWords(
                                            s, searchKeyWords )
            bGotKeyWords = ( uGotKeyWordsOrNoKeyWords and
                             searchKeyWords is not None )
            #
            sWhatRemains = ''
            #
            if (    sFoundInTitle and
                    uGotKeyWordsOrNoKeyWords and
                    isinstance( oTableRow, Model ) and
                    not uExcludeThis ):
                #
                sWhatRemains = getSpaceForWhiteAlsoStrip(
                                    ' '.join( findTitle.split( s ) ) )
                #
            #
            if ( settings.COVERAGE or True ) and bExplainVerbose: #
                maybePrint('')
                maybePrint('sFoundInTitle           :', sFoundInTitle )
                maybePrint('findTitle               :', findTitle )
                maybePrint('findTitle.pattern       :', findTitle.pattern )
                maybePrint('oTableRow.cLookFor      :', oTableRow.cLookFor )
                maybePrint('oTableRow.cExcludeIf    :', oTableRow.cExcludeIf )
                maybePrint('oTableRow.cKeyWords     :', oTableRow.cKeyWords )
                maybePrint('uGotKeyWordsOrNoKeyWords:', uGotKeyWordsOrNoKeyWords )
                maybePrint('bGotKeyWords            :', bGotKeyWords )
                maybePrint('sWhatRemains            :', sWhatRemains )
                #
            #
            return (    sFoundInTitle,
                        uGotKeyWordsOrNoKeyWords,
                        bGotKeyWords,
                        uExcludeThis,
                        sWhatRemains )
            #
        #
        dFinders[ oTableRow.pk ] = foundItemTester
        #
    #
    return foundItemTester


def _whichGetsCredit( sInTitle, bInHeirarchy1, bInHeirarchy2 ):
    #
    if sInTitle:
        #
        sReturn = 'title'
        #
    elif bInHeirarchy1:
        #
        sReturn = 'heirarchy1'
        #
    else: # bInHeirarchy2
        #
        sReturn = 'heirarchy2'
        #
    #
    return sReturn


def _printHitSearchSteps( oItemFound, dFindSteps ):
    #
    maybePrint('')
    maybePrint('Item %s Hit Search Steps:' % oItemFound.iItemNumb )
    maybePrint( oItemFound.cTitle )
    #
    for k, v in dFindSteps.items():
        #
        if not v: continue
        #
        # most items will not have any preliminary content
        #
        maybePrint( '  %s' % k )
        #
        for s in v:
            #
            maybePrint( '    %s' % s )
            #

def _getTitleOrNone( o ):
    #
    return o.cTitle if hasattr( o, 'cTitle' ) else 'None'


def _appendIfNotAlreadyIn( l, s ):
    #
    if s not in l:
        #
        l.append( s )


def _getModelFoundLen( sInTitle, sGotInParens ):
    #
    if sGotInParens and sInTitle in sGotInParens:
        #
        iFoundModelLen= getLen( sInTitle ) // 3
        #
    else:
        #
        iFoundModelLen= getLen( sInTitle )
        #
    #
    return iFoundModelLen



def _gotFullStringOrSubStringOfListItem( sTitle, lGotModels ):
    #
    uGotSub  = None
    uGotFull = None
    uGotMore = None
    #
    sTitleUpper = sTitle.upper()
    #
    for sGotModel in lGotModels:
        #
        sUpperModel = sGotModel.upper()
        #
        if sTitleUpper in sUpperModel:
            #
            if sTitleUpper == sUpperModel:
                uGotFull = getWhatsNotInParens( sGotModel )
            else:
                uGotSub  = getWhatsNotInParens( sGotModel )
            #
        elif sUpperModel in sTitleUpper:
            #
            lParts = sTitleUpper.split( sUpperModel )
            #
            if len( lParts ) == 2:
                #
                uGotMore = getWhatsNotInParens( sGotModel )
                #
            #
        #
    #
    return uGotFull, uGotSub, uGotMore


def _updateModelsStoredAlready(
            dModelsStoredAlready, oHitLine, sModelTitleUPPER ):
    #
    # dModelsStoredAlready used for scoring & selection
    #
    iCategoryID = None
    #
    if oHitLine.oCategory:
        iCategoryID = oHitLine.oCategory.id
    #
    oThisModel = ValueContainer(
        bGenericModel   = oHitLine.oModel.bGenericModel,
        iModelBrand     = oHitLine.oModel.iBrand,
        iBrand          = oHitLine.oBrand,
        bSubModelsOK    = oHitLine.oModel.bSubModelsOK,
        iModelID        = oHitLine.oModel.id,
        iHitStars       = oHitLine.iHitStars,
        bModelKeyWords  = oHitLine.bModelKeyWords,
        sTitleLeftOver  = oHitLine.cTitleLeftOver,
        iCategoryID     = iCategoryID,
        sModelTitleUPPER= sModelTitleUPPER )
    #
    dModelsStoredAlready.setdefault(
        sModelTitleUPPER, [] ).append( oThisModel )
    #


def _getMaxHitStars( dModelsStoredAlready ):
    #
    # dModelsStoredAlready used for scoring & selection
    #
    iMaxStars = iMaxModel = 0
    #
    tHitStarsModels = tuple(    ( o.iHitStars, o.iModelID )
                                for l in dModelsStoredAlready.values()
                                for o in l )
    #
    if tHitStarsModels:
        #
        iMaxStars = max( ( t[0] for t in tHitStarsModels ) )
        #
    #
    if iMaxStars:
        #
        def gotMax( t ): return t[0] == iMaxStars
        #
        tMax  = get1stThatMeets( tHitStarsModels, gotMax )
        #
        iMaxModel = tMax[1]
        #
    #
    return iMaxStars, iMaxModel



def _getBoosterOffPair( oLongr, oShort ):
    #
    iLongerStars = oLongr.iHitStars or 1
    iShortrStars = oShort.iHitStars or 1
    #
    nBoost = ( ( iShortrStars + 0.1 ) / iLongerStars ) ** 0.5
    #
    return nBoost



def _getFoundModelBooster( oHitsList, bRecordSteps ):
    #
    # if 415-C in title, want 415-C to get higher score than 415
    # especially when 415 has more stars than 415-C
    #
    iFoundModelBooster = 1
    #
    lAllFoundIns = []
    #
    iMaxLen = 0
    #
    lExactMatch = []
    #
    for o in oHitsList:
        #
        if  (   o.cFoundModel is not None and
                o.cModelAlphaNum == _getAlphaNum( o.cFoundModel ) ):
            #
            o.bExact = True
            #
            lExactMatch.append( o )
            #
        else:
            #
            o.bExact = False
            #
        #
    #
    dModelMaxStars = dict.fromkeys(
            ( o.cModelAlphaNum for o in oHitsList ), 0 )
    #
    for i in range( len( oHitsList ) ):
        #
        o = oHitsList[ i ]
        #
        if o.iFoundModelLen:
            #
            lAllFoundIns.append(
                ( o.iFoundModelLen, i, o.cModelAlphaNum, o.iHitStars ) )
            #
            iMaxLen = max( iMaxLen, o.iFoundModelLen )
            #
            dModelMaxStars[ o.cModelAlphaNum ] = (
                    max( dModelMaxStars[ o.cModelAlphaNum ],
                         o.iHitStars ) )
            #
        #
    #
    #
    #
    if len( lAllFoundIns ) < 2: return 1, iMaxLen, lExactMatch
    #
    #
    #
    lAllFoundIns.sort()
    lAllFoundIns.reverse()
    #
    #
    if bRecordSteps: # settings.COVERAGE and
        #
        maybePrint()
        maybePrint( 'lAllFoundIns (iLen, i [oHitsList], cModelAlphaNum, iHitStars):' )
        maybePrettyP( lAllFoundIns )
        #maybePrint( 'lExactMatch:' )
        #for o in lExactMatch:
            #maybePrint( ' ', o )
        #
    #
    lGotModelOverlap = []
    #
    for iOut in range( len( lAllFoundIns ) ):
        #
        for iIn in range( iOut + 1, len( lAllFoundIns ) ):
            #
            oLongr = oHitsList[ lAllFoundIns[ iOut ][ 1 ] ]
            oShort = oHitsList[ lAllFoundIns[ iIn  ][ 1 ] ]
            #
            if (    oLongr.iHitStars == dModelMaxStars[ oLongr.cModelAlphaNum ]
                    and
                    oShort.iHitStars > oLongr.iHitStars
                    and
                    oLongr.iFoundModelLen > oShort.iFoundModelLen
                    and
                    oLongr.cModelAlphaNum.startswith(
                    oShort.cModelAlphaNum ) ):
                #
                lGotModelOverlap.append( ( oLongr, oShort ) )
                #
                if bRecordSteps: # settings.COVERAGE and
                    #
                    maybePrint()
                    maybePrint( 'oLongr.iHitStars     :', oLongr.iHitStars      )
                    maybePrint( 'oShort.iHitStars     :', oShort.iHitStars      )
                    maybePrint( 'oLongr.cModelAlphaNum:', oLongr.cModelAlphaNum )
                    maybePrint( 'oShort.cModelAlphaNum:', oShort.cModelAlphaNum )
                    maybePrint( 'oLongr.cFoundModel   :', oLongr.cFoundModel    )
                    maybePrint( 'oShort.cFoundModel   :', oShort.cFoundModel    )
                    maybePrint( 'oLongr.bExact        :', oLongr.bExact         )
                    maybePrint( 'oShort.bExact        :', oShort.bExact         )
                    #
            #
        #
    #
    #
    #
    if not lGotModelOverlap: return 1, iMaxLen, lExactMatch
    #
    #
    #
    nBoost = iMaxLen = 0
    #
    for t in lGotModelOverlap:
        #
        oLongr, oShort = t
        #
        nBoost  = max( nBoost, _getBoosterOffPair( oLongr, oShort ) )
        #
        iMaxLen = max( iMaxLen, oLongr.iFoundModelLen )
    #
    if bRecordSteps: # settings.COVERAGE and
        #
        maybePrint()
        maybePrint( 'nBoost :', nBoost )
        maybePrint( 'iMaxLen:', iMaxLen )
        #

    #
    return nBoost, iMaxLen, lExactMatch




def _getCategoriesForPositions(
            tPositions,
            dLocationsModelIDs,
            dModelID_oHitsItem ):
    #
    lCategories = []
    #
    for iPosition in tPositions:
        #
        if iPosition in dLocationsModelIDs:
            #
            for iModelID in dLocationsModelIDs[ iPosition ]:
                #
                oHitLine = dModelID_oHitsItem[ iModelID ]
                #
                if oHitLine.oCategory is not None:
                    #
                    lCategories.append( oHitLine.oCategory.id )
                    #
                #
            #
        #
    #
    return frozenset( lCategories )



def _getModelLocationsBegAndEnd( sAuctionTitle, dModelIDinTitle ):
    #
    tWordsOfInterest = tuple(
            frozenset(
            [ o.sInTitle for o in dModelIDinTitle.values() ] ) )
    #
    oLocated = getStrLocationsBegAndEnd( sAuctionTitle, tWordsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd & tInParens
    #
    iGotCategories = len( frozenset( [ o.oCategory for o in dModelIDinTitle.values() ] ) )
    #
    if (    oLocated.tNearFront and
            (   oLocated.tOnEnd    or
                oLocated.tNearEnd  or
                oLocated.tInParens or
                iGotCategories == 1 ) ):
        #
        oLocated.iGotCategories = iGotCategories
        #
        dAllWordLocations = oLocated.dAllWordLocations
        #
        lTitleWords = []
        #
        for k, v in dAllWordLocations.items():
            #
            for i in v:
                #
                lTitleWords.append( ( i, k ) )
                #
            #
        #
        lTitleWords.sort()
        #
        tTitleWords = tuple( ( t[1] for t in lTitleWords ) )
        #
        oLocated.tTitleWords      = tTitleWords
        oLocated.tWordsOfInterest = tWordsOfInterest
        #
        oLocated.dAndWords = getDictSubset(
                dAllWordLocations, *WITH_AND_JOINERS )
        #
    else:
        #
        oLocated = None
        #
    #
    return oLocated



def _getSearchMyCategoryDict( oUser = oUserOne ):
    #
    dSearchMyCategory = {}
    #
    qsUserSearches = Search.objects.filter( iUser = oUser )
    #
    for oSearch in qsUserSearches:
        #
        dSearchMyCategory[ oSearch.id ] = oSearch.iMyCategory
        #
    #
    return dSearchMyCategory



def updateModelIDinTitle(
            dModelIDinTitle,
            oModel,
            sInTitle,
            oCategory ):
    #
    if oModel.id not in dModelIDinTitle:
        #
        dModelIDinTitle[ oModel.id ] = ValueContainer(
            sInTitle    = sInTitle,
            oCategory   = oCategory,
            oBrand      = oModel.iBrand,
            sModelTitle = oModel.cTitle )
        #
    #



def _doStepThruCategories(
            oItemFound,
            oUserItem,
            qsCategories,
            dFindersCategories,
            sAuctionTitleRelevantPart,
            dFindSteps,
            bRecordSteps ):
    #
    lModels         = dFindSteps[ 'models' ]
    lCategories     = dFindSteps[ 'categories' ]
    #
    # breaks findSearchHits() !
    # oHitsList  = HitsListClass()
    #
    # lCategoryFound  = oHitsList.lCategoryFound
    # dGotCategories  = oHitsList.dGotCategories
    #
    # to avoid breaking findSearchHits(), must do this:
    lCategoryFound  = []
    dGotCategories  = {}
    #
    oHitsList = HitsListClass(
                dGotCategories  = dGotCategories,
                lCategoryFound  = lCategoryFound,
                oItemFound      = oItemFound )
    #
    for oCategory in qsCategories:
        #
        foundItem = _getFoundItemTester(
                        oCategory,
                        dFindersCategories,
                        bPluralize = True )
        #
        t = foundItem( sAuctionTitleRelevantPart )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        uGotKeyWordsOrNoKeyWords = uGot
        #
        #
        # the following are short circuiting --
        # if one is True, the following will be True
        # and the string will not be searched
        # so don't take bInHeirarchy1 & bInHeirarchy2 literally!
        #
        bInHeirarchy1  = ( # will be True if sInTitle is True
                sInTitle or
                ( oItemFound.iCatHeirarchy and # can be None
                    foundItem(
                        oItemFound.iCatHeirarchy.cCatHierarchy )[0] ) )
        #
        bInHeirarchy2  = ( # will be True if either are True
                sInTitle or
                bInHeirarchy1 or
                ( oItemFound.i2ndCatHeirarchy and
                    foundItem(
                        oItemFound.i2ndCatHeirarchy.cCatHierarchy )[0] ) )
        #
        #
        bGotCategory = sInTitle or bInHeirarchy1 or bInHeirarchy2
        #
        if not bGotCategory: # sInTitle or bInHeirarchy1 or bInHeirarchy2
            #
            continue
            #
        elif uExcludeThis:
            #
            if bRecordSteps:
                #
                _appendIfNotAlreadyIn(
                        lCategories, 'excluded: %s cuz found %s' %
                        ( oCategory.cTitle, uExcludeThis ) )
                #
            #
            continue
            #
        elif not uGotKeyWordsOrNoKeyWords:
            #
            if bRecordSteps:
                #
                lKeyWords = oFinderCRorLF.split( oCategory.cKeyWords )
                #
                sSayKeyWords = getTextSequence( lKeyWords, sAnd = 'or' )
                #
                lKeyWords = (   lKeyWords[0].split()
                                if len( lKeyWords ) == 1
                                else lKeyWords )
                #
                sPlural = 's' if len( lKeyWords ) > 1 else ''
                #
                _appendIfNotAlreadyIn(
                        lModels,
                        'excluded: %s cuz aint got key word%s %s' %
                        ( oCategory.cTitle, sPlural, sSayKeyWords ) )
                #
            #
            continue
            #
        #
        if bRecordSteps:
            #
            if sInTitle and sInTitle == oCategory.cTitle:
                #
                _appendIfNotAlreadyIn(
                        lCategories,
                        'category %s in title' % oCategory )
                #
            elif sInTitle:
                #
                _appendIfNotAlreadyIn(
                        lCategories,
                        'category %s ("%s") in title' %
                            ( oCategory, sInTitle ) )
                #
            elif bInHeirarchy1:
                #
                sInCategory1 = foundItem(
                                oItemFound.iCatHeirarchy.cCatHierarchy )[0]
                #
                _appendIfNotAlreadyIn( lCategories,
                    '%s in primary caregory %s' %
                    ( oCategory.cTitle, sInCategory1 ) )
                #
            elif bInHeirarchy2:
                #
                sInCategory2 = foundItem(
                                oItemFound.i2ndCatHeirarchy.cCatHierarchy )[0]
                #
                _appendIfNotAlreadyIn( lCategories,
                    '%s in secondary caregory %s' %
                    ( oCategory.cTitle, sInCategory2 ) )
                #
            #
        #
        sWhich = _whichGetsCredit(
                    sInTitle, bInHeirarchy1, bGotCategory )
        #
        lCategoryFound.append( oCategory )
        #
        dGotCategories[ oCategory.id ] = sInTitle
        #
        oHitsList.appendItem(
                iStarsCategory  = oCategory.iStars,
                iHitStars       = oCategory.iStars,
                oSearch         = oUserItem.iSearch,
                oCategory       = oCategory,
                cWhereCategory  = sWhich )
        #
        #
    #
    # cWhereCategory 'title' 'heirarchy1' or 'heirarchy2'
    #
    # if have category in title, discount other categories
    #
    def gotCategorInTitle( o ): return o.cWhereCategory == 'title'
    #
    oGotCategoryInTitle = get1stThatMeets(
                            oHitsList, gotCategorInTitle )
    #
    if oGotCategoryInTitle:
        #
        for o in oHitsList:
            #
            if o.cWhereCategory != 'title':
                #
                o.iStarsCategory    = o.iStarsCategory // 2 or 1
                o.iHitStars         = o.iHitStars      // 2 or 1
                #
            #
        #
    #
    return oHitsList




def _doStepThruModels(
            qsModels,
            dFindersModels,
            oHitsList,
            oUserItem,
            dCategoryInfo,
            dFamilyCategories,
            sAuctionTitleRelevantPart,
            sGotInParens,
            dFindSteps,
            bRecordSteps ):
    #
    lModels     = dFindSteps[ 'models' ]
    lCategories = dFindSteps[ 'categories' ]
    #
    dModelIDinTitle     = {} # the other way breaks findSearchHits()
    #
    dGotCategories  = oHitsList.dGotCategories
    oItemFound      = oHitsList.oItemFound
    #
    for oModel in qsModels:
        #
        foundItem = _getFoundItemTester(
                        oModel,
                        dFindersModels,
                        bAddDash = True,
                        bSubModelsOK = oModel.bSubModelsOK,
                        bExplainVerbose = False )
        #
        bFoundCategoryForModel = False
        #
        bExplainVerbose = ( bRecordSteps and
                            oModel.cTitle == '2A3 (RCA SP)' )
        #
        t = foundItem( sAuctionTitleRelevantPart, bExplainVerbose )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        uGotKeyWordsOrNoKeyWords = uGot
        #
        if not sInTitle:
            #
            continue
            #
        elif uExcludeThis:
            #
            if bRecordSteps:
                #
                _appendIfNotAlreadyIn(
                        lModels, 'excluded: %s cuz found %s' %
                        ( oModel.cTitle, uExcludeThis ) )
                #
            #
            continue
            #
        elif not uGotKeyWordsOrNoKeyWords:
            #
            if bRecordSteps:
                #
                lKeyWords = oFinderCRorLF.split( oModel.cKeyWords )
                #
                sSayKeyWords = getTextSequence( lKeyWords, sAnd = 'or' )
                #
                lKeyWords = (   lKeyWords[0].split()
                                if len( lKeyWords ) == 1
                                else lKeyWords )
                #
                sPlural = 's' if len( lKeyWords ) > 1 else ''
                #
                _appendIfNotAlreadyIn(
                        lModels,
                        'excluded: %s cuz aint got key word%s %s' %
                        ( oModel.cTitle, sPlural, sSayKeyWords ) )
                #
            #
            continue
            #
        #
        sModelAlphaNum  = _getAlphaNum( sInTitle )
        #
        iShorterByOK    = 1 if oModel.bSubModelsOK else 0 # None compatible
        #
        if bRecordSteps:
            #
            if (    uGotKeyWordsOrNoKeyWords and
                    type( uGotKeyWordsOrNoKeyWords ) is not bool ):
                #
                _appendIfNotAlreadyIn( lModels,
                        'for model "%s", "%s" is in title '
                        'and have key word(s) "%s"' %
                        (   oModel.cTitle,
                            sInTitle,
                            uGotKeyWordsOrNoKeyWords.group(0)) )
                #
            elif sInTitle == oModel.cTitle:
                #
                _appendIfNotAlreadyIn(
                        lModels, 'model %s (category %s) in title' %
                        ( sInTitle, oModel.iCategory ) )
                #
            else:
                #
                _appendIfNotAlreadyIn( lModels,
                        'for model "%s", "%s" is in title' %
                        ( oModel.cTitle, sInTitle ) )
                #
            #
            if oModel.cExcludeIf:
                #
                sSayExclude = getDashForReturn( oModel.cExcludeIf )
                _appendIfNotAlreadyIn( lModels,
                        'model "%s" excludes: %s (RegEx: %s)' %
                        ( oModel.cTitle,
                            sSayExclude,
                            oModel.cRegExExclude ) )
                #
                #
            #
        #
        iModelCateID = oModel.iCategory_id
        #
        bModelCategoryAlreadyFound = (
                iModelCateID in dGotCategories )
        #
        bCategoryFamilyRelation = False
        #
        tHitsList = tuple( oHitsList ) # copy of categories found list
        #
        #
        for oHitLine in tHitsList:
            #
            # like a crossover w drivers
            # or
            # a tube tester roll chart
            #
            iItemCateID = ( oHitLine.oCategory.id
                            if oHitLine.oCategory
                            else 0 )
            #
            bCategoryFamilyRelation = (
                oHitLine.oCategory and dCategoryInfo and
                iItemCateID != iModelCateID and
                iItemCateID in dCategoryInfo and
                (   (   dCategoryInfo[ iItemCateID ].iFamilyID ==
                        iModelCateID )
                    or
                    (   iModelCateID in dCategoryInfo and
                            dCategoryInfo[ iModelCateID ].iFamilyID ==
                            dCategoryInfo[ iItemCateID  ].iFamilyID ) ) )
            #
            bAddThisCategory = False
            #
            if  (   bCategoryFamilyRelation and
                    iModelCateID    in dGotCategories and
                    iItemCateID in dGotCategories ):
                #
                sModelCategory = dGotCategories[ iModelCateID ]
                iModelCategory = len( sModelCategory )
                #
                sThisCategory = dGotCategories[ iItemCateID ]
                iThisCategory = len( sThisCategory )
                #
                bAddThisCategory = (
                        sModelCategory and
                        iThisCategory > iModelCategory and
                        sModelCategory in sThisCategory )
                #
            #
            if bCategoryFamilyRelation and bAddThisCategory:
                #
                pass
                #
            elif (  bModelCategoryAlreadyFound and
                    oModel.iCategory != oHitLine.oCategory ):
                #
                continue
                #
            elif oModel.id in dModelIDinTitle:
                #
                continue
                #
            #
            if bModelCategoryAlreadyFound or bCategoryFamilyRelation:
                #
                if bModelCategoryAlreadyFound:
                    #
                    oCategory = oHitLine.oCategory
                    sWhereCategory = oHitLine.cWhereCategory
                    #
                else: # bCategoryFamilyRelation
                    #
                    if iModelCateID in dCategoryInfo:
                        #
                        iFamily = dCategoryInfo[ iModelCateID ].iFamilyID
                        #
                    else:
                        #
                        # dCategoryInfo[ iItemCateID ] ==
                        # iModelCateID )
                        #
                        logger.warning(
                                'model has category id %s in dCategoryInfo for %s' %
                                ( iModelCateID, oItemFound.iItemNumb ) )
                        #
                        iFamily = dCategoryInfo[ iItemCateID ].iFamilyID
                        #
                    #
                    # dFamilyCategories should work here
                    #
                    oFamily = Category.objects.get( id = iFamily )
                    #
                    sSayFamily = 'a member'
                    #
                    if oModel.iCategory == iFamily:
                        #
                        sSayFamily = 'the head'
                        #
                    #
                    # find targets for troubleshooting:
                    # is a member of family X
                    # is the head of family X
                    #
                    _appendIfNotAlreadyIn(
                            lCategories,
                            'category %s is %s of family %s' %
                                ( oModel.iCategory,
                                    sSayFamily,
                                    oFamily.cTitle ) )
                    #
                    oCategory = oModel.iCategory
                    #
                    sWhereCategory = 'family'
                    #
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                            lModels,
                            'adding model %s for category %s' %
                            ( oModel.cTitle, oCategory ) )
                #
                oItemOnList = oHitsList.appendItem(
                        iStarsCategory  = oHitLine.iStarsCategory,
                        iHitStars       = oHitLine.iHitStars,
                        oSearch         = oHitLine.oSearch,
                        oCategory       = oCategory,
                        cWhereCategory  = sWhereCategory,
                        oModel          = oModel,
                        iStarsModel     = oModel.iStars,
                        cFoundModel     = sInTitle,
                        bModelKeyWords  = bGotKeyWords,
                        cModelAlphaNum  = sModelAlphaNum,
                        cTitleLeftOver  = sWhatRemains )
                #
                iModelStars = oModel.iStars or 1
                #
                iHitStars = oHitLine.iStarsCategory * iModelStars
                #
                oItemOnList.iHitStars  = iHitStars
                #
                oItemOnList.iFoundModelLen = _getModelFoundLen(
                                                sInTitle, sGotInParens )
                #
                bFoundCategoryForModel  = True
                #
                updateModelIDinTitle(
                        dModelIDinTitle,
                        oModel,
                        sInTitle,
                        oCategory )
                #
            elif    ( oModel.iCategory == oHitLine.oCategory and
                    oHitLine.oModel is None ):
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                            lModels,
                            'item has category %s for model %s' %
                            ( oHitLine.oCategory, oModel.cTitle ) )
                    #
                #
                iModelStars = oModel.iStars or 1
                #
                iHitStars = oHitLine.iStarsCategory * iModelStars
                #
                oHitLine.oModel         = oModel
                oHitLine.iStarsModel    = oModel.iStars
                oHitLine.cFoundModel    = sInTitle
                oHitLine.bModelKeyWords = bGotKeyWords
                oHitLine.iFoundModelLen = _getModelFoundLen(
                                                sInTitle, sGotInParens )
                oHitLine.iHitStars      = iHitStars
                #
                bFoundCategoryForModel  = True
                #
                # not needed when using oHitsList
                updateModelIDinTitle(
                        dModelIDinTitle,
                        oModel,
                        sInTitle,
                        oCategory )
                #
                if bRecordSteps and oModel.cTitle == 'E88CC':
                    maybePrint()
                    maybePrint( 'E88CC iInTitleLocation:', iInTitleLocation )
                #
            #
        #
        if bCategoryFamilyRelation and not bFoundCategoryForModel:
            #
            if oModel.iCategory_id in dCategoryInfo:
                #
                iFamily = dCategoryInfo[ oModel.iCategory_id ].iFamilyID
                #
                if iFamily in dFamilyCategories:
                    #
                    oFamily = Category.objects.get( id = iFamily )
                    #
                    _appendIfNotAlreadyIn(
                            lCategories,
                            'category %s is the head of family %s' %
                                ( oModel.iCategory, oFamily.cTitle ) )
                    #
                #
            #
        #
        if not bFoundCategoryForModel:
            #
            if bRecordSteps:
                #
                _appendIfNotAlreadyIn(
                        lModels,
                        'item does not have category %s for model %s' %
                            ( oModel.iCategory, oModel.cTitle ) )
                #
                if oModel.iCategory.cLookFor:
                    #
                    lLookFor = oFinderCRorLF.split( oModel.iCategory.cLookFor )
                    #
                    sayLookFor = ' | '.join( lLookFor )
                    #
                    _appendIfNotAlreadyIn(
                            lModels,
                            'category look for: %s' % sayLookFor )
                    #
                #
                _appendIfNotAlreadyIn(
                        lModels,
                        'category RegEx: %s' % oModel.iCategory.cRegExLook4Title )
            #
            oItemOnList = oHitsList.appendItem(
                    iHitStars       = oModel.iStars,
                    iStarsModel     = oModel.iStars,
                    cFoundModel     = sInTitle,
                    cModelAlphaNum  = sModelAlphaNum,
                    iFoundModelLen  = len( sModelAlphaNum ),
                    oSearch         = oUserItem.iSearch,
                    oModel          = oModel )
            #
        #
    #
    oHitsList.dModelIDinTitle = dModelIDinTitle
    #



def _doStepThruBrands(
            oHitsList,
            oUser,
            qsBrands,
            dFindSteps,
            dFindersBrands,
            sAuctionTitleRelevantPart,
            oUserItem,
            bRecordSteps ):
    #
    lBrands = dFindSteps[ 'brands' ]
    lModels = dFindSteps[ 'models' ]
    #
    bGotBrandForNonGenericModel = False
    #
    lCategoryFound  = oHitsList.lCategoryFound
    oItemFound      = oHitsList.oItemFound
    #
    dGotBrandIDsInTitle = {}
    #
    for oBrand in qsBrands:
        #
        foundItem = _getFoundItemTester(
                        oBrand, dFindersBrands, bAddDash = True )
        #
        bFoundBrandForModel = False
        #
        t = foundItem( sAuctionTitleRelevantPart )
        #
        sInTitle, uGot, bGotKeyWords, uExcludeThis, sWhatRemains = t
        #
        uGotKeyWordsOrNoKeyWords = uGot
        #
        #
        if not sInTitle:
            #
            continue
            #
        elif uExcludeThis:
            #
            if bRecordSteps:
                #
                _appendIfNotAlreadyIn(
                        lBrands, 'excluded: %s cuz found %s' %
                        ( oBrand.cTitle, uExcludeThis ) )
                #
            #
            continue
            #
        elif not uGotKeyWordsOrNoKeyWords:
            #
            if bRecordSteps:
                #
                lKeyWords = oFinderCRorLF.split( oBrand.cKeyWords )
                #
                sSayKeyWords = getTextSequence( lKeyWords, sAnd = 'or' )
                #
                lKeyWords = (   lKeyWords[0].split()
                                if len( lKeyWords ) == 1
                                else lKeyWords )
                #
                sPlural = 's' if len( lKeyWords ) > 1 else ''
                #
                _appendIfNotAlreadyIn(
                        lModels,
                        'excluded: %s cuz aint got key word%s %s' %
                        ( oBrand.cTitle, sPlural, sSayKeyWords ) )
                #
            #
            continue
            #
        #
        setModelsBrands = set( [] ) # local to _doStepThruBrands()
        #
        dGotBrandIDsInTitle[ oBrand.id ] = sInTitle
        #
        if bRecordSteps:
            #
            if sInTitle == oBrand.cTitle:
                #
                _appendIfNotAlreadyIn(
                        lBrands, 'brand %s in title' % sInTitle )
                #
            else:
                #
                _appendIfNotAlreadyIn( lBrands,
                        'for brand "%s", "%s" is in title' %
                        ( oBrand.cTitle, sInTitle ) )
                #
            #
        #
        for oHitLine in oHitsList: # categories found list shallow copy
            #
            tModelBrand = ( oHitLine.oModel, oBrand )
            #
            oHitLineModel = None
            #
            if oHitLine.oModel:
                oHitLineModel = Model.objects.get(
                                        id = oHitLine.oModel.id )
            #
            if   (      oHitLine.oModel                and
                    not oHitLine.oModel.bGenericModel  and
                    oHitLineModel                 and
                    oHitLineModel.iBrand == oHitLine.oBrand ):
                #
                bFoundBrandForModel = True
                #
            elif (  oHitLine.oModel                and
                    oHitLine.oBrand                and
                    oHitLine.oModel.bGenericModel  and
                    oHitLine.oCategory             and
                    tModelBrand not in setModelsBrands ):
                #

                bSaveBrand = BrandCategory.objects.filter(
                    iUser     = oUser,
                    iBrand    = oBrand,
                    iCategory = oHitLine.oCategory ).exists()
                #
                if bRecordSteps:
                    #
                    maybePrint()
                    maybePrint( 'bSaveBrand:', bSaveBrand )
                    #
                    _appendIfNotAlreadyIn( lBrands,
                            'found another brand %s for generic model %s' %
                            ( oBrand.cTitle, oHitLine.oModel.cTitle ) )
                    #
                #
                oNewItem = oHitsList.appendCopy( oHitLine )
                #
                oNewItem.oBrand      = None
                oNewItem.iStarsBrand = 0
                oNewItem.iHitStars   = 0
                #
                continue
                #
            elif (      oHitLine.oModel and
                    (   oHitLine.oBrand is None or
                        oHitLine.oBrand != oBrand ) ):
                #
                bSaveBrand = False
                #
                if oBrand == oHitLine.oModel.iBrand:
                    #
                    oHitLine.oBrand = oBrand
                    #
                    bSaveBrand = True
                    #
                    if bRecordSteps:
                        #
                        _appendIfNotAlreadyIn( lBrands,
                                'found brand %s for model %s' %
                                ( oBrand.cTitle, oHitLine.oModel.cTitle ) )
                        #
                    #
                    bGotBrandForNonGenericModel = True
                    #
                    bFoundBrandForModel = True
                    #
                elif    (   oHitLineModel                  and
                            oHitLineModel.iBrand == oBrand and
                            oHitLine.oBrand != oBrand ):
                    #
                    oHitLine.oBrand = oBrand
                    #
                    bSaveBrand = True
                    #
                    bFoundBrandForModel = True
                    #
                elif oHitLine.oModel.bGenericModel and oHitLine.oCategory:
                    #
                    bSaveBrand = BrandCategory.objects.filter(
                        iUser     = oUser,
                        iBrand    = oBrand,
                        iCategory = oHitLine.oCategory ).exists()
                    #
                #
                if bSaveBrand and tModelBrand not in setModelsBrands:
                    #
                    if (    bRecordSteps and
                            oHitLine.oModel.bGenericModel and
                            not bGotBrandForNonGenericModel ):
                        #
                        _appendIfNotAlreadyIn( lBrands,
                                'found brand %s for generic model %s' %
                                ( oBrand.cTitle, oHitLine.oModel.cTitle ) )
                        #
                    #
                    oHitLine.iStarsBrand  = oBrand.iStars
                    oHitLine.oBrand       = oBrand
                    #
                    iStarsCategory  = oHitLine.iStarsCategory  or 1
                    iStarsModel     = oHitLine.iStarsModel     or 1
                    #
                    iHitStars = (   iStarsCategory *
                                    iStarsModel *
                                    oBrand.iStars )
                    #
                    oHitLine.iHitStars    = iHitStars
                    #
                    bFoundBrandForModel = True
                    #
                    setModelsBrands.add( tModelBrand )
                    #
                #
            #
        #
        bSaveBrand = False
        #
        for oCategory in lCategoryFound:
            #
            bSaveBrand = BrandCategory.objects.filter(
                iUser     = oUser,
                iBrand    = oBrand,
                iCategory = oCategory ).exists()
            #
            if bSaveBrand: break
            #
        #
        iBrandStars = oBrand.iStars or 1
        #
        if bSaveBrand and not bFoundBrandForModel:
            #
            if bRecordSteps:
                #
                _appendIfNotAlreadyIn( lBrands,
                        'brand %s has products in category %s' %
                        ( oBrand.cTitle, oCategory.cTitle ) )
                #
            #
            oHitLine.iStarsBrand  = oBrand.iStars
            oHitLine.oBrand       = oBrand
            #
            iStarsCategory          = oCategory.iStars or 1
            #
            iHitStars = iStarsCategory * oBrand.iStars
            #
            oHitLine.iHitStars    = iHitStars
            #
            oHitsList.appendItem(
                    oBrand          = oBrand,
                    oCategory       = oCategory,
                    iStarsBrand     = iBrandStars,
                    iStarsCategory  = iStarsCategory,
                    iHitStars       = iHitStars,
                    oSearch         = oUserItem.iSearch )
            #
        elif not bFoundBrandForModel:
            #
            if bRecordSteps:
                #
                _appendIfNotAlreadyIn( lBrands,
                        'did not find brand %s for any model found' %
                        oBrand.cTitle )
                #
            #
            oHitsList.appendItem(
                    oBrand          = oBrand,
                    iStarsBrand     = oBrand.iStars,
                    iHitStars       = iBrandStars,
                    oSearch         = oUserItem.iSearch )
            #
        #
    #
    oHitsList.dGotBrandIDsInTitle         = dGotBrandIDsInTitle
    oHitsList.bGotBrandForNonGenericModel = bGotBrandForNonGenericModel
    #





def _getModelLocations(
            oHitsList,
            sAuctionTitleRelevantPart,
            bRecordSteps ):
    #
    oModelLocated       = None
    #
    dModelIDinTitle     = oHitsList.dModelIDinTitle
    dGotBrandIDsInTitle = oHitsList.dGotBrandIDsInTitle
    #
    #
    if len( dModelIDinTitle ) > 1:
        #
        # toss obvious non candidates
        #
        iterModelIDsBrandID = (
                ( k, v.oBrand.id )
                for k, v in dModelIDinTitle.items()
                if v.oBrand )
        #
        lDeleteThese = []
        #
        for t in iterModelIDsBrandID:
            #
            if t[1] not in dGotBrandIDsInTitle:
                #
                lDeleteThese.append( t[0] )
                #
            #
        #
        if lDeleteThese and len( lDeleteThese ) < len( dModelIDinTitle ):
            #
            for iModelID in lDeleteThese:
                #
                if bRecordSteps:
                    #
                    maybePrint( 'not a strong candidate:',
                                dModelIDinTitle[ iModelID ].sInTitle )
                    #
                #
                del dModelIDinTitle[ iModelID ]
                #
            #
        #
    #
    if len( dModelIDinTitle ) > 1:
        #
        oModelLocated = _getModelLocationsBegAndEnd(
                sAuctionTitleRelevantPart, dModelIDinTitle )
        #
        # tNearFront, tOnEnd, tNearEnd, tInParens,
        # dAllWordLocations, tTitleWords
        #
    #
    if bRecordSteps:
        maybePrint()
        maybePrint( 'dModelIDinTitle:' )
        maybePrettyP( dModelIDinTitle )
        if oModelLocated is None:
            maybePrint( 'oModelLocated is None' )
        else:
            o = oModelLocated
            maybePrint(
                    'oModelLocated '
                    'tNearFront, tOnEnd, tNearEnd, tInParens:',
                o.tNearFront, o.tOnEnd, o.tNearEnd, o.tInParens )
            maybePrint( 'tWordsOfInterest:', o.tWordsOfInterest )
            maybePrint( 'dAllWordLocations:' )
            maybePrettyP( o.dAllWordLocations )
    #
    oHitsList.oModelLocated = oModelLocated
    #


def _isCompleteHit( o ):
    #
    return o.oModel and o.oBrand and o.oCategory




def _doScoreCandidates(
            oHitsList,
            oUserItem,
            dSearchMyCategory,
            dCategoryInfo,
            dFindSteps,
            dSearchLogs,
            setComponents,
            oUser,
            bRecordSteps ):
    #
    tNow                        = timezone.now()
    #
    lCandidates                 = dFindSteps[ 'candidates' ]
    lSelect                     = dFindSteps[ 'selection' ]
    #
    # dModelID_oHitLine          = {}
    dModelID_oHitsItem          = {}
    #
    oItemFound                  = oHitsList.oItemFound
    dModelIDinTitle             = oHitsList.dModelIDinTitle
    dGotBrandIDsInTitle         = oHitsList.dGotBrandIDsInTitle
    #
    bGotBrandForNonGenericModel = oHitsList.bGotBrandForNonGenericModel
    #
    oModelLocated               = oHitsList.oModelLocated
    #
    def isComponent( iCategory ): return iCategory in setComponents
    #
    if len( oHitsList ) == 0:
        #
        if bRecordSteps:
            #
            _appendIfNotAlreadyIn(
                lSelect,
                'did not find anything for this item' )
            #
        #
        oUserItem.tLook4Hits = tNow
        #
        oUserItem.save()
        #
        return # save one level of indent
    #
    #
    if len( oHitsList ) > 1:
        #
        if bRecordSteps:
            #
            lCandidates.append(
                    'scoring (total, hit stars, found length): '
                    '%s candidates'
                    % len( oHitsList ) )
            #
        #
    #
    #if oItemFound.iItemNumb == 192659380750:
        #print( '\n\noModelLocated:', bool( oModelLocated ) )
    if oModelLocated: # some on the end of the auctin title
        #
        # tNearFront, tOnEnd, tNearEnd, tInParens,
        # dAllWordLocations, tTitleWords
        #
        dModelID_oHitsItem = dict(
                ( ( oHitLine.oModel.id, oHitLine )
                    for oHitLine in oHitsList
                    if oHitLine.oModel is not None ) )
        #
        #if oItemFound.iItemNumb == 192659380750:
            #print( 'item 192659380750 -- same?\n' )
            #print( 'dModelID_oTempItem - original:')
            #pprint( dModelID_oTempItem )

            #dModelID_oObjItem = dict(
                #( ( oTempItem.iModel.id, oTempItem )
                    #for oTempItem in oHitsList
                    #if oTempItem.iModel is not None ) )
            #print( 'dModelID_oTempItem - object:')
            #pprint( dModelID_oObjItem )
            #print()
        #
        # dAllWordLocations = { 'Jbl'       : ( 0, ),
        #                       'L65'       : ( 1, ),
        #                       'Jubal'     : ( 2, ),
        #                       'Le5-12'    : ( 3, ),
        #                       'Mids'      : ( 4, ),
        #                       'Pair'      : ( 5, ),
        #                       'Working'   : ( 6, ),
        #                       'Nice'      : ( 7, ),
        #                       'See'       : ( 8, ),
        #                       'Pictures'  : ( 9, ) }
        #
        dWordLocations = oModelLocated.dAllWordLocations
        #
        dLocationsModelIDs = {}
        #
        for iModelID, o in dModelIDinTitle.items():
            #
            sInTitle = o.sInTitle
            #
            tLocation = dWordLocations.get( sInTitle )
            #
            if tLocation is not None:
                #
                for i in tLocation:
                    #
                    lModels = dLocationsModelIDs.setdefault(
                                    i, [] ).append( iModelID )
                    #
                #
            #
        #
        setCategoriesBeg    = _getCategoriesForPositions(
                oModelLocated.tNearFront,
                dLocationsModelIDs,
                dModelID_oHitsItem )
        #
        setCategoriesOnEnd  = _getCategoriesForPositions(
                oModelLocated.tOnEnd,
                dLocationsModelIDs,
                dModelID_oHitsItem )
        #
        setCategoriesNearEnd  = _getCategoriesForPositions(
                oModelLocated.tNearEnd,
                dLocationsModelIDs,
                dModelID_oHitsItem )
        #
        if bRecordSteps:
            #
            maybePrint()
            maybePrint( 'setCategoriesBeg:', setCategoriesBeg )
            maybePrint( 'setCategoriesOnEnd:', setCategoriesOnEnd )
            maybePrint( 'setCategoriesNearEnd:', setCategoriesNearEnd )
            # maybePrint( 'len( lItemFoundTemp ) before:', len( lItemFoundTemp ) )
            # maybePrint( 'dModelID_oTempItem:' )
            # maybePrettyP( dModelID_oTempItem )
            # for k, o in dModelID_oTempItem.items():
            #     maybePrint( ' %s: %s, %s' % ( k, o.iModel, o.iCategory ) )
            maybePrint( 'dLocationsModelIDs:' )
            maybePrettyP( dLocationsModelIDs )
            # maybePrint( 'lItemFoundTemp (iModel, iBrand, iCategory):')
            # maybePrettyP( lItemFoundTemp )
            #for o in lItemFoundTemp:
                #if o.iCategory is None:
                    #maybePrint( '  %s - %s - %s (id %s)' % ( o.iModel, o.iBrand, o.iCategory, 'None' ) )
                #else:
                    #maybePrint( '  %s - %s - %s (id %s)' % ( o.iModel, o.iBrand, o.iCategory, o.iCategory.id ) )
            maybePrint( 'oModelLocated:' )
            for s in vars( oModelLocated ):
                if s.startswith( '_' ): continue
                maybePrint( '  %s: %s' % ( s, oModelLocated.__dict__[s] ) )
            #
            maybePrint( 'dGotBrandIDsInTitle:' )
            maybePrettyP( dGotBrandIDsInTitle )
            maybePrint( 'bGotBrandForNonGenericModel:', bGotBrandForNonGenericModel )
            #
        #
        if dGotBrandIDsInTitle and bGotBrandForNonGenericModel:
            #
            for iModelID, oHitLine in dModelID_oHitsItem.items():
                #
                if  (   oHitLine.oBrand is None or
                        oHitLine.oBrand.id not in dGotBrandIDsInTitle ):
                    #
                    oHitLine.bIncludeThis = False
                    #
                    # oTempItem = dModelID_oTempItem[ iModelID ]
                    #
                    # oTempItem.bIncludeThis = False
                    #
                    if bRecordSteps:
                        #
                        lCandidates.append(
                            'do not have brand for model %s, '
                            'so excluding' % oHitLine.iModel )
                        #
                    #
                #
            #
            oNewHitsObj = oHitsList.getCopyWithoutItems()
            #
            lIncludeHitItems = [ o for o in oHitsList if o.bIncludeThis ]
            #
            oNewHitsObj.appendObjects( *lIncludeHitItems )
            #
            oHitsList = oNewHitsObj # overwrite
            #
        #
        if bRecordSteps:
            #
            maybePrint( 'oHitsList:' )
            for o in oHitsList:
                maybePrint( '  %s - %s - %s' %
                            ( o.oModel, o.oBrand, o.oCategory ) )
            #
        if setCategoriesBeg or oModelLocated.tInParens:
            #
            setFamiliesBeg = frozenset(
                    ( dCategoryInfo[ id ].iFamilyID
                        for id in setCategoriesBeg
                        if id in dCategoryInfo ) )
            #
            setFamiliesOnEnd = frozenset(
                    ( dCategoryInfo[ id ].iFamilyID
                        for id in setCategoriesOnEnd
                        if id in dCategoryInfo ) )
            #
            setExcludeTempModels = set( [] )
            setExcludeHitsModels = set( [] )
            #
            # oHitsList = HitsListClass()
            #
            o = oModelLocated
            #
            if (    o.tNearEnd  and
                    o.tOnEnd    and
                    len( o.tNearEnd ) > len( o.tOnEnd ) and
                    o.tNearEnd.endswith( o.tOnEnd ) ):
                #
                setFamiliesNearEnd = frozenset(
                        ( dCategoryInfo[ id ].iFamilyID
                            for id in setCategoriesNearEnd
                            if id in dCategoryInfo ) )
                #
                tTests = (
                    ( o.tNearEnd, 'near end of',
                        setCategoriesNearEnd, setFamiliesNearEnd ),
                    ( o.tInParens,'within parens in',
                        None, None ) )
                #
            else:
                #
                tTests = (
                    ( o.tOnEnd,   'on end of',
                        setCategoriesOnEnd, setFamiliesOnEnd ),
                    ( o.tInParens,'within parens in',
                        None, None ),
                    ( o.tNearEnd, 'near end of',
                        setCategoriesNearEnd, None ) )
                #
            #
            if bRecordSteps:
                #
                maybePrint( 'setFamiliesBeg    :', setFamiliesBeg    )
                maybePrint( 'setFamiliesOnEnd  :', setFamiliesOnEnd  )
                maybePrint( 'test in this order:',
                            ', '.join( [ t[1] for t in tTests ] ) )
                #
            #
            setAllCategories = (
                    setCategoriesBeg |
                    setCategoriesNearEnd |
                    setCategoriesOnEnd )
            #
            bAllComponents = allMeet(
                    setAllCategories, isComponent )
            #
            # enhance here --
            # if "with" word is between front and on / near end
            #
            for tLocations, sSay, setTest, setFamily in tTests:
                #
                # o = oModelLocated
                # o.tNearFront, o.tOnEnd, o.tNearEnd, o.tInParens
                #
                if bRecordSteps:
                    #
                    maybePrint( 'step for', sSay, 'tLocations:', tLocations )
                    #
                #
                if not tLocations: continue
                #
                if setTest is not None:
                    #
                    if False and setCategoriesBeg == setTest:
                        #
                        # want to process if all are vacuum tubes!
                        #
                        continue # categories same
                        #
                    elif bAllComponents:
                        #
                        continue
                        #
                    elif (  setFamiliesBeg is not None and
                            setFamily      is not None and
                            len( setFamiliesBeg ) == 1 and
                            setFamiliesBeg == setFamily ):
                        #
                        sNext2Last = o.tTitleWords[
                                            max( o.tOnEnd ) - 1 ]
                        #
                        if bRecordSteps:
                            #
                            maybePrint( 'category IDs:  ',
                                    setCategoriesBeg | setCategoriesNearEnd )
                            maybePrint( 'bAllComponents:', bAllComponents )
                            #
                        #
                        if   (  o.tNearEnd and
                                o.tNearEnd.endswith( o.tOnEnd ) and
                                sNext2Last.lower() in
                                    ( '&', 'and', ',' ) ):
                            #
                            # proper listing,
                            # not just model # tacked on end
                            #
                            continue
                            #
                        #
                    #
                #
                if bRecordSteps:
                    #
                    maybePrint( sSay, 'tLocations:', tLocations )
                    maybePrint( 'o.dAndWords:', o.dAndWords )
                    #
                #
                dModelIDsLocations = getReverseDictCarefully( dLocationsModelIDs )
                #
                iMaxAtFront = max( o.tNearFront )
                uAndWords   = o.dAndWords.values()
                #
                if not o.dAndWords:
                    iLastAnd = 0
                elif isinstance( uAndWords, int ):
                    iLastAnd = uAndWords
                else:
                    iLastAnd = max(
                            chain.from_iterable(o.dAndWords.values() ) )
                #
                if bRecordSteps:
                    #
                    print( 'iLastAnd:', iLastAnd )
                    #
                #
                for iLocation in tLocations:
                    #
                    if iLocation in dLocationsModelIDs:
                        #
                        for iModelID in dLocationsModelIDs[ iLocation ]:
                            #
                            lLocations = dModelIDsLocations[ iModelID ]
                            #
                            iMinOnEnd  = min( lLocations )
                            #
                            if (    len( lLocations ) > 1 and
                                    iMinOnEnd in o.tNearFront ):
                                #
                                continue
                                #
                            elif (  o.dAndWords and
                                    iLastAnd >=
                                        iMaxAtFront +
                                        ( ( iMinOnEnd - iMaxAtFront )
                                            / 2 ) ):
                                #
                                continue
                                #
                            #
                            # oTempItem = dModelID_oTempItem[ iModelID ]
                            #
                            # setExcludeTempModels.add( oTempItem.cModelAlphaNum )
                            #
                            # oTempItem.bIncludeThis = False
                            #
                            oHitLine = dModelID_oHitsItem[ iModelID ]
                            #
                            oHitLine.bIncludeThis = False
                            #
                            setExcludeHitsModels.add(
                                dModelID_oHitsItem[iModelID].cModelAlphaNum )
                            #
                            if bRecordSteps:
                                #
                                sModel = dModelID_oHitsItem[ iModelID ].oModel
                                #
                                lCandidates.append(
                                    'model %s %s auction title, '
                                    'so excluding' % ( sModel, sSay ) )
                                #
                        #
                    else:
                        #
                        if bRecordSteps:
                            #
                            logger.info(
                                'weak hit: model location %s '
                                'not in dLocationsModelIDs for %s' %
                                ( iLocation, oItemFound.iItemNumb ) )
                            #
                        #
                    #
                #
            #
            for o in oHitsList:
                #
                if o.cModelAlphaNum in setExcludeHitsModels:
                    #
                    o.bIncludeThis = False
                    #
                #
            #
        #
        if bRecordSteps:
            #
            maybePrint( 'len( oHitsList ) after:', len( oHitsList ) )
            #
    #
    bGotCompleteHit = get1stThatMeets( oHitsList, _isCompleteHit )
    #
    if bGotCompleteHit:
        #
        for o in oHitsList:
            #
            if not _isCompleteHit( o ):
                #
                o.bIncludeThis = False
                #
            #
        #
    #
    lIncludeHitItems = [ o for o in oHitsList if o.bIncludeThis ]
    #
    oNewHitsObj = oHitsList.getCopyWithoutItems()
    #
    lHitListNotExcluded = [ o for o in oHitsList if o.bIncludeThis ]
    #                       if o.cModelAlphaNum not in setExcludeHitsModels ]
    #
    oNewHitsObj.appendObjects( *lHitListNotExcluded )
    #
    oHitsList = oNewHitsObj
    #
    if len( oHitsList ) > 1:
        #
        t = _getFoundModelBooster( oHitsList, bRecordSteps )
        #
        nFoundModelBoost, iMaxLen, lExactMatch = t
        #
        if bRecordSteps and lExactMatch:
            #
            sSayExactMatch = getTextSequence(
                                ( o.cFoundModel for o in lExactMatch ) )
            #
            lCandidates.append(
                    'have exact match%s: %s'
                    % ( Plural( len( lExactMatch ), 'es' ),
                        sSayExactMatch ) )
            #
        elif bRecordSteps and nFoundModelBoost > 1:
            #
            lCandidates.append(
                    'giving the longest title a boost: %s'
                    % nFoundModelBoost )
            #
        #
        # ### oHitsList ###
        #
        lSortItems = []
        #
        for i in range( len( oHitsList ) ): # need the index after sort!
            #
            oHitLine = oHitsList[ i ]
            #
            iFoundModelMultiplier = oHitLine.iFoundModelLen or 1
            #
            if oHitLine.iFoundModelLen == iMaxLen:
                #
                iScoreStars = round( (
                    iFoundModelMultiplier * oHitLine.iHitStars
                    ) * nFoundModelBoost )
                #
            else:
                #
                iScoreStars = int( (
                    iFoundModelMultiplier * oHitLine.iHitStars
                    ) / nFoundModelBoost )
                #
            #
            if  (       oHitLine.oModel is not None and
                        oHitLine.oBrand is None and
                        oHitLine.oModel.iBrand is not None ):
                #
                if bRecordSteps:
                    #
                    lCandidates.append(
                        'did not find brand for %s, so discounting'
                        % oHitLine.oModel )
                    #
                #
                iScoreStars = iScoreStars / 2
                #
            #
            lSortItems.append( ( iScoreStars, i ) )
            #
            if bRecordSteps:
                #
                lCandidates.append(
                    '%s, %s, %s - %s : %s : %s' %
                    ( iScoreStars,
                        oHitLine.iHitStars,
                        oHitLine.iFoundModelLen,
                        _getTitleOrNone( oHitLine.oCategory ),
                        _getTitleOrNone( oHitLine.oModel ),
                        _getTitleOrNone( oHitLine.oBrand ) ) )
                #
            #
        #
        lSortItems.sort()
        #
        lSortItems.reverse()
        #
        iTopScoreStars = iTopHitStars = oTopStars = None
        sTitle = sTopTitle = None
        #
        bSortAgain = False
        #
        for i in range( len( oHitsList ) ):
            #
            oHitLine = oHitsList[ lSortItems[i][1] ]
            #
            sTitle = None
            #
            if oHitLine.oModel:
                sTitle          = getWhatsNotInParens(
                                    oHitLine.oModel.cTitle ).upper()
                if oHitLine.oModel.bSubModelsOK:
                    sTitle      = sTitle[ : -1 ]
            #
            if (    settings.COVERAGE and
                    bRecordSteps and
                    ( iTopScoreStars is None or ( sTopTitle and sTitle) ) ):
                #
                maybePrint()
                maybePrint( 'i:', i )
                maybePrint( 'iScoreStars:', lSortItems[i][0] )
                maybePrint( 'oHitLine.iHitStars:', oHitLine.iHitStars )
                maybePrint( 'sTopTitle:', sTopTitle)
                maybePrint( 'sTitle:', sTitle)
                #
            #
            if iTopScoreStars is None:
                #
                iTopScoreStars  = lSortItems[i][0]
                iTopHitStars    = oHitLine.iHitStars
                oTopStars       = oHitLine
                sTopTitle       = sTitle
                #
                continue
            #
            if (    oHitLine.iHitStars >= iTopHitStars and
                    sTopTitle                           and
                    sTitle                              and
                    len( sTitle ) < len( sTopTitle )    and
                    sTitle in sTopTitle ):
                #
                # discount this
                #
                oHitLine.iHitStars = (
                        oHitLine.iHitStars *
                        iTopHitStars /
                        iTopScoreStars )
                #
                bSortAgain = True
                #
                if bRecordSteps:
                    #
                    lCandidates.append(
                            'discounting Hit Stars for %s' %
                                oHitLine.oModel )
                    #
                #
            #
        #
        if bSortAgain:
            #
            lSortItems.sort()
            #
            lSortItems.reverse()
            #
        #
        # sort oHitsList, more stars on top, fewer stars on bottom
        #
        lItemHitsSort = [ oHitsList[ t[1] ] for t in lSortItems ]
        #
        oNewHitsObj = oHitsList.getCopyWithoutItems()
        #
        oNewHitsObj.appendObjects( *lItemHitsSort )
        #
        oHitsList = oNewHitsObj
        #
        # oHitsList.testSameSame( lItemFoundSort )
        #
        # end ### oHitsList ###
        #
        if bRecordSteps:
            #
            _appendIfNotAlreadyIn(
                    lSelect,
                    'on top:   %s : %s : %s' %
                    (   _getTitleOrNone( oHitsList[0].oCategory ),
                        _getTitleOrNone( oHitsList[0].oModel ),
                        _getTitleOrNone( oHitsList[0].oBrand )) )
            #
            #maybePrint()
            #maybePrint( 'len( lItemFoundSort ):', len( lItemFoundSort ) )
            #
        #
    else:
        #
        if bRecordSteps:
            #
            _appendIfNotAlreadyIn(
                    lSelect,
                    'only found one thing for this item, a no brainer!' )
            #
        #
    #
    #
    # items found are in lItemFoundSort & oHitsList
    #
    #
    if bRecordSteps and len( oHitsList ) > 0:
        #
        print( 'oHitsList:' )
        pprint( oHitsList )
        #
        print()
        print( 'dSearchMyCategory:' )
        pprint( dSearchMyCategory )

    #
    iItemsFoundTemp         = -1
    #
    dModelsStoredAlready    = {} # used for scoring & selection
    #
    lModelsStoredAlready    = []
    #
    setBrandStoredIDs       = set( [] )
    setBrandStoredNames     = set( [] )
    #
    for oHitLine in oHitsList:
        #
        iItemsFoundTemp += 1
        #
        sModelTitleLessParens = sModelTitleUPPER = ''
        #
        if oHitLine.oModel:
            #
            # sModelTitleLessParens = getWhatsNotInParens(
            #         oHitLine.oModel.cTitle )
            #
            sModelTitleLessParens = oHitLine.cFoundModel
            #
            # sModelTitleUPPER = sModelTitleLessParens.upper()
            #
            # sModelTitleUPPER = oHitLine.cModelAlphaNum
            sModelTitleUPPER = oHitLine.cFoundModel.upper()
        #
        if ( settings.COVERAGE or True ) and bRecordSteps:
            #
            maybePrint()
            maybePrint( 'temp item index :', iItemsFoundTemp )
            maybePrint( 'model           :', oHitLine.oModel )
            maybePrint( 'brand           :', oHitLine.oBrand )
            maybePrint( 'category        :', oHitLine.oCategory )
            maybePrint( 'sModelTitleUPPER:', sModelTitleUPPER )
            maybePrint( 'iHitStars       :', oHitLine.iHitStars )
            maybePrint( 'bModelKeyWords  :', oHitLine.bModelKeyWords )
            maybePrint()
            #
        #
        if iItemsFoundTemp == 0: # store item on top here
            #
            oUserItem.iBrand        = oHitLine.oBrand
            oUserItem.iModel        = oHitLine.oModel
            #
            if oHitLine.oBrand:
                #
                setBrandStoredIDs.add(   oHitLine.oBrand.id )
                #
            #
            if oHitLine.oBrand:
                #
                setBrandStoredNames.add(
                    dGotBrandIDsInTitle[ oHitLine.oBrand.id ] )
                #
            #
            oMyCategory = dSearchMyCategory.get( oHitLine.oSearch.id )
            #
            if oMyCategory:
                #
                oUserItem.iCategory = oMyCategory
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                            lSelect,
                            'search that found this expects category '
                            '"%s", so changing now' % oMyCategory )
                    #
            else:
                #
                oUserItem.iCategory = oHitLine.oCategory
                #
            #
            oUserItem.iHitStars     = oHitLine.iHitStars
            oUserItem.cWhereCategory= oHitLine.cWhereCategory
            # oUserItem.iSearch     = oHitLine.oSearch
            #
            oUserItem.tLook4Hits = tNow
            #
            oUserItem.save()
            #
            if oHitLine.oModel:
                #
                lModelsStoredAlready.append( sModelTitleUPPER )
                #
                _updateModelsStoredAlready(
                        dModelsStoredAlready, oHitLine, sModelTitleUPPER )
                #
            #
            # testing problem work around 2019-12-18
            #
            if oHitLine.oSearch.id in dSearchLogs:
                #
                oSearchLog = dSearchLogs.get( oHitLine.oSearch.id )
                #
            else:
                #
                try:
                    oSearchLog = SearchLog.objects.get( iSearch = oHitLine.iSearch )
                except:
                    #
                    if settings.TESTING:
                        #
                        oSearchLog = SearchLog(
                                        iSearch_id  = oHitLine.oSearch.id,
                                        tBegSearch  = tNow,
                                        cResult     = 'Success' )
                        #
                    else:
                        #
                        raise
                        #
                    #
                #
                oSearchLog.iOrigHits = oSearchLog.iItemHits
                oSearchLog.iItemHits = 0
                #
                dSearchLogs[ oHitLine.oSearch.id ] = oSearchLog
                #
            #
            if (    oHitLine.oBrand and
                    oHitLine.oCategory and
                    oHitLine.oModel ):
                #
                oSearchLog.iItemHits += 1
                #
            #
        elif (  oHitLine.oBrand and
                oHitLine.oCategory and
                oHitLine.oModel ):
            #
            # have complete hit, make an additional UserItem record
            #
            t = _gotFullStringOrSubStringOfListItem(
                        sModelTitleUPPER,
                        lModelsStoredAlready )
            #
            uExact, uLonger, uShort = t
            #
            bGotNonGenericForThis       = False
            sBetterBrandForThisGeneric  = None
            bGotKeyWordsModelForThis    = False
            #
            # dModelsStoredAlready used for scoring & selection
            #
            if sModelTitleUPPER in dModelsStoredAlready:
                #
                if bRecordSteps:
                    maybePrint()
                    maybePrint( 'sModelTitleUPPER in dModelsStoredAlready:', sModelTitleUPPER in dModelsStoredAlready )
                #
                for oModelStored in dModelsStoredAlready[ sModelTitleUPPER ]:
                    #
                    # startswith below handles Amperex Bugle Boy & Amperex
                    #
                    bGotNonGenericForThis = bGotNonGenericForThis or (
                            oModelStored.iModelBrand and
                            not oModelStored.bGenericModel )
                            #oHitLine.oBrand and
                            #oModelStored.iModelBrand.cTitle.startswith(
                                    #oHitLine.oBrand.cTitle ) and
                    #
                    # if bGotNonGenericForThis: continue
                    #
                    bGotKeyWordsModelForThis   = (
                            bGotKeyWordsModelForThis or
                            oModelStored.bModelKeyWords )
                    #
                    if  (   oModelStored.iModelBrand is None and
                            oModelStored.iBrand and
                            oHitLine.oBrand    and
                            oModelStored.iBrand.cTitle.startswith(
                                    oHitLine.oBrand.cTitle  ) ):
                        #
                        sBetterBrandForThisGeneric = oModelStored.iBrand.cTitle
                        #
                    #
                    if bRecordSteps:
                        #
                        maybePrint()
                        maybePrint( 'oModelStored:' )
                        maybePrint( oModelStored )
                        maybePrint( 'oModelStored.iModelBrand:', oModelStored.iModelBrand )
                        maybePrint( 'oHitLine.oBrand:', oHitLine.oBrand )
                        if oModelStored.iModelBrand:
                            maybePrint( 'oModelStored.iModelBrand.cTitle:', oModelStored.iModelBrand.cTitle )
                        else:
                            maybePrint( 'oModelStored.iModelBrand:', oModelStored.iModelBrand )
                        maybePrint( 'oHitLine.oBrand.cTitle:', oHitLine.oBrand.cTitle )
                        maybePrint( 'oModelStored.bGenericModel:', oModelStored.bGenericModel )
                        maybePrint( 'bGotNonGenericForThis:', bGotNonGenericForThis )
                        maybePrint( 'sBetterBrandForThisGeneric:', sBetterBrandForThisGeneric )
                        maybePrint( 'bGotKeyWordsModelForThis:', bGotKeyWordsModelForThis )
                        maybePrint( 'lModelsStoredAlready:', lModelsStoredAlready )
                        maybePrint( 'sModelTitleLessParens:', sModelTitleLessParens )
                        #
                    #
                    if sBetterBrandForThisGeneric or bGotKeyWordsModelForThis:
                        #
                        continue
                        #
                    #
                #
            #
            bGotBrand = False
            #
            if (    oHitLine.oModel.iBrand is not None and
                    oHitLine.oModel.iBrand != oHitLine.oBrand ):
                #
                continue
                #
            elif uShort and uShort in dModelsStoredAlready:
                #
                for oModelStored in dModelsStoredAlready[ uShort ]:
                    #
                    bGotBrand = ( oModelStored.iModelBrand == oHitLine.oBrand )
                    #
                    if bGotBrand: continue
                    #
                #
            #
            doPrintMore = (
                    True and
                    bRecordSteps and
                    sModelTitleUPPER == '6V6' )
            #
            if doPrintMore: #  and not bGotNonGenericForThis
                #
                maybePrint()
                maybePrint( 'sModelTitleUPPER:', sModelTitleUPPER )
                maybePrint( 'oHitLine.oModel:', oHitLine.oModel )
                maybePrint( 'oHitLine.oBrand:', oHitLine.oBrand )
                maybePrint( 'oHitLine.oCategory:', oHitLine.oCategory )
                maybePrint( 'dModelsStoredAlready:' )
                CustomPPrint.pprint( dModelsStoredAlready )
                maybePrint( 'oHitLine.oModel.bGenericModel:', oHitLine.oModel.bGenericModel )
                maybePrint( 'uExact:', uExact )
                maybePrint( 'setBrandStoredNames:', setBrandStoredNames )
                maybePrint( 'setBrandStoredIDs:', setBrandStoredIDs )
                #
            #
            # exclude if uLonger unless
            # both longer string and shorter substring
            # are BOTH in title
            # carry on / continue here
            #
            bGotLongGotShort = False
            oModelStored     = None
            #
            # '''
            if settings.COVERAGE and bRecordSteps:
                #
                maybePrint()
                maybePrint('uExact, uLonger, uShort:', t )
                maybePrint('dModelsStoredAlready:')
                for k, l in dModelsStoredAlready.items():
                    maybePrint( '%s:' % k )
                    i = -1
                    for o in l:
                        i += 1
                        if len( l ) > 1:
                            maybePrint( '%s:' % i )
                        else:
                            maybePrint( 'only one hit:' )
                        maybePrint( o )
                #
            # '''
            #
            if uExact and uExact in dModelsStoredAlready:
                #
                oModelStored = dModelsStoredAlready[ uExact ][0]
                #
            #
            if uLonger and uLonger in dModelsStoredAlready:
                #
                sWithout = dModelsStoredAlready[
                            uLonger ][0].sTitleLeftOver or ''
                ##
                #t = foundItem( sAuctionTitleRelevantPart )
                ##
                #sInTitle, uGotKeyWords, uExcludeThis, sWhatRemains = t
                ##
                #lParts = sAuctionTitleRelevantPart.split( sInTitle )
                ##
                #sWithout = ' '.join( lParts )
                ##
                #sWithout = oHitLine.cTitleLeftOver or ''
                #
                bGotLongGotShort = (
                        sModelTitleLessParens in sWithout )
                #
            #
            bShorterNearEnd = False
            #
            if uLonger and bGotLongGotShort and oModelLocated:
                #
                o = oModelLocated
                #
                tLocations = o.dAllWordLocations.get(
                                sModelTitleLessParens, () )
                #
                if (    tLocations and
                        ( o.tNearEnd or
                            o.tOnEnd ) ):
                    #
                    lNearEnd = list( o.tNearEnd )
                    lNearEnd.extend( o.tOnEnd )
                    #
                    bShorterNearEnd = (
                        not containsAny( tLocations, o.tNearFront ) and
                            containsAll( tLocations, lNearEnd ) )
                #
            #
            if uLonger and bGotLongGotShort and bShorterNearEnd:
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'excluding %s '
                            'because it is tacked on the end' %
                            sModelTitleLessParens )
                    #
                #
                continue
                #
            elif (  uLonger and
                    bGotLongGotShort and
                    sModelTitleUPPER not in lModelsStoredAlready ):
                #
                if bRecordSteps:
                    #
                    #maybePrint()
                    #maybePrint( 'sWithout:', sWithout )
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'keeping %s because this and '
                            '%s both are in the title' %
                            ( sModelTitleLessParens, uLonger ) )
                    #
                #
            elif uLonger:
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'excluding %s '
                            'because this is a substring of %s' %
                            ( sModelTitleLessParens, uLonger ) )
                    #
                #
                continue
                #
            elif uShort and bGotBrand:
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'excluding %s '
                            'because its root is %s' %
                            ( sModelTitleLessParens, uShort ) )
                    #
                #
                continue
                #
            elif     (  uExact and
                        oHitLine.oModel.bGenericModel and
                        bGotNonGenericForThis and
                        oHitLine.oBrand is not None and
                        oHitLine.oBrand.id in setBrandStoredIDs and
                        bGotKeyWordsModelForThis ):
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'excluding generic %s for %s -- '
                            'already have model with key words' %
                            ( sModelTitleLessParens, oHitLine.oBrand ) )
                    #
                #
                continue
                #
            elif    (   uExact and
                        oHitLine.oModel.bGenericModel and
                        oHitLine.oBrand is not None and
                        oHitLine.oBrand.id in setBrandStoredIDs and
                        bGotNonGenericForThis ):
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'excluding generic model %s -- '
                            'already have a non generic' %
                            ( sModelTitleLessParens ) )
                    #
                #
                continue
                #
            elif    (   uExact and
                        oHitLine.oModel.bGenericModel and
                        sBetterBrandForThisGeneric ):
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'excluding generic %s for %s -- '
                            'already have a generic for %s' %
                            ( sModelTitleLessParens,
                                oHitLine.oBrand,
                                sBetterBrandForThisGeneric ) )
                    #
                #
                continue
                #
            elif (      uExact and
                        oModelStored and
                        oModelStored.iCategoryID and
                        oHitLine.oCategory and
                        oModelStored.iCategoryID != oHitLine.oCategory.id ):
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'have model %s already, but including '
                            'it again for a different category' %
                            ( sModelTitleLessParens ) )
                    #
                #
            elif (  uExact and
                    oHitLine.oBrand is not None and
                    oHitLine.oBrand.id in setBrandStoredIDs and
                    sModelTitleUPPER in lModelsStoredAlready ):
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'excluding %s for %s -- '
                            'already have' %
                            ( sModelTitleLessParens, oHitLine.oBrand ) )
                    #
                #
                continue
                #
            elif (  uExact and
                    oHitLine.oBrand.id in dGotBrandIDsInTitle and
                    dGotBrandIDsInTitle[ oHitLine.oBrand.id ] in
                        setBrandStoredNames ):
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'excluding %s for %s -- '
                            'already have a %s for %s' %
                            ( sModelTitleLessParens, oHitLine.oBrand,
                                sModelTitleLessParens, oHitLine.oBrand ) )
                    #
                #
                continue
                #

            elif uExact and oHitLine.oModel.bGenericModel:
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'have model %s already, '
                            'but including again for %s' %
                            ( sModelTitleLessParens, oHitLine.oBrand ) )
                    #
                #
            elif uExact:
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                            'excluding %s '
                            'because we already got %s' %
                            ( sModelTitleLessParens, uExact ) )
                    #
                #
                continue
                #
            #
            tNow = timezone.now()
            #
            if UserItemFound.objects.filter(
                    iItemNumb       = oUserItem.iItemNumb,
                    iUser           = oUser,
                    iModel          = oHitLine.oModel,
                    iBrand          = oHitLine.oBrand,
                    iCategory       = oHitLine.oCategory ).exists():
                #
                # hitting error in testing in django 2.2,
                # was never a problem in 1.11
                #
                pass
                #
            else:
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                        lSelect,
                        'also storing: %s : %s : %s' %
                            (   _getTitleOrNone( oHitLine.oCategory ),
                                _getTitleOrNone( oHitLine.oModel ),
                                _getTitleOrNone( oHitLine.oBrand )) )
                    #
                #
                oNewUserItem = UserItemFound(
                    iItemNumb       = oUserItem.iItemNumb,
                    iHitStars       = oHitLine.iHitStars,
                    iSearch         = oHitLine.oSearch,
                    iModel          = oHitLine.oModel,
                    iBrand          = oHitLine.oBrand,
                    iCategory       = oHitLine.oCategory,
                    cWhereCategory  = oHitLine.cWhereCategory,
                    tLook4Hits      = tNow,
                    tCreate         = tNow,
                    tModify         = tNow,
                    iUser           = oUser )
                #
                if oHitLine.oBrand:
                    #
                    setBrandStoredIDs.add(   oHitLine.oBrand.id )
                    #
                #
                if oHitLine.oBrand:
                    #
                    setBrandStoredNames.add(
                        dGotBrandIDsInTitle[ oHitLine.oBrand.id ] )
                    #
                #
                oNewUserItem.save()
                #
                # dModelsStoredAlready used for scoring & selection
                #
                _updateModelsStoredAlready(
                        dModelsStoredAlready, oHitLine, sModelTitleUPPER )
                #
                lModelsStoredAlready.append( sModelTitleUPPER )
                #
            #
        #
    #
    #
    # this is after
    # for oHitLine in lItemFoundSort:
    #
    #
    # before going on, update userFinder, dModelsStoredAlready has the info
    #
    #
    iMaxStars, iMaxModel = _getMaxHitStars( dModelsStoredAlready )
    #
    if settings.COVERAGE and bRecordSteps:
        #
        maybePrint('')
        maybePrint('iMaxStars:', iMaxStars )
        #
    if iMaxStars:
        #
        oUserFinder = UserFinder(
                iItemNumb       = oItemFound,
                iHitStars       = iMaxStars,
                iMaxModel       = iMaxModel,
                cTitle          = oItemFound.cTitle,
                cMarket         = oItemFound.cMarket,
                cListingType    = oItemFound.cListingType,
                tTimeEnd        = oItemFound.tTimeEnd,
                iUser           = oUser )
            #
        #
        oUserFinder.save()
        #
    #
    #
    if bRecordSteps:
        #
        _printHitSearchSteps( oItemFound, dFindSteps )
        #
    #



def _getUserItems( oItemFound, oUser ):
    #
    qsUserItems = UserItemFound.objects.filter(
            iItemNumb   = oItemFound.iItemNumb,
            iUser       = oUser )
    #
    oUserItem = None
    #
    lDeleteThese = []
    #
    for oNext in qsUserItems:
        #
        if oUserItem is None:
            oUserItem = oNext
        else:
            lDeleteThese.append( oNext )
    #
    for oThis in lDeleteThese:
        oThis.delete()
    #
    oUserItem.iStarsBrand = oUserItem.iStarsCategory = 0
    oUserItem.iStarsModel = oUserItem.iHitStars      = 0
    #
    return qsUserItems, oUserItem




def _getRecordSteps(
            oItemFound,
            setScriptTested,
            lScriptTested,
            dFindSteps,
            oUser,
            dCategoryInfo,
            dFamilyCategories,
            sAuctionTitleRelevantPart,
            iRecordStepsForThis ):
    #
    bRecordSteps = False
    #
    if settings.COVERAGE:
        #
        bRecordSteps        = True
        iRecordStepsForThis = oItemFound.iItemNumb
        #
    elif (       oItemFound.iItemNumb == iRecordStepsForThis and
            str( iRecordStepsForThis ) not in setScriptTested ):
        #
        lScriptTested.append( str( iRecordStepsForThis ) )
        #
        QuickDumpLines( lScriptTested, SCRIPT_TEST_FILE )
        #
        setScriptTested.add( str( iRecordStepsForThis ) )
        #
        bRecordSteps = True
        #
    #
    if bRecordSteps:
        #
        # need a blank for every heading
        #
        dFindSteps = OrderedDict(
            (   ( 'preliminary',[] ),
                ( 'categories', [] ),
                ( 'models',     [] ),
                ( 'brands',     [] ),
                ( 'candidates', [] ),
                ( 'selection',  [] ) ) )
        #
        qsUserSearches = Search.objects.filter( iUser = oUser )
        #
        maybePrint()
        maybePrint( 'Searches (id, iMyCategory, name):' )
        #
        for oSearch in qsUserSearches:
            #
            maybePrint( oSearch.id, oSearch.iMyCategory, oSearch )
            #
        #
        #
        maybePrint( 'dFamilyCategories:' )
        maybePrettyP( dFamilyCategories )
        #
        maybePrint( 'dCategoryInfo:' )
        maybePrettyP(dCategoryInfo )
        #
        if len( oItemFound.cTitle ) > len( sAuctionTitleRelevantPart ):
            #
            lPreliminary = dFindSteps[ 'preliminary' ]
            #
            _appendIfNotAlreadyIn(
                    lPreliminary,
                    'will consider only: %s' % sAuctionTitleRelevantPart )
            #
            sLoppedOff = oItemFound.cTitle[ len( sAuctionTitleRelevantPart ) : ]
            #
            _appendIfNotAlreadyIn(
                    lPreliminary, '(will ignore: %s)' % sLoppedOff )
            #
        #
    #
    return bRecordSteps, iRecordStepsForThis



def _getCategoryInfo( oUser ):
    #
    dCategoryInfo       = {}
    dFamilyCategories   = {} # ### not populated !!! try fixing ! ###
    setComponents       = set( [] )
    #
    dSearchMyCategory   = _getSearchMyCategoryDict( oUser )
    #
    qsCategories = Category.objects.filter( iUser = oUser )
    #
    for oCategory in qsCategories:
        #
        if oCategory.iFamily_id:
            #
            iFamilyID   = oCategory.iFamily_id
            bComponent  = oCategory.bComponent
            #
            # category oCategory.id is a member of family iFamilyID
            #
            dCategoryInfo[ oCategory.id ] = ValueContainer(
                    iFamilyID   = iFamilyID,
                    bComponent  = bComponent,
                    sCategTitle = oCategory.cTitle )
            #
        #
        if oCategory.bComponent:
            #
            setComponents.add( oCategory.id )
            #
        #
    #
    setComponents = frozenset( setComponents )
    #
    return (    qsCategories,
                dCategoryInfo,
                dFamilyCategories,
                dSearchMyCategory,
                setComponents )




def findSearchHits(
            iUser                   = oUserOne.id,
            iRecordStepsForThis     = None ):
    #
    oUserModel = get_user_model()
    #
    oUser = oUserModel.objects.get( id = iUser )
    #
    # generate a list of the most recent SearchLogs for this user
    #
    qsSearchLogs = ( SearchLog.objects.filter(
                        iSearch_id__in =
                            Search.objects.filter( iUser = oUser )
                            .values_list( 'id', flat=True ),
                        tBegStore__in =
                            SearchLog.objects.values( "iSearch_id" )
                            .annotate(
                                tBegStore = Max( "tBegStore" )
                                ).values_list( "tBegStore", flat = True ) ) )
    #
    for oSearchLog in qsSearchLogs:
        #
        oSearchLog.iOrigHits = oSearchLog.iItemHits
        oSearchLog.iItemHits = 0
        #
    #
    dSearchLogs = { o.iSearch_id: o for o in qsSearchLogs }
    #
    qsItemsFound = ItemFound.objects.filter(
                pk__in = UserItemFound.objects
                    .filter( iUser = oUser,
                             tLook4Hits__isnull = True )
                    .values_list( 'iItemNumb', flat=True ) )
    #
    if len( qsItemsFound ) == 0: return
    #
    dFindersBrands      = {}
    dFindersCategories  = {}
    dFindersModels      = {}
    #
    t = _getCategoryInfo( oUser )
    #
    (   qsCategories,
        dCategoryInfo,
        dFamilyCategories,
        dSearchMyCategory,
        setComponents ) = t
    #
    qsModels = ( Model.objects
                    .select_related('iBrand')
                    .filter( iUser = oUser ) )
    #
    qsBrands = Brand.objects.filter( iUser = oUser )
    #
    dFindSteps = dict(
        (   ( 'preliminary',[] ),
            ( 'categories', [] ),
            ( 'models',     [] ),
            ( 'brands',     [] ),
            ( 'candidates', [] ),
            ( 'selection',  [] ) ) )
    #
    lScriptTested = [] # in this session, test an item ONLY ONCE
    #
    if isFileThere( SCRIPT_TEST_FILE ):
        #
        lScriptTested = [ s for s in
                          getListFromFileLines( SCRIPT_TEST_FILE )
                          if s ]
        #
    #
    setScriptTested = set( lScriptTested )
    #
    # step thru the items one by one
    #
    for oItemFound in qsItemsFound:
        #
        qsUserItems, oUserItem = _getUserItems( oItemFound, oUser )
        #
        # if title includes for or fits, consider the part in front,
        # not what follows
        #
        t = _getRelevantTitle( oItemFound.cTitle )
        #
        sAuctionTitleRelevantPart, sGotInParens = t
        #
        #
        #
        # troubleshooting code if applicable
        #
        #
        t = _getRecordSteps(
                oItemFound,
                setScriptTested,
                lScriptTested,
                dFindSteps,
                oUser,
                dCategoryInfo,
                dFamilyCategories,
                sAuctionTitleRelevantPart,
                iRecordStepsForThis )
        #
        bRecordSteps, iRecordStepsForThis = t
        #
        #
        #
        #
        # step thru categories
        #
        #
        oHitsList = _doStepThruCategories(
                oItemFound,
                oUserItem,
                qsCategories,
                dFindersCategories,
                sAuctionTitleRelevantPart,
                dFindSteps,
                bRecordSteps )
        #
        #
        #
        #
        #
        # step thru models
        #
        #
        _doStepThruModels(
                qsModels,
                dFindersModels,
                oHitsList,
                oUserItem,
                dCategoryInfo,
                dFamilyCategories,
                sAuctionTitleRelevantPart,
                sGotInParens,
                dFindSteps,
                bRecordSteps )
        #
        #
        #
        #
        #
        #
        # step thru brands
        #
        #
        _doStepThruBrands(
                oHitsList,
                oUser,
                qsBrands,
                dFindSteps,
                dFindersBrands,
                sAuctionTitleRelevantPart,
                oUserItem,
                bRecordSteps )
        #
        #
        #
        #
        #
        # determine model locations for candidates
        #
        #
        _getModelLocations(
                oHitsList,
                sAuctionTitleRelevantPart,
                bRecordSteps )
        #
        #
        #
        # score candidates
        #
        #
        _doScoreCandidates(
                oHitsList,
                oUserItem,
                dSearchMyCategory,
                dCategoryInfo,
                dFindSteps,
                dSearchLogs,
                setComponents,
                oUser,
                bRecordSteps )
    #
    for oSearchLog in dSearchLogs.values():
        #
        if not oSearchLog.iOrigHits:
            #
            oSearchLog.save()
        #
    #
