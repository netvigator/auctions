import logging

from copy                   import copy
from pprint                 import pprint, pformat

from collections            import OrderedDict

from django.conf            import settings
from django.db.models       import Q, Max
from django.contrib.auth    import get_user_model
from django.utils           import timezone

from core.user_one          import oUserOne
from core.utils             import ( maybePrint, maybePrettyP,
                                     getWhatsNotInParens )

from core.templatetags.core_tags import getDashForReturn

from .models                import Search, SearchLog

from categories.models      import BrandCategory

from finders.models         import ( ItemFound, UserItemFound, ItemFoundTemp,
                                     UserFinder )

from models.models          import Model

from searching              import ( WORD_BOUNDARY_MAX, SCRIPT_TEST_FILE,
                                     DROP_AFTER_THIS )

from pyPks.Collect.Get      import LongerList
from pyPks.Collect.Output   import getTextSequence
from pyPks.Collect.Query    import get1stThatMeets, get1stThatFails

from pyPks.Dict.Get         import getReverseDict

from pyPks.File.Get         import getListFromFileLines
from pyPks.File.Test        import isFileThere
from pyPks.File.Write       import QuickDumpLines

from pyPks.Object.Get       import ValueContainer
from pyPks.Object.Output    import CustomPPrint

from pyPks.String.Count     import getAlphaNumCount as getLen
from pyPks.String.Dumpster  import getAlphaNumCleanNoSpaces
from pyPks.String.Eat       import eatPunctuationBegAndEnd
from pyPks.String.Get       import getTextBeforeC
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


def _getRelevantTitle( sTitle ):
    #
    return _oDropAfterThisFinder.split( sTitle )[0]



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



def _getRegExSearchOrNone( s ):
    #
    if s:
        #
        oRegExObj = getRegExObj( s )
        #
        return oRegExObj.search


_oParensSearcher = _getRegExSearchOrNone( r'(?<=\().*(?=\))' )


def _getAlphaNum( s ): return getAlphaNumCleanNoSpaces( s ).upper()


def getInParens( s ):
    #
    oMatch = _oParensSearcher( s )
    #
    uReturn = None
    #
    if oMatch:
        #
        uReturn = oMatch.group(0)
        #
    #
    return uReturn



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


def getFoundItemTester( oTableRow, dFinders,
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
                        bExplainVerbose = bExplainVerbose )
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
        def foundItemTester( s, bExplainVerbose = False ):
            #
            sFoundInTitle = ''
            #
            oTitleMatch = searchTitle( s )
            #
            if oTitleMatch: sFoundInTitle = oTitleMatch.group(0)
            #
            uExcludeThis = _includeOrExclude( s, searchExclude )
            #
            uGotKeyWordsOrNoKeyWords = _gotKeyWordsOrNoKeyWords( s, searchKeyWords )
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
            if settings.COVERAGE and bExplainVerbose: #
                maybePrint('')
                maybePrint('sFoundInTitle           :', sFoundInTitle )
                maybePrint('findTitle               :', findTitle )
                maybePrint('findTitle.pattern       :', findTitle.pattern )
                maybePrint('oTableRow.cLookFor      :', oTableRow.cLookFor )
                maybePrint('oTableRow.cExcludeIf    :', oTableRow.cExcludeIf )
                maybePrint('oTableRow.cKeyWords     :', oTableRow.cKeyWords )
                maybePrint('uGotKeyWordsOrNoKeyWords:', uGotKeyWordsOrNoKeyWords )
                maybePrint('sWhatRemains            :', sWhatRemains )
                #
            #
            return (    sFoundInTitle,
                        uGotKeyWordsOrNoKeyWords,
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


def _printHitSearchSteps( oItem, dFindSteps ):
    #
    maybePrint('')
    maybePrint('Item %s Hit Search Steps:' % oItem.iItemNumb )
    maybePrint( oItem.cTitle )
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

def getTitleOrNone( o ):
    #
    sTitle = 'None'
    #
    if hasattr( o, 'cTitle' ):
        #
        sTitle = o.cTitle
        #
    #
    return sTitle


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
            dModelsStoredAlready, oTempItem, sModelTitleUPPER ):
    #
    # dModelsStoredAlready used for scoring & selection
    #
    iCategoryID = None
    #
    if oTempItem.iCategory:
        iCategoryID = oTempItem.iCategory.id
    #
    oThisModel = ValueContainer(
        bGenericModel   = oTempItem.iModel.bGenericModel,
        iModelBrand     = oTempItem.iModel.iBrand,
        iBrand          = oTempItem.iBrand,
        bSubModelsOK    = oTempItem.iModel.bSubModelsOK,
        iModelID        = oTempItem.iModel.id,
        iHitStars       = oTempItem.iHitStars,
        sTitleLeftOver  = oTempItem.cTitleLeftOver,
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



def _getFoundModelBooster( lItemFoundTemp, bRecordSteps ):
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
    for o in lItemFoundTemp:
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
            ( o.cModelAlphaNum for o in lItemFoundTemp ), 0 )
    #
    for i in range( len( lItemFoundTemp ) ):
        #
        o = lItemFoundTemp[ i ]
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
        maybePrint( 'lAllFoundIns (iLen, i [lItemFoundTemp], cModelAlphaNum, iHitStars):' )
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
            oLongr = lItemFoundTemp[ lAllFoundIns[ iOut ][ 1 ] ]
            oShort = lItemFoundTemp[ lAllFoundIns[ iIn  ][ 1 ] ]
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
            tPositions, dLocationsModelIDs, dModelID_oTempItem ):
    #
    lCategories = []
    #
    for iPosition in tPositions:
        #
        if iPosition in dLocationsModelIDs:
            #
            for iModelID in dLocationsModelIDs[ iPosition ]:
                #
                iCategory = dModelID_oTempItem[ iModelID ].iCategory
                #
                if iCategory is not None:
                    #
                    lCategories.append( iCategory )
                    #
                #
            #
        #
    #
    return frozenset( lCategories )



def _getModelLocationsBegAndEnd( sAuctionTitle, tWordsOfInterest ):
    #
    oLocated = getStrLocationsBegAndEnd( sAuctionTitle, tWordsOfInterest )
    #
    # tNearFront, tOnEnd, tNearEnd & tInParens
    #
    if (    oLocated.tNearFront and
            (   oLocated.tOnEnd   or
                oLocated.tNearEnd or
                oLocated.tInParens ) ):
        #
        pass
        #
    else:
        #
        oLocated = None
        #
    #
    return oLocated




def findSearchHits(
            iUser                   = oUserOne.id,
            bCleanUpAfterYourself   = True,
            iRecordStepsForThis     = None ):
    #
    from brands.models      import Brand
    from categories.models  import Category
    from models.models      import Model
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
    ItemFoundTemp.objects.all().delete()
    #
    qsItems = ItemFound.objects.filter(
                pk__in = UserItemFound.objects
                    .filter( iUser = oUser,
                             tLook4Hits__isnull = True )
                    .values_list( 'iItemNumb', flat=True ) )
    #
    if len( qsItems ) == 0: return
    #
    dFindersBrands      = {}
    dFindersCategories  = {}
    dFindersModels      = {}
    #
    dCategoryFamily     = {}
    dFamilyCategory     = {}
    #
    bExcludeThis        = False
    #
    qsCategories = Category.objects.filter( iUser = oUser )
    #
    for oCategory in qsCategories:
        #
        if oCategory.iFamily_id:
            #
            iFamily_id = oCategory.iFamily_id
            #
            # category oCategory.id is a member of family iFamily_id
            #
            dCategoryFamily[ oCategory.id ] = iFamily_id
            #
        #
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
    lScriptTested = []
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
    for oItem in qsItems:
        #
        qsUserItems = UserItemFound.objects.filter(
                iItemNumb   = oItem.iItemNumb,
                iUser       = oUser )
        #
        oUserItem = None
        #
        lDeleteThese = []
        #
        bRecordSteps = False
        #
        if settings.COVERAGE:
            #
            bRecordSteps        = True
            iRecordStepsForThis = oItem.iItemNumb
            #
        elif (       oItem.iItemNumb == iRecordStepsForThis and
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
        bGotCategory   = False
        dGotCategories = {}
        #
        oTempItem = None
        lItemFoundTemp = []
        #
        oItemFound = ItemFound.objects.get( pk = oItem.iItemNumb )
        #
        # if title includes for or fits, consider the part in front,
        # not what follows
        #
        sAuctionTitleRelevantPart = _getRelevantTitle( oItem.cTitle )
        #
        if bRecordSteps and (
                len( oItem.cTitle ) > len( sAuctionTitleRelevantPart ) ):
            #
            lPreliminary = dFindSteps[ 'preliminary' ]
            #
            _appendIfNotAlreadyIn(
                    lPreliminary,
                    'will consider only: %s' % sAuctionTitleRelevantPart )
            #
            sLoppedOff = oItem.cTitle[ len( sAuctionTitleRelevantPart ) : ]
            #
            _appendIfNotAlreadyIn(
                    lPreliminary, '(will ignore: %s)' % sLoppedOff )
            #
        #
        sGotInParens = getInParens( sAuctionTitleRelevantPart )
        #
        lCategories = dFindSteps[ 'categories' ]
        #
        lCategoryFound = []
        #
        #
        #
        #
        #
        # first: step thru categories
        #
        #
        #
        #
        for oCategory in qsCategories:
            #
            foundItem = getFoundItemTester(
                            oCategory,
                            dFindersCategories,
                            bPluralize = True )
            #
            # the following are short circuiting --
            # if one is True, the following will be True
            # and the string will not be searched
            # so don't take bInHeirarchy1 & bInHeirarchy2 literally!
            #
            t = foundItem( sAuctionTitleRelevantPart )
            #
            sInTitle, uGotKeyWordsOrNoKeyWords, uExcludeThis, sWhatRemains = t
            #
            #
            bInHeirarchy1  = ( # will be True if sInTitle is True
                    sInTitle or
                    ( oItem.iCatHeirarchy and # can be None
                        foundItem(
                            oItem.iCatHeirarchy.cCatHierarchy )[0] ) )
            #
            bInHeirarchy2  = ( # will be True if either are True
                    sInTitle or
                    bInHeirarchy1 or
                    ( oItem.i2ndCatHeirarchy and
                        foundItem(
                            oItem.i2ndCatHeirarchy.cCatHierarchy )[0] ) )
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
                                    oItem.iCatHeirarchy.cCatHierarchy )[0]
                    #
                    _appendIfNotAlreadyIn( lCategories,
                        '%s in primary caregory %s' %
                        ( oCategory.cTitle, sInCategory1 ) )
                    #
                elif bInHeirarchy2:
                    #
                    sInCategory2 = foundItem(
                                    oItem.i2ndCatHeirarchy.cCatHierarchy )[0]
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
            oTempItem = ItemFoundTemp(
                    iItemNumb       = oItemFound,
                    iStarsCategory  = oCategory.iStars,
                    iHitStars       = oCategory.iStars,
                    iSearch         = oUserItem.iSearch,
                    iCategory       = oCategory,
                    cWhereCategory  = sWhich )
            #
            oTempItem.save()
            #
            lItemFoundTemp.append( oTempItem )
            #
            lCategoryFound.append( oCategory )
            #
            dGotCategories[ oCategory.id ] = sInTitle
            #
        #
        # cWhereCategory 'title' 'heirarchy1' or 'heirarchy2'
        #
        # if have category in title, discount other categories
        #
        def gotCategorInTitle( o ): return o.cWhereCategory == 'title'
        #
        oGotCategoryInTitle = get1stThatMeets(
                                lItemFoundTemp, gotCategorInTitle )
        #
        if oGotCategoryInTitle:
            #
            for o in lItemFoundTemp:
                #
                if o.cWhereCategory != 'title':
                    #
                    o.iStarsCategory    = o.iStarsCategory // 2 or 1
                    o.iHitStars         = o.iHitStars      // 2 or 1
                    #
        #
        # finished stepping thru categories
        #
        #
        # next: step thru models
        #
        #
        #
        lModels = dFindSteps[ 'models' ]
        #
        dModelIDinTitle = {}
        oModelLocated   = None
        #
        # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
        #
        for oModel in qsModels:
            #
            foundItem = getFoundItemTester(
                            oModel,
                            dFindersModels,
                            bAddDash = True,
                            bSubModelsOK = oModel.bSubModelsOK,
                            bExplainVerbose = False )
            #
            bFoundCategoryForModel = False
            #
            bExplainVerbose = ( bRecordSteps and
                                oModel.cTitle == '6DJ8 (Bugle Boy)' )
            #
            t = foundItem( sAuctionTitleRelevantPart, bExplainVerbose )
            #
            sInTitle, uGotKeyWordsOrNoKeyWords, uExcludeThis, sWhatRemains = t
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
            # sGotInParens = getInParens( sAuctionTitleRelevantPart )
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
            lNewItemFoundTemp = []
            #
            bModelCategoryAlreadyFound = (
                    oModel.iCategory_id in dGotCategories )
            #
            bCategoryFamilyRelation = False
            #
            for oTempItem in lItemFoundTemp: # lists categories found
                #
                # like a crossover w drivers
                # or
                # a tube tester roll chart
                #
                bCategoryFamilyRelation = (
                    oTempItem.iCategory and dCategoryFamily and
                    oTempItem.iCategory.id != oModel.iCategory_id and
                    oTempItem.iCategory.id in dCategoryFamily and
                    (   (   dCategoryFamily[ oTempItem.iCategory.id ] ==
                            oModel.iCategory_id )
                        or
                        (   oModel.iCategory_id in dCategoryFamily and
                                dCategoryFamily[ oModel.iCategory_id ] ==
                                dCategoryFamily[ oTempItem.iCategory.id ] ) ) )
                #
                bAddThisCategory = False
                #
                if  (   bCategoryFamilyRelation and
                        oModel.iCategory_id    in dGotCategories and
                        oTempItem.iCategory.id in dGotCategories ):
                    #
                    sModelCategory = dGotCategories[ oModel.iCategory_id ]
                    iModelCategory = len( sModelCategory )
                    #
                    sThisCategory = dGotCategories[ oTempItem.iCategory.id ]
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
                        oModel.iCategory != oTempItem.iCategory ):
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
                        oCategory = oTempItem.iCategory
                        sWhereCategory = oTempItem.cWhereCategory
                        #
                    else: # bCategoryFamilyRelation
                        #
                        if oModel.iCategory_id in dCategoryFamily:
                            #
                            iFamily = dCategoryFamily[ oModel.iCategory_id ]
                            #
                        else:
                            #
                            # dCategoryFamily[ oTempItem.iCategory.id ] ==
                            # oModel.iCategory_id )
                            #
                            logger.warning(
                                    'model has category id %s in dCategoryFamily for %s' %
                                    ( oModel.iCategory_id, oItem.iItemNumb ) )
                            #
                            iFamily = dCategoryFamily[ oTempItem.iCategory.id ]
                            #
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
                    oNewTempItem = ItemFoundTemp(
                            iItemNumb       = oTempItem.iItemNumb,
                            iStarsCategory  = oTempItem.iStarsCategory,
                            iHitStars       = oTempItem.iHitStars,
                            iSearch         = oTempItem.iSearch,
                            iCategory       = oCategory,
                            cWhereCategory  = sWhereCategory,
                            iModel          = oModel,
                            iStarsModel     = oModel.iStars,
                            cFoundModel     = sInTitle,
                            cModelAlphaNum  = sModelAlphaNum,
                            cTitleLeftOver  = sWhatRemains )
                    #
                    iModelStars = oModel.iStars or 1
                    #
                    iHitStars = oTempItem.iStarsCategory * iModelStars
                    #
                    oNewTempItem.iHitStars  = iHitStars
                    #
                    oNewTempItem.iFoundModelLen = _getModelFoundLen(
                                                    sInTitle, sGotInParens )
                    #
                    oNewTempItem.save()
                    #
                    bFoundCategoryForModel  = True
                    #
                    lNewItemFoundTemp.append( oNewTempItem )
                    #
                    if oModel.id not in dModelIDinTitle:
                        #
                        dModelIDinTitle[ oModel.id ] = sInTitle
                        #
                    #
                elif    ( oModel.iCategory == oTempItem.iCategory and
                        oTempItem.iModel is None ):
                    #
                    if bRecordSteps:
                        #
                        _appendIfNotAlreadyIn(
                                lModels,
                                'item has category %s for model %s' %
                                ( oTempItem.iCategory, oModel.cTitle ) )
                        #
                    #
                    oTempItem.iModel            = oModel
                    #
                    oTempItem.iStarsModel       = oModel.iStars
                    #
                    # reduce the length boost if the match is in parens
                    #
                    oTempItem.iFoundModelLen = _getModelFoundLen(
                                                    sInTitle, sGotInParens )
                    #
                    iModelStars = oModel.iStars or 1
                    #
                    iHitStars = oTempItem.iStarsCategory * iModelStars
                    #
                    oTempItem.iHitStars         = iHitStars
                    #
                    oTempItem.save()
                    #
                    bFoundCategoryForModel      = True
                    #
                    if oModel.id not in dModelIDinTitle:
                        #
                        dModelIDinTitle[ oModel.id ] = sInTitle
                        #
                    #
                    if bRecordSteps and oModel.cTitle == 'E88CC':
                        maybePrint()
                        maybePrint( 'E88CC iInTitleLocation:', iInTitleLocation )
                    #
                #
            #
            if lNewItemFoundTemp:
                #
                lItemFoundTemp.extend( lNewItemFoundTemp )
                #
            #
            if bCategoryFamilyRelation and not bFoundCategoryForModel:
                #
                if oModel.iCategory_id in dCategoryFamily:
                    #
                    iFamily = dCategoryFamily[ oModel.iCategory_id ]
                    #
                    if iFamily in dFamilyCategory:
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
                oTempItem = ItemFoundTemp(
                        iItemNumb       = oItemFound,
                        iHitStars       = oModel.iStars,
                        iStarsModel     = oModel.iStars,
                        cFoundModel     = sInTitle,
                        cModelAlphaNum  = sModelAlphaNum,
                        iFoundModelLen  = len( sModelAlphaNum ),
                        iSearch         = oUserItem.iSearch,
                        iModel          = oModel )
                #
                oTempItem.save()
                #
                lItemFoundTemp.append( oTempItem )
                #
            #
        #
        if len( dModelIDinTitle ) > 1:
            #
            oModelLocated = _getModelLocationsBegAndEnd(
                    sAuctionTitleRelevantPart, dModelIDinTitle.values() )
            #
            # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
            #
            # if a model is both near the beginning and end, the one on the end does not count
            #
            if oModelLocated is not None:
                #
                dAllWordLocations = oModelLocated.dAllWordLocations
                #
                for sModel in dAllWordLocations.keys():
                    #
                    tModelLocation = dAllWordLocations[ sModel ]
                    #
                    if (    len( tModelLocation ) > 1 and
                            tModelLocation[ 0] in oModelLocated.tNearFront and
                            tModelLocation[-1] in oModelLocated.tNearEnd ):
                        #
                        dAllWordLocations[ sModel ] = (
                                i for i in tModelLocation
                                if i not in oModelLocated.tNearEnd )
                        #
                    #
                #
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
                maybePrint( 'oModelLocated tNearFront, tOnEnd, tNearEnd, tInParens:',
                        o.tNearFront, o.tOnEnd, o.tNearEnd, o.tInParens )
                maybePrint( 'dAllWordLocations:' )
                maybePrettyP( o.dAllWordLocations )
        #
        #
        #
        # finished stepping thru models
        #
        # next: step thru brands
        #
        #
        #
        #
        lBrands = dFindSteps[ 'brands' ]
        #
        setGotBrandsIDs = set( [] )
        #
        bGotBrandForNonGenericModel = False
        #
        for oBrand in qsBrands:
            #
            foundItem = getFoundItemTester(
                            oBrand, dFindersBrands, bAddDash = True )
            #
            bFoundBrandForModel = False
            #
            t = foundItem( sAuctionTitleRelevantPart )
            #
            sInTitle, uGotKeyWordsOrNoKeyWords, uExcludeThis, sWhatRemains = t
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
            setModelsBrands = set( [] )
            #
            setGotBrandsIDs.add( oBrand.id )
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
            # django discrepancy between 1.11 and 2.2 here
            # django 2.2 gets confused when an item is added to lItemFoundTemp
            # try workaround here!
            #
            for oTempItem in lItemFoundTemp:
                #
                tModelBrand = ( oTempItem.iModel, oBrand )
                #
                oItemFoundTempModel = None
                #
                if oTempItem.iModel:
                    oItemFoundTempModel = Model.objects.get(
                                            id = oTempItem.iModel.id )
                #
                if   (      oTempItem.iModel                and
                        not oTempItem.iModel.bGenericModel  and
                        oItemFoundTempModel                 and
                        oItemFoundTempModel.iBrand == oTempItem.iBrand ):
                    #
                    bFoundBrandForModel = True
                    #
                elif (  oTempItem.iModel                and
                        oTempItem.iBrand                and
                        oTempItem.iModel.bGenericModel  and
                        oTempItem.iCategory             and
                        tModelBrand not in setModelsBrands ):
                    #

                    bSaveBrand = BrandCategory.objects.filter(
                        iUser     = oUser,
                        iBrand    = oBrand,
                        iCategory = oTempItem.iCategory ).exists()
                    #
                    if bRecordSteps:
                        #
                        maybePrint()
                        maybePrint( 'bSaveBrand:', bSaveBrand )
                        #
                        _appendIfNotAlreadyIn( lBrands,
                                'found another brand %s for generic model %s' %
                                ( oBrand.cTitle, oTempItem.iModel.cTitle ) )
                        #
                    #
                    oAnotherTempItem = copy( oTempItem )
                    #
                    oAnotherTempItem.iBrand      = None
                    oAnotherTempItem.iStarsBrand = 0
                    oAnotherTempItem.iHitStars   = 0
                    #
                    lItemFoundTemp.append( oAnotherTempItem )
                    #
                    continue
                    #
                elif (      oTempItem.iModel and
                        (   oTempItem.iBrand is None or
                            oTempItem.iBrand != oBrand ) ):
                    #
                    bSaveBrand = False
                    #
                    if oBrand == oTempItem.iModel.iBrand:
                        #
                        oTempItem.iBrand = oBrand
                        #
                        bSaveBrand = True
                        #
                        if bRecordSteps:
                            #
                            _appendIfNotAlreadyIn( lBrands,
                                    'found brand %s for model %s' %
                                    ( oBrand.cTitle, oTempItem.iModel.cTitle ) )
                            #
                        #
                        bGotBrandForNonGenericModel = True
                        #
                        bFoundBrandForModel = True
                        #
                    elif    (   oItemFoundTempModel                  and
                                oItemFoundTempModel.iBrand == oBrand and
                                oTempItem.iBrand != oBrand ):
                        #
                        oTempItem.iBrand = oBrand
                        #
                        bSaveBrand = True
                        #
                        bFoundBrandForModel = True
                        #
                    elif oTempItem.iModel.bGenericModel and oTempItem.iCategory:
                        #
                        bSaveBrand = BrandCategory.objects.filter(
                            iUser     = oUser,
                            iBrand    = oBrand,
                            iCategory = oTempItem.iCategory ).exists()
                        #
                    #
                    if bSaveBrand and tModelBrand not in setModelsBrands:
                        #
                        if (    bRecordSteps and
                                oTempItem.iModel.bGenericModel and
                                not bGotBrandForNonGenericModel ):
                            #
                            _appendIfNotAlreadyIn( lBrands,
                                    'found brand %s for generic model %s' %
                                    ( oBrand.cTitle, oTempItem.iModel.cTitle ) )
                            #
                        #
                        oTempItem.iStarsBrand  = oBrand.iStars
                        oTempItem.iBrand       = oBrand
                        #
                        iStarsCategory  = oTempItem.iStarsCategory  or 1
                        iStarsModel     = oTempItem.iStarsModel     or 1
                        #
                        iHitStars = (   iStarsCategory *
                                        iStarsModel *
                                        oBrand.iStars )
                        #
                        oTempItem.iHitStars    = iHitStars
                        #
                        oTempItem.save()
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
                oTempItem.iStarsBrand  = oBrand.iStars
                oTempItem.iBrand       = oBrand
                #
                iStarsCategory          = oCategory.iStars or 1
                #
                iHitStars = iStarsCategory * oBrand.iStars
                #
                oTempItem.iHitStars    = iHitStars
                #
                oTempItem = ItemFoundTemp(
                        iItemNumb       = oItem,
                        iBrand          = oBrand,
                        iCategory       = oCategory,
                        iStarsBrand     = iBrandStars,
                        iStarsCategory  = iStarsCategory,
                        iHitStars       = iHitStars,
                        iSearch         = oUserItem.iSearch )
                #
                oTempItem.save()
                #
                lItemFoundTemp.append( oTempItem )
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
                oTempItem = ItemFoundTemp(
                        iItemNumb       = oItem,
                        iBrand          = oBrand,
                        iStarsBrand     = oBrand.iStars,
                        iHitStars       = iBrandStars,
                        iSearch         = oUserItem.iSearch )
                #
                oTempItem.save()
                #
                lItemFoundTemp.append( oTempItem )
                #
            #
        #
        #
        #
        #
        # finished stepping thru brands
        #
        # next: score candidates
        #
        #
        #
        tNow = timezone.now()
        #
        lCandidates = dFindSteps[ 'candidates' ]
        lSelect     = dFindSteps[ 'selection' ]
        #
        if lItemFoundTemp:
            #
            lExcludeThese = []
            #
            if len( lItemFoundTemp ) > 1:
                #
                if bRecordSteps:
                    #
                    lCandidates.append(
                            'scoring (total, hit stars, found length): '
                            '%s candidates'
                            % len( lItemFoundTemp ) )
                    #
                #
            #
            if oModelLocated: # some on the end of the auctin title
                #
                # tNearFront, tOnEnd, tNearEnd, tInParens, dAllWordLocations
                #
                dModelID_oTempItem = dict(
                        ( ( oTempItem.iModel.id, oTempItem )
                            for oTempItem in lItemFoundTemp
                            if oTempItem.iModel is not None ) )
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
                for iModelID, sInTitle in dModelIDinTitle.items():
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
                        dModelID_oTempItem )
                #
                setCategoriesOnEnd  = _getCategoriesForPositions(
                        oModelLocated.tOnEnd,
                        dLocationsModelIDs,
                        dModelID_oTempItem )
                #
                setCategoriesNearEnd  = _getCategoriesForPositions(
                        oModelLocated.tNearEnd,
                        dLocationsModelIDs,
                        dModelID_oTempItem )
                #
                if bRecordSteps:
                    #
                    maybePrint()
                    maybePrint( 'setCategoriesBeg:', setCategoriesBeg )
                    maybePrint( 'setCategoriesOnEnd:', setCategoriesOnEnd )
                    maybePrint( 'setCategoriesNearEnd:', setCategoriesNearEnd )
                    maybePrint( 'len( lItemFoundTemp ) before:', len( lItemFoundTemp ) )
                    maybePrint( 'dModelID_oTempItem:' )
                    # maybePrettyP( dModelID_oTempItem )
                    for k, o in dModelID_oTempItem.items():
                        maybePrint( ' %s: %s, %s' % ( k, o.iModel, o.iCategory ) )
                    maybePrint( 'dLocationsModelIDs:' )
                    maybePrettyP( dLocationsModelIDs )
                    maybePrint( 'lItemFoundTemp (iModel, iBrand, iCategory):')
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
                if bRecordSteps:
                    #
                    maybePrint( 'setGotBrandsIDs:', setGotBrandsIDs )
                    maybePrint( 'bGotBrandForNonGenericModel:', bGotBrandForNonGenericModel )
                    #
                #
                if setGotBrandsIDs and bGotBrandForNonGenericModel:
                    #
                    for iModelID, oTempItem in dModelID_oTempItem.items():
                        #
                        if  (   oTempItem.iBrand is None or
                                oTempItem.iBrand.id not in setGotBrandsIDs ):
                            #
                            lExcludeThese.append( oTempItem )
                            #
                            if bRecordSteps:
                                #
                                #
                                lCandidates.append(
                                    'do not have brand for model %s, '
                                    'so excluding' % oTempItem.iModel )
                                #
                            #
                        #
                    #
                    lItemFoundTemp = [ o for o in lItemFoundTemp
                                      if o not in lExcludeThese ]
                    #
                    lExcludeThese = []
                    #
                #
                if bRecordSteps:
                    #
                    maybePrint( 'setCategoriesBeg:', setCategoriesBeg )
                    maybePrint( 'oModelLocated.tInParens:', oModelLocated.tInParens )
                    maybePrint( 'lItemFoundTemp:' )
                    for o in lItemFoundTemp:
                        maybePrint( '  %s - %s - %s' % ( o.iModel, o.iBrand, o.iCategory ) )
                    #
                if setCategoriesBeg or oModelLocated.tInParens:
                    #
                    lExcludeThese = []
                    #
                    o = oModelLocated
                    #
                    tTests = (
                        ( o.tOnEnd,   'on end of',       setCategoriesOnEnd ),
                        ( o.tInParens,'within parens in',None ),
                        ( o.tNearEnd, 'near end of',     setCategoriesNearEnd))
                    #
                    for tLocations, sSay, setTest in tTests:
                        #
                        # o = oModelLocated
                        # o.tNearFront, o.tOnEnd, o.tNearEnd, o.tInParens
                        #
                        if setTest is not None:
                            #
                            if not setCategoriesBeg & setTest: # intersection
                                #
                                continue # categories different
                                #
                            #
                        #
                        if bRecordSteps:
                            #
                            maybePrint( 'tLocations:', tLocations )
                            #
                        #
                        for iLocation in tLocations:
                            #
                            if iLocation in dLocationsModelIDs:
                                #
                                for iModelID in dLocationsModelIDs[ iLocation ]:
                                    #
                                    lExcludeThese.append(
                                            dModelID_oTempItem[ iModelID ] )
                                    #
                                    if bRecordSteps:
                                        #
                                        sModel = dModelID_oTempItem[ iModelID ].iModel
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
                                        ( iLocation, oItem.iItemNumb ) )
                                    #
                                #
                            #
                        #
                    #
                    #
                    lItemFoundTemp = [ o for o in lItemFoundTemp
                                      if o not in lExcludeThese ]
                    #

                if bRecordSteps:
                    #
                    maybePrint( 'len( lItemFoundTemp ) after:', len( lItemFoundTemp ) )

            if len( lItemFoundTemp ) > 1:
                #
                t = _getFoundModelBooster( lItemFoundTemp, bRecordSteps )
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
                lSortItems = []
                #
                for i in range( len( lItemFoundTemp ) ):
                    #
                    oTempItem = lItemFoundTemp[ i ]
                    #
                    iFoundModelMultiplier = oTempItem.iFoundModelLen or 1
                    #
                    if oTempItem.iFoundModelLen == iMaxLen:
                        #
                        iScoreStars = round( (
                            iFoundModelMultiplier * oTempItem.iHitStars
                            ) * nFoundModelBoost )
                        #
                    else:
                        #
                        iScoreStars = int( (
                            iFoundModelMultiplier * oTempItem.iHitStars
                            ) / nFoundModelBoost )
                        #
                    #
                    if  (       oTempItem.iModel is not None and
                                oTempItem.iBrand is None and
                                oTempItem.iModel.iBrand is not None ):
                        #
                        if bRecordSteps:
                            #
                            lCandidates.append(
                                'did not find brand for %s, so discounting'
                                % oTempItem.iModel )
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
                              oTempItem.iHitStars,
                              oTempItem.iFoundModelLen,
                              getTitleOrNone( oTempItem.iCategory ),
                              getTitleOrNone( oTempItem.iModel ),
                              getTitleOrNone( oTempItem.iBrand ) ) )
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
                for i in range( len( lItemFoundTemp ) ):
                    #
                    oItemTemp = lItemFoundTemp[ lSortItems[i][1] ]
                    #
                    sTitle = None
                    #
                    if oTempItem.iModel:
                        sTitle          = getWhatsNotInParens(
                                            oTempItem.iModel.cTitle ).upper()
                        if oTempItem.iModel.bSubModelsOK:
                            sTitle      = sTitle[ : -1 ]
                    #
                    if (    settings.COVERAGE and
                            bRecordSteps and
                            ( iTopScoreStars is None or ( sTopTitle and sTitle) ) ):
                        #
                        maybePrint()
                        maybePrint( 'i:', i )
                        maybePrint( 'iScoreStars:', lSortItems[i][0] )
                        maybePrint( 'oItemTemp.iHitStars:', oItemTemp.iHitStars )
                        maybePrint( 'sTopTitle:', sTopTitle)
                        maybePrint( 'sTitle:', sTitle)
                        #
                    #
                    if iTopScoreStars is None:
                        #
                        iTopScoreStars  = lSortItems[i][0]
                        iTopHitStars    = oItemTemp.iHitStars
                        oTopStars       = oItemTemp
                        sTopTitle       = sTitle
                        #
                        continue
                    #
                    if (    oItemTemp.iHitStars >= iTopHitStars and
                            sTopTitle                           and
                            sTitle                              and
                            len( sTitle ) < len( sTopTitle )    and
                            sTitle in sTopTitle ):
                        #
                        # discount this
                        #
                        oItemTemp.iHitStars = (
                                oItemTemp.iHitStars *
                                iTopHitStars /
                                iTopScoreStars )
                        #
                        bSortAgain = True
                        #
                        if bRecordSteps:
                            #
                            lCandidates.append( 'discounting Hit Stars for %s' % oItemTemp.iModel )
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
                # sort lItemFoundTemp, more stars on top, fewer stars on bottom
                #
                lItemFoundSort = [ lItemFoundTemp[ t[1] ] for t in lSortItems ]
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                            lSelect,
                            'on top:   %s : %s : %s' %
                            ( getTitleOrNone( lItemFoundSort[0].iCategory ),
                              getTitleOrNone( lItemFoundSort[0].iModel ),
                              getTitleOrNone( lItemFoundSort[0].iBrand )) )
                    #
                    #maybePrint()
                    #maybePrint( 'len( lItemFoundSort ):', len( lItemFoundSort ) )
                    #
                #
            else:
                #
                lItemFoundSort = lItemFoundTemp
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                            lSelect,
                            'only found one thing for this item, a no brainer!' )
                    #
                #
            #
            iItemsFoundTemp         = 0
            #
            dModelsStoredAlready    = {} # used for scoring & selection
            #
            lModelsStoredAlready    = []
            #
            for oTempItem in lItemFoundSort:
                #
                iItemsFoundTemp += 1
                #
                sModelTitleLessParens = sModelTitleUPPER = ''
                #
                if oTempItem.iModel:
                    #
                    # sModelTitleLessParens = getWhatsNotInParens(
                    #         oTempItem.iModel.cTitle )
                    #
                    sModelTitleLessParens = oTempItem.cFoundModel
                    #
                    # sModelTitleUPPER = sModelTitleLessParens.upper()
                    #
                    # sModelTitleUPPER = oTempItem.cModelAlphaNum
                    sModelTitleUPPER = oTempItem.cFoundModel.upper()
                #
                if settings.COVERAGE and bRecordSteps:
                    #
                    maybePrint()
                    maybePrint( 'temp item      #:', iItemsFoundTemp )
                    maybePrint( 'model           :', oTempItem.iModel )
                    maybePrint( 'brand           :', oTempItem.iBrand )
                    maybePrint( 'category        :', oTempItem.iCategory)
                    maybePrint( 'sModelTitleUPPER:', sModelTitleUPPER )
                    maybePrint( 'iHitStars       :', oTempItem.iHitStars )
                    maybePrint()
                    #
                #
                if iItemsFoundTemp == 1: # store item on top here
                    #
                    oUserItem.iBrand        = oTempItem.iBrand
                    oUserItem.iCategory     = oTempItem.iCategory
                    oUserItem.iModel        = oTempItem.iModel
                    #
                    oUserItem.iHitStars     = oTempItem.iHitStars
                    oUserItem.cWhereCategory= oTempItem.cWhereCategory
                    # oUserItem.iSearch     = oTempItem.iSearch
                    #
                    oUserItem.tLook4Hits = tNow
                    #
                    oUserItem.save()
                    #
                    if oTempItem.iModel:
                        #
                        lModelsStoredAlready.append( sModelTitleUPPER )
                        #
                        _updateModelsStoredAlready(
                                dModelsStoredAlready, oTempItem, sModelTitleUPPER )
                        #
                    #
                    # testing problem work around 2019-12-18
                    #
                    if oTempItem.iSearch_id in dSearchLogs:
                        #
                        oSearchLog = dSearchLogs.get( oTempItem.iSearch_id )
                        #
                    else:
                        #
                        try:
                            oSearchLog = SearchLog.objects.get( iSearch = oTempItem.iSearch )
                        except:
                            #
                            if settings.TESTING:
                                #
                                oSearchLog = SearchLog(
                                                iSearch_id  = oTempItem.iSearch_id,
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
                        dSearchLogs[ oTempItem.iSearch_id ] = oSearchLog
                        #
                    #
                    if (    oTempItem.iBrand and
                            oTempItem.iCategory and
                            oTempItem.iModel ):
                        #
                        oSearchLog.iItemHits += 1
                        #
                    #
                elif (  oTempItem.iBrand and
                        oTempItem.iCategory and
                        oTempItem.iModel ):
                    #
                    # have complete hit, make an additional UserItem record
                    #
                    t = _gotFullStringOrSubStringOfListItem(
                                sModelTitleUPPER,
                                lModelsStoredAlready )
                    #
                    uExact, uLonger, uShort = t
                    #
                    bGotNonGenericForThis      = False
                    sBetterBrandForThisGeneric = None
                    #
                    # dModelsStoredAlready used for scoring & selection
                    #
                    if sModelTitleUPPER in dModelsStoredAlready:
                        #
                        if bRecordSteps:
                            maybePrint()
                            maybePrint( 'sModelTitleUPPER in dModelsStoredAlready:', sModelTitleUPPER in dModelsStoredAlready )
                        for oModelStored in dModelsStoredAlready[ sModelTitleUPPER ]:
                            #
                            # startswith below handles Amperex Bugle Boy & Amperex
                            #
                            bGotNonGenericForThis = (
                                    oModelStored.iModelBrand and
                                    oTempItem.iBrand and
                                    oModelStored.iModelBrand.cTitle.startswith(
                                            oTempItem.iBrand.cTitle ) and
                                    not oModelStored.bGenericModel )
                            #
                            if bGotNonGenericForThis: continue
                            #
                            if  (   oModelStored.iModelBrand is None and
                                    oModelStored.iBrand and
                                    oTempItem.iBrand    and
                                    oModelStored.iBrand.cTitle.startswith(
                                            oTempItem.iBrand.cTitle  ) ):
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
                                maybePrint( 'oTempItem.iBrand:', oTempItem.iBrand )
                                if oModelStored.iModelBrand:
                                    maybePrint( 'oModelStored.iModelBrand.cTitle:', oModelStored.iModelBrand.cTitle )
                                else:
                                    maybePrint( 'oModelStored.iModelBrand:', oModelStored.iModelBrand )
                                maybePrint( 'oTempItem.iBrand.cTitle:', oTempItem.iBrand.cTitle )
                                maybePrint( 'oModelStored.bGenericModel:', oModelStored.bGenericModel )
                                maybePrint( 'bGotNonGenericForThis:', bGotNonGenericForThis )
                                maybePrint( 'sBetterBrandForThisGeneric:', sBetterBrandForThisGeneric )
                                #
                            #
                            if sBetterBrandForThisGeneric: continue
                            #
                        #
                    #
                    bGotBrand = False
                    #
                    if (    oTempItem.iModel.iBrand is not None and
                            oTempItem.iModel.iBrand != oTempItem.iBrand ):
                        #
                        continue
                        #
                    elif uShort and uShort in dModelsStoredAlready:
                        #
                        for oModelStored in dModelsStoredAlready[ uShort ]:
                            #
                            bGotBrand = ( oModelStored.iModelBrand == oTempItem.iBrand )
                            #
                            if bGotBrand: continue
                            #
                        #
                    #
                    doPrintMore = (
                            False and
                            bRecordSteps and
                            sModelTitleUPPER == '6DJ8' )
                    #
                    if doPrintMore and not bGotNonGenericForThis:
                        #
                        maybePrint()
                        maybePrint( 'sModelTitleUPPER:', sModelTitleUPPER )
                        maybePrint( 'oTempItem.iModel:', oTempItem.iModel )
                        maybePrint( 'oTempItem.iBrand:', oTempItem.iBrand )
                        maybePrint( 'oTempItem.iCategory:', oTempItem.iCategory )
                        maybePrint( 'dModelsStoredAlready:' )
                        CustomPPrint.maybePrettyP( dModelsStoredAlready )
                        maybePrint( 'oTempItem.iModel.bGenericModel:', oTempItem.iModel.bGenericModel )
                        maybePrint( 'uExact:', uExact )
                        maybePrint( 'oModelStored:' )
                        maybePrint(  oModelStored )
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
                        #sWithout = oTempItem.cTitleLeftOver or ''
                        #
                        bGotLongGotShort = (
                                sModelTitleLessParens in sWithout )
                        #
                    #
                    if uLonger and bGotLongGotShort:
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
                    elif    (   uExact and
                                oTempItem.iModel.bGenericModel and
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
                                oTempItem.iModel.bGenericModel and
                                sBetterBrandForThisGeneric ):
                        #
                        if bRecordSteps:
                            #
                            _appendIfNotAlreadyIn(
                                lSelect,
                                    'excluding generic %s for %s -- '
                                    'already have a generic for %s' %
                                    ( sModelTitleLessParens,
                                      oTempItem.iBrand,
                                      sBetterBrandForThisGeneric ) )
                            #
                        #
                        continue
                        #
                    elif uExact and oTempItem.iModel.bGenericModel:
                        #
                        if bRecordSteps:
                            #
                            _appendIfNotAlreadyIn(
                                lSelect,
                                    'have generic model %s already, '
                                    'but including again for %s' %
                                    ( sModelTitleLessParens, oTempItem.iBrand ) )
                            #
                        #
                    elif (      uExact and
                                oModelStored and
                                oModelStored.iCategoryID and
                                oTempItem.iCategory and
                                oModelStored.iCategoryID != oTempItem.iCategory.id ):
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
                            iModel          = oTempItem.iModel,
                            iBrand          = oTempItem.iBrand,
                            iCategory       = oTempItem.iCategory ).exists():
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
                                    (   getTitleOrNone( oTempItem.iCategory ),
                                        getTitleOrNone( oTempItem.iModel ),
                                        getTitleOrNone( oTempItem.iBrand )) )
                            #
                        #
                        oNewUserItem = UserItemFound(
                            iItemNumb       = oUserItem.iItemNumb,
                            iHitStars       = oTempItem.iHitStars,
                            iSearch         = oTempItem.iSearch,
                            iModel          = oTempItem.iModel,
                            iBrand          = oTempItem.iBrand,
                            iCategory       = oTempItem.iCategory,
                            cWhereCategory  = oTempItem.cWhereCategory,
                            tLook4Hits      = tNow,
                            tCreate         = tNow,
                            tModify         = tNow,
                            iUser           = oUser )
                        #
                        #
                        oNewUserItem.save()
                        #
                        # dModelsStoredAlready used for scoring & selection
                        #
                        _updateModelsStoredAlready(
                                dModelsStoredAlready, oTempItem, sModelTitleUPPER )
                        #
                        lModelsStoredAlready.append( sModelTitleUPPER )
                        #
                    #
                #
            #
            # before going on, update userFinder, dModelsStoredAlready has the info
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
                        iItemNumb       = oItem,
                        iHitStars       = iMaxStars,
                        iMaxModel       = iMaxModel,
                        cTitle          = oItem.cTitle,
                        cMarket         = oItem.cMarket,
                        cListingType    = oItem.cListingType,
                        tTimeEnd        = oItem.tTimeEnd,
                        iUser           = oUser )
                    #
                #
                oUserFinder.save()
                #
            #
        else: # not lItemFoundTemp
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
        #
        if bRecordSteps:
            #
            _printHitSearchSteps( oItem, dFindSteps )
            #
        #
    #
    for oSearchLog in dSearchLogs.values():
        #
        if not oSearchLog.iOrigHits:
            #
            oSearchLog.save()
        #
    #
    if bCleanUpAfterYourself:
        #
        ItemFoundTemp.objects.all().delete()
        #
    #
