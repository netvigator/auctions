import logging

from copy                   import copy
from pprint                 import pprint, pformat

from collections            import OrderedDict

from django.conf            import settings
from django.db.models       import Q, Max
from django.contrib.auth    import get_user_model
from django.utils           import timezone

from core.user_one          import oUserOne
from core.utils             import getWhatsNotInParens, maybePrint
from core.templatetags.core_tags import getDashForReturn

from .models                import Search, SearchLog

from categories.models      import BrandCategory

from finders.models         import ( ItemFound, UserItemFound, ItemFoundTemp,
                                     UserFinder )

from models.models          import Model

from searching              import WORD_BOUNDARY_MAX

from pyPks.Collect.Output   import getTextSequence
from pyPks.Collect.Query    import get1stThatMeets

from pyPks.File.Get         import getListFromFileLines
from pyPks.File.Test        import isFileThere
from pyPks.File.Write       import QuickDumpLines

from pyPks.Object.Get       import ValueContainer
from pyPks.Object.Output    import CustomPPrint

from pyPks.String.Count     import getAlphaNumCount as getLen
from pyPks.String.Dumpster  import getAlphaNumCleanNoSpaces
from pyPks.String.Get       import getTextBeforeC
from pyPks.String.Find      import getRegExpress, getRegExObj
from pyPks.String.Find      import oFinderCRorLFnMore as oFinderCRorLF
from pyPks.String.Replace   import getSpaceForWhiteAlsoStrip
from pyPks.String.Output    import ReadableNo

if settings.TESTING:
    from pyPks.Utils.Both2n3 import print3_n_2
    from pyPks.Object.Get   import ValueContainerCanPrint as ValueContainer


logger = logging.getLogger(__name__)

logging_level = logging.WARNING


SCRIPT_TEST_FILE            = '/tmp/auction_script_test.txt'
#


_oDropAfterThisFinder = getRegExObj(
    '(?<=[\W.,!?:;])'  # look back for this if u find any of the following
    '(?:'              # non grouping (saves CPU ticks)
        r'for\b|'
        r'fits\b|'
        r'tests*\b|'
        r'tested (?:on|with)\b|'
        r'from\b|'
        r'ala\b|'
        r'used (?:with|in|on)\b|'
        r'same as\b|'
        r'similar to\b)' ) # formerly oForFitsFinder


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
    iCategoryID = None
    #
    if oTempItem.iCategory:
        iCategoryID = oTempItem.iCategory.id
    #
    oThisModel = ValueContainer(
        bGenericModel   = oTempItem.iModel.bGenericModel,
        iModelBrand     = oTempItem.iModel.iBrand,
        bSubModelsOK    = oTempItem.iModel.bSubModelsOK,
        iModelID        = oTempItem.iModel.id,
        iHitStars       = oTempItem.iHitStars,
        sTitleLeftOver  = oTempItem.cTitleLeftOver,
        iCategoryID     = iCategoryID )
    #
    dModelsStoredAlready.setdefault(
        sModelTitleUPPER, [] ).append( oThisModel )
    #


def _getMaxHitStars( dModelsStoredAlready ):
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
    iLongerLen = oLongr.iFoundModelLen or 1
    iShortrLen = oShort.iFoundModelLen or 1
    #
    iLongerStars = oLongr.iHitStars or 1
    iShortrStars = oShort.iHitStars or 1
    #
    nBoost = ( ( float( iShortrStars ) * iShortrLen ) /
               ( iLongerStars * iLongerLen ) ) ** 0.5
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
    if len( lAllFoundIns ) < 2: return 1, iMaxLen
    #
    #
    #
    lAllFoundIns.sort()
    lAllFoundIns.reverse()
    #
    #
    if settings.COVERAGE and bRecordSteps:
        #
        maybePrint()
        maybePrint( 'lAllFoundIns:' )
        pprint( lAllFoundIns )
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
                if bRecordSteps:
                    #
                    maybePrint()
                    maybePrint( 'oLongr.iHitStars     :', oLongr.iHitStars      )
                    maybePrint( 'oShort.iHitStars     :', oShort.iHitStars      )
                    maybePrint( 'oLongr.cModelAlphaNum:', oLongr.cModelAlphaNum )
                    maybePrint( 'oShort.cModelAlphaNum:', oShort.cModelAlphaNum )
                    #
            #
        #
    #
    #
    #
    if not lGotModelOverlap: return 1, iMaxLen
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
    if settings.COVERAGE and bRecordSteps:
        #
        maybePrint()
        maybePrint( 'nBoost :', nBoost )
        maybePrint( 'iMaxLen:', iMaxLen )
        #
    #
    return nBoost, iMaxLen



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
        sRelevantTitle = _getRelevantTitle( oItem.cTitle )
        #
        if bRecordSteps and len( oItem.cTitle ) > len( sRelevantTitle ):
            #
            lPreliminary = dFindSteps[ 'preliminary' ]
            #
            _appendIfNotAlreadyIn(
                    lPreliminary, 'will consider only: %s' % sRelevantTitle )
            #
            sLoppedOff = oItem.cTitle[ len( sRelevantTitle ) : ]
            #
            _appendIfNotAlreadyIn(
                    lPreliminary, '(will ignore: %s)' % sLoppedOff )
            #
        #
        sGotInParens = getInParens( sRelevantTitle )
        #
        lCategories = dFindSteps[ 'categories' ]
        #
        lCategoryFound = []
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
            t = foundItem( sRelevantTitle )
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
        lModels = dFindSteps[ 'models' ]
        #
        setModelsStoredAlready = set( [] )
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
            t = foundItem( sRelevantTitle, bExplainVerbose )
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
            #
            sModelAlphaNum  = _getAlphaNum( sInTitle )
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
                elif oModel.id in setModelsStoredAlready:
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
                            logger.warning( '%s in %s' % ( oModel.iCategory_id, "dCategoryFamily" ) )
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
                    setModelsStoredAlready.add( oModel.id )
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
        #
        lBrands = dFindSteps[ 'brands' ]
        #
        for oBrand in qsBrands:
            #
            foundItem = getFoundItemTester(
                            oBrand, dFindersBrands, bAddDash = True )
            #
            bFoundBrandForModel = False
            #
            t = foundItem( sRelevantTitle )
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
                    bGotBrandForNonGenericModel = False
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
        tNow = timezone.now()
        #
        lCandidates = dFindSteps[ 'candidates' ]
        lSelect     = dFindSteps[ 'selection' ]
        #
        if lItemFoundTemp:
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
                nFoundModelBoost, iMaxLen = _getFoundModelBooster(
                                                lItemFoundTemp, bRecordSteps )
                #
                if bRecordSteps and nFoundModelBoost > 1:
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
                        if bRecordSteps:
                            #
                            lCandidates.append( 'discounting Hit Stars for %s' % oItemTemp.iModel )
                            #
                        #
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
            dModelsStoredAlready    = {}
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
                    bGotNonGenericForThis = False
                    #
                    if sModelTitleUPPER in dModelsStoredAlready:
                        #
                        for oModelStored in dModelsStoredAlready[ sModelTitleUPPER ]:
                            #
                            bGotNonGenericForThis = (
                                    oModelStored.iModelBrand == oTempItem.iBrand and
                                    not oModelStored.bGenericModel )
                            #
                            if bGotNonGenericForThis: continue
                        #
                    #
                    bGotBrand = False
                    #
                    if uShort and uShort in dModelsStoredAlready:
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
                            bRecordSteps and
                            sModelTitleUPPER == '6DJ8' )
                    #
                    if doPrintMore:
                        #
                        print()
                        print( 'sModelTitleUPPER:', sModelTitleUPPER )
                        print( 'oTempItem.iModel:', oTempItem.iModel )
                        print( 'oTempItem.iBrand:', oTempItem.iBrand )
                        print( 'oTempItem.iCategory:', oTempItem.iCategory )
                        print( 'dModelsStoredAlready:' )
                        CustomPPrint.pprint( dModelsStoredAlready )
                        print( 'oTempItem.iModel.bGenericModel:', oTempItem.iModel.bGenericModel )
                        print( 'uExact:', uExact )
                        print( 'oModelStored:' )
                        print(  oModelStored )
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
                        #t = foundItem( sRelevantTitle )
                        ##
                        #sInTitle, uGotKeyWords, uExcludeThis, sWhatRemains = t
                        ##
                        #lParts = sRelevantTitle.split( sInTitle )
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
                    oNewUserItem.save()
                    #
                    _updateModelsStoredAlready(
                            dModelsStoredAlready, oTempItem, sModelTitleUPPER )
                    #
                    lModelsStoredAlready.append( sModelTitleUPPER )
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
