from collections            import OrderedDict

from django.db.models       import Q, Max
from django.contrib.auth    import get_user_model
from django.utils           import timezone

from core.user_one          import oUserOne
from core.utils             import getWhatsLeft

from .models                import ( ItemFound, UserItemFound, ItemFoundTemp,
                                     Search, SearchLog )

from categories.models      import BrandCategory

from String.Count           import getAlphaNumCount as getLen
from String.Get             import getTextBeforeC
from String.Find            import getRegExpress, getRegExObj
from String.Output          import ReadableNo
from Utils.Progress         import TextMeter, DummyMeter

from searching              import WORD_BOUNDARY_MAX


def _getTitleRegExress(
            oTableRow,
            bAddDash     = False,
            bPluralize   = False ):
    #
    '''gets the RegEx expression for title + look for
    (comibines title & look for into one RegEx expression)'''
    #
    bSubModelsOK = ( hasattr( oTableRow, 'bSubModelsOK' ) and
                     oTableRow.bSubModelsOK )
    #
    sLook4Title = getWhatsLeft( oTableRow.cTitle )
    #
    sRegExpress = getRegExpress( sLook4Title,
                                 bAddDash       = bAddDash,
                                 bSubModelsOK   = bSubModelsOK,
                                 iWordBoundChrs = WORD_BOUNDARY_MAX,
                                 bPluralize     = bPluralize )
    #
    if oTableRow.cLookFor:
        #
        sLookFor = oTableRow.cLookFor.strip()
        #
        sRegExpress = '|'.join( (   sRegExpress,
                                    getRegExpress(
                                        sLookFor,
                                        bAddDash       = bAddDash,
                                        bSubModelsOK   = bSubModelsOK,
                                        iWordBoundChrs = WORD_BOUNDARY_MAX ) ) )
        #
    #
    return sRegExpress



def _getRowRegExpressions( oTableRow,
                           bAddDash     = False,
                           bPluralize   = False ):
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
                                         bAddDash     = bAddDash,
                                         bPluralize   = bPluralize )
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
                            iWordBoundChrs = WORD_BOUNDARY_MAX )
            #
            oTableRow.cRegExKeyWords = sFindKeyWords
            #
            bAnyUpdates = True
            #
        else:
            #
            sFindKeyWords = oTableRow.cRegExKeyWords
            #
        #
    #
    if oTableRow.cExcludeIf and not oTableRow.cRegExExclude:
        #
        sFindExclude = getRegExpress(
                        oTableRow.cExcludeIf,
                        iWordBoundChrs  = WORD_BOUNDARY_MAX,
                        bEscBegEndOfStr = False )
        #
        oTableRow.cRegExExclude   = sFindExclude
        #
        bAnyUpdates = True
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
        oRegExObj = getRegExObj( s )
        #
        return oRegExObj.search


_oParensSearcher = _getRegExSearchOrNone( r'(?<=\().*(?=\))' )

def getInParens( s ):
    #
    oMatch = _oParensSearcher( s )
    #
    uReturn = None
    #
    if oMatch is not None:
        #
        uReturn = oMatch.group(0)
        #
    #
    return uReturn


def _getRegExObjOrNone( s ):
    #
    if s:
        oRegExObj = getRegExObj( s )
        #
        return oRegExObj




def _includeNotExclude( s, findExclude ):
    #
    return findExclude is None or not findExclude( s )

def _gotKeyWordsOrNoKeyWords( s, findKeyWords ):
    #
    return findKeyWords is None or findKeyWords( s )


def getFoundItemTester( oTableRow, dFinders,
                        bAddDash     = False,
                        bSubModelsOK = False,
                        bPluralize   = False):
    #
    ''' pass model row instance, returns tester '''
    #
    if oTableRow.pk in dFinders:
        #
        foundItemTester = dFinders[ oTableRow.pk ]
        #
    else:
        #
        t = _getRowRegExpressions( oTableRow,
                                   bAddDash     = bAddDash,
                                   bPluralize   = bPluralize )
        #
        t = tuple( map( _getRegExObjOrNone, t ) )
        #
        findTitle, findExclude, findKeyWords = t
        #
        searchTitle = searchExclude = searchKeyWords = None
        #
        if findTitle    is not None: searchTitle     = findTitle.search
        if findExclude  is not None: searchExclude   = findExclude.search
        if findKeyWords is not None: searchKeyWords  = findKeyWords.search
        #
        def foundItemTester( s ):
            #
            sFoundInTitle = ''
            #
            oTitleMatch = searchTitle( s )
            #
            if oTitleMatch: sFoundInTitle = oTitleMatch.group(0)
            #
            bIncludeThis = _includeNotExclude( s, searchExclude )
            #
            if (    sFoundInTitle and
                    bIncludeThis and
                    _gotKeyWordsOrNoKeyWords( s, searchKeyWords ) ):
                #
                return sFoundInTitle, not bIncludeThis
                #
            else:
                #
                return '', not bIncludeThis
                #
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


def _printHitSearchSteps( iItemNumb, dFindSteps ):
    #
    print('')
    print('Item %s Hit Search Steps:' % iItemNumb )
    #
    for k, v in dFindSteps.items():
        #
        print( '  %s' % k )
        #
        for s in v:
            #
            print( '    %s' % s )
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



def _gotSubstringOfListItem( s, l ):
    #
    for sL in l:
        #
        if s in sL: return sL
    #

_oForFitsFinder = getRegExObj( r' (?:for|fits|tests|test)' )


def findSearchHits(
            iUser                   = oUserOne.id,
            bCleanUpAfterYourself   = True,
            bShowProgress           = False,
            setRecordStepsForThese  = () ):
    #
    from brands.models      import Brand
    from categories.models  import Category
    from models.models      import Model
    #
    oUserModel = get_user_model()
    #
    oUser = oUserModel.objects.get( id = iUser )
    #
    if (    bShowProgress and
            UserItemFound.objects.filter(
                    iUser = oUser,
                    tLook4Hits__isnull = True ).exists() ):
        #
        # no need to test
        #
        print( 'doing some big queries ...' )
        #
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
    bExcludeThis        = False
    #
    if bShowProgress: # progress meter for running in shell, no need to test
        #
        oProgressMeter = TextMeter()
        #
        print( 'counting items found ...' )
        #
        iItemsFound = len( qsItems )
        #
        sLineB4 = ( 'determining items found hit stars for %s ...' %
                    oUser.username )
        #
        sOnLeft = "%s %s" % ( ReadableNo( iItemsFound ), 'items found' )
        #
        oProgressMeter.start( iItemsFound, sOnLeft, sLineB4 )
        #
    else:
        #
        oProgressMeter = DummyMeter()
        #
    #
    iSeq = 0
    #
    qsCategories = Category.objects.filter( iUser = oUser )
    #
    qsModels = ( Model.objects
                    .select_related('iBrand')
                    .filter( iUser = oUser ) )
    #
    qsBrands = Brand.objects.filter( iUser = oUser )
    #
    dFindSteps = OrderedDict(
        (   ( 'categories', [] ),
            ( 'models',     [] ),
            ( 'brands',     [] ),
            ( 'candidates', [] ),
            ( 'selection',  [] ) ) )
    #
    for oItem in qsItems:
        #
        iSeq  += 1
        #
        oProgressMeter.update( iSeq )
        #
        qsUserItems = UserItemFound.objects.filter(
                iItemNumb   = oItem.iItemNumb,
                iUser       = oUser )
        #
        oUserItem = None
        #
        lDeleteThese = []
        #
        bRecordSteps = ( setRecordStepsForThese is not None and
                         oItem.iItemNumb in setRecordStepsForThese )
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
        #
        oTempItem = None
        lItemFoundTemp = []
        #
        oItemFound = ItemFound.objects.get( pk = oItem.iItemNumb )
        #
        # if title includes for or with, consider the part in front,
        # not what follows
        #
        sRelevantTitle = _oForFitsFinder.split( oItem.cTitle )[0]
        #
        if bRecordSteps and len( oItem.cTitle ) > len( sRelevantTitle ):
            #
            _appendIfNotAlreadyIn(
                    [], 'will search only this: %s' % bRecordSteps )
            #
        #
        #if oItem.iItemNumb == 162988530803:
            #print('')
            #print('Item 162988530803 is here' )
            #print('sRelevantTitle:', sRelevantTitle )
        #
        sGotInParens = getInParens( sRelevantTitle )
        #
        lCategories = dFindSteps[ 'categories' ]
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
            sInTitle, bExcludeThis = foundItem( sRelevantTitle )
            #
            if bExcludeThis:
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                            lCategories, 'excluded: %s' % oCategory.cTitle )
                    #
                #
                continue
                #
            else:
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
            if bGotCategory: # sInTitle or bInHeirarchy1 or bInHeirarchy2
                #
                if bRecordSteps:
                    #
                    if sInTitle:
                        #
                        _appendIfNotAlreadyIn( lCategories, 'category %s in title' % oCategory )
                        #
                    elif bInHeirarchy1:
                        #
                        _appendIfNotAlreadyIn( lCategories,
                            '%s in primary caregory' % oCategory.cTitle )
                        #
                    elif bInHeirarchy2:
                        #
                        _appendIfNotAlreadyIn( lCategories,
                            '%s in secondary caregory' % oCategory.cTitle )
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
                #if oItem.iItemNumb == 162988530803:
                    #print('')
                    #print('Category:', oCategory.cTitle )
            #
        #
        #if oItem.iItemNumb == 162988530803:
            #print('')
            #print('doing models now')
        #
        lModels = dFindSteps[ 'models' ]
        #
        for oModel in qsModels:
            #
            foundItem = getFoundItemTester(
                            oModel,
                            dFindersModels,
                            bAddDash = True,
                            bSubModelsOK = oModel.bSubModelsOK )
            #
            bFoundCategoryForModel = False
            #
            sInTitle, bExcludeThis = foundItem( sRelevantTitle )
            #
            #if oItem.iItemNumb == 162988530803 and oModel.cTitle == '311-90':
                #print('')
                #print('doing model 311-90 now')
                #print('sInTitle, bExcludeThis:', sInTitle, bExcludeThis )
            #
            if bExcludeThis:
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                            lModels, 'excluded: %s' % oModel.cTitle )
                    #
                #
                continue
                #
            #
            if sInTitle:
                #
                if bRecordSteps:
                    #
                    if sInTitle == oModel.cTitle:
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
                        _appendIfNotAlreadyIn( lModels,
                                'model "%s" excludes: %s' %
                                ( oModel.cTitle, oModel.cRegExExclude ) )
                        #
                    #
                #
                lNewItemFoundTemp = []
                #
                for oTempItem in lItemFoundTemp:
                    #
                    if      ( oModel.iCategory == oTempItem.iCategory and
                              oTempItem.iModel is not None and
                              oTempItem.iModel != oModel ):
                        #
                        if bRecordSteps:
                            #
                            _appendIfNotAlreadyIn(
                                    lModels,
                                    'adding model %s for category %s' %
                                    ( oModel.cTitle, oTempItem.iCategory ) )
                            #
                        #
                        oNewTempItem = ItemFoundTemp(
                                iItemNumb       = oTempItem.iItemNumb,
                                iStarsCategory  = oTempItem.iStarsCategory,
                                iHitStars       = oTempItem.iHitStars,
                                iSearch         = oTempItem.iSearch,
                                iCategory       = oTempItem.iCategory,
                                cWhereCategory  = oTempItem.cWhereCategory,
                                iModel          = oModel,
                                iStarsModel     = oModel.iStars)
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
                        #if oItem.iItemNumb == 162988530803:
                            #print('')
                            #print('model found for caregory:',
                                   #oModel.cTitle, oModel.iCategory.cTitle )
                        #
                        # break keep looking?
                        #
                #
                if lNewItemFoundTemp:
                    #
                    lItemFoundTemp.extend( lNewItemFoundTemp )
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
                    #
                    oTempItem = ItemFoundTemp(
                            iItemNumb       = oItemFound,
                            iHitStars       = oModel.iStars,
                            iStarsModel     = oModel.iStars,
                            iFoundModelLen  = getLen( sInTitle ),
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
            foundItem = getFoundItemTester( oBrand, dFindersBrands )
            #
            bFoundBrandForModel = False
            #
            sInTitle, bExcludeThis = foundItem( sRelevantTitle )
            #
            #if oItem.iItemNumb == 123046984227 and oBrand.cTitle == 'GE':
                #print('brand GE')
            #
            if bExcludeThis:
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                            lBrands, 'excluded: %s' % oBrand.cTitle )
                    #
                #
                continue
                #
            #
            if sInTitle:
                #
                #if oItem.iItemNumb == 123046984227 and oBrand.cTitle == 'GE':
                    #print('sInTitle and not bExcludeThis')
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
                    if (    oTempItem.iModel is not None and
                            oTempItem.iBrand is None ):
                        #
                        #if (    oItem.iItemNumb == 123046984227 and
                                #oBrand.cTitle == 'GE' and
                                #oTempItem.iModel.cTitle == '5R4GA' ):
                            #print('doing 5R4GA')
                        #
                        bSaveBrand = False
                        #
                        bGotBrandForNonGenericModel = False
                        #
                        if oBrand == oTempItem.iModel.iBrand:
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
                        elif oTempItem.iModel.bGenericModel and oTempItem.iCategory is not None:
                            #
                            bSaveBrand = BrandCategory.objects.filter(
                                iUser     = oUser,
                                iBrand    = oBrand,
                                iCategory = oTempItem.iCategory ).exists()
                            #
                        #
                        if bSaveBrand:
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
                        #
                    #
                #
                if not bFoundBrandForModel:
                    #
                    if bRecordSteps:
                        #
                        _appendIfNotAlreadyIn( lBrands,
                                'did not find brand %s for any model found' %
                                oBrand.cTitle )
                        #
                    #
                    iBrandStars = oBrand.iStars or 1
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
                    lCandidates.append( 'scoring (total, hit stars, found length):' )
                    #
                #
                lSortItems = []
                #
                for i in range( len( lItemFoundTemp ) ):
                    #
                    iFoundModelMultiplier = lItemFoundTemp[i].iFoundModelLen or 1
                    #
                    iScoreStars = ( iFoundModelMultiplier *
                                    lItemFoundTemp[i].iHitStars )
                    #
                    lSortItems.append( ( iScoreStars, i ) )
                    #
                    if bRecordSteps:
                        #
                        lCandidates.append(
                            '%s, %s, %s - %s : %s : %s' %
                            ( iScoreStars,
                              lItemFoundTemp[i].iHitStars,
                              lItemFoundTemp[i].iFoundModelLen,
                              getTitleOrNone( lItemFoundTemp[i].iCategory ),
                              getTitleOrNone( lItemFoundTemp[i].iModel ),
                              getTitleOrNone( lItemFoundTemp[i].iBrand ) ) )
                        #
                    #
                #
                lSortItems.sort()
                #
                lSortItems.reverse()
                #
                iTopScoreStars = iTopHitStars = None
                #
                for i in range( len( lItemFoundTemp ) ):
                    #
                    oItemTemp = lItemFoundTemp[ lSortItems[i][1] ]
                    #
                    if iTopScoreStars is None:
                        iTopScoreStars = lSortItems[i][0]
                        iTopHitStars   = oItemTemp.iHitStars
                        continue
                    #
                    if oItemTemp.iHitStars >= iTopHitStars:
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
                lItemFoundTemp = [ lItemFoundTemp[ t[1] ] for t in lSortItems ]
                #
                if bRecordSteps:
                    #
                    lSelect.append(
                        'on top:   %s : %s : %s' %
                        ( getTitleOrNone( lItemFoundTemp[0].iCategory ),
                          getTitleOrNone( lItemFoundTemp[0].iModel ),
                          getTitleOrNone( lItemFoundTemp[0].iBrand )) )
                    #
                #
            else:
                #
                if bRecordSteps:
                    #
                    lSelect.append( 'only found one thing for this item, a no brainer!' )
                    #
                #
            #
            iItemsFoundTemp = 0
            #
            lModelsStoredAlready = []
            #
            for oTempItem in lItemFoundTemp:
                #
                iItemsFoundTemp += 1
                #
                if iItemsFoundTemp == 1:
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
                        lModelsStoredAlready = [ oTempItem.iModel.cTitle ]
                    #
                    oSearchLog = dSearchLogs.get( oTempItem.iSearch_id )
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
                    uLonger = _gotSubstringOfListItem( oTempItem.iModel.cTitle, lModelsStoredAlready )
                    #
                    if uLonger:
                        #
                        if bRecordSteps:
                            #
                            lSelect.append(
                                    'excluding %s because '
                                    'this is substring of %s' %
                                    ( oTempItem.iModel.cTitle, uLonger ) )
                            #
                        #
                        continue
                        #
                    #
                    if bRecordSteps:
                        #
                        lSelect.append( 'also storing: %s : %s : %s' %
                                        (   getTitleOrNone( oTempItem.iCategory ),
                                            getTitleOrNone( oTempItem.iModel ),
                                            getTitleOrNone( oTempItem.iBrand )) )
                        #
                    tNow = timezone.now()
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
                    lModelsStoredAlready.append( oTempItem.iModel.cTitle )
                    #
                else:
                    #
                    break
                    #
                #
            #
        else: # not lItemFoundTemp
            #
            if bRecordSteps:
                #
                lSelect.append( 'did not find anything for this item' )
                #
            #
            oUserItem.tLook4Hits = tNow
            #
            oUserItem.save()
            #
        #
        if bRecordSteps:
            #
            _printHitSearchSteps( oItem.iItemNumb, dFindSteps )
            #
            #print('')
            #print('call stack:')
            #for i in range( len( inspect.stack() ) ):
                #if inspect.stack()[i][3].startswith( '__' ): break
                #print( inspect.stack()[i][3] )
        #
    #
    oProgressMeter.end( iSeq )
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



