from copy                   import copy

from collections            import OrderedDict

from django.conf            import settings
from django.db.models       import Q, Max
from django.contrib.auth    import get_user_model
from django.utils           import timezone

from core.user_one          import oUserOne
from core.utils             import getWhatsNotInParens

from .models                import ( ItemFound, UserItemFound, ItemFoundTemp,
                                     Search, SearchLog )

from categories.models      import BrandCategory

from String.Count           import getAlphaNumCount as getLen
from String.Get             import getTextBeforeC
from String.Find            import getRegExpress, getRegExObj, oFinderCRorLF
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
        sRegExpress = '|'.join( (   sRegExpress,
                                    getRegExpress(
                                        sLookFor,
                                        bAddDash       = bAddDash,
                                        bSubModelsOK   = False,
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


def _printHitSearchSteps( oItem, dFindSteps ):
    #
    if not settings.COVERAGE:
        #
        print('')
        print('Item %s Hit Search Steps:' % oItem.iItemNumb )
        print(' %s' % oItem.cTitle )
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



def _gotFullStringOrSubStringOfListItem( s, l ):
    #
    uGotSub  = None
    uGotFull = None
    uGotMore = None
    #
    sUpper = s.upper()
    #
    for sL in l:
        #
        sLupper = sL.upper()
        #
        if sUpper in sLupper:
            #
            if sUpper == sLupper:
                uGotFull = sL
            else:
                uGotSub  = sL
        elif sLupper in sUpper:
            uGotMore = sL
        #
    #
    return uGotFull, uGotSub, uGotMore



_oDropAfterThisFinder = getRegExObj(
        r' (?:\bfor\b|'
            r'\bfits\b|'
            r'\btests*\b|'
            r'\btested (?:on|with)\b|'
            r'\bfrom\b)|'
            r'\bused with\b|'
            r'\bsimilar to\b' ) # formerly oForFitsFinder

def _getRelevantTitle( sTitle ):
    #
    return _oDropAfterThisFinder.split( sTitle )[0]



def findSearchHits(
            iUser                   = oUserOne.id,
            bCleanUpAfterYourself   = True,
            bShowProgress           = False,
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
    dCategoryFamily     = {}
    dFamilyCategory     = {}
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
    for oCategory in qsCategories:
        #
        if oCategory.iFamily_id:
            #
            iFamily_id = oCategory.iFamily_id
            #
            dCategoryFamily[ oCategory.id ] = iFamily_id
            #
            setFamilyCategories = dFamilyCategory.setdefault( iFamily_id, set( [] ) )
            #
            setFamilyCategories.add( oCategory.id )
            #
        #
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
        bRecordSteps = ( iRecordStepsForThis is not None and
                         oItem.iItemNumb == iRecordStepsForThis )
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
        setGotCategories = set( [] )
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
            _appendIfNotAlreadyIn(
                    [], 'will search only this: %s' % bRecordSteps )
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
                setGotCategories.add( oCategory.id )
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
                            bSubModelsOK = oModel.bSubModelsOK )
            #
            bFoundCategoryForModel = False
            #
            sInTitle, bExcludeThis = foundItem( sRelevantTitle )
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
                bModelCategoryAlreadyFound = (
                        oModel.iCategory_id in setGotCategories )
                #
                for oTempItem in lItemFoundTemp: # lists categories found
                    #
                    if  (   bModelCategoryAlreadyFound and
                            oModel.iCategory != oTempItem.iCategory ):
                        #
                        continue
                        #
                    elif oModel.id in setModelsStoredAlready:
                        #
                        continue
                        #
                    else:
                        #
                        bCategoryFamilyRelation = (
                            oTempItem.iCategory and dCategoryFamily and
                            oTempItem.iCategory.id in dCategoryFamily and
                            oModel.iCategory_id in dCategoryFamily and
                                dCategoryFamily[ oModel.iCategory_id ] ==
                                dCategoryFamily[ oTempItem.iCategory.id ] )
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
                            iFamily = dCategoryFamily[ oModel.iCategory_id ]
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
                            _appendIfNotAlreadyIn(
                                    lModels,
                                    'model category %s is %s  of family%s' %
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
                if not bFoundCategoryForModel:
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
                                    lModels,
                                    'model category %s is a member of family %s' %
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
            setModelsBrands = set( [] )
            #
            if sInTitle:
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
                    if (    oTempItem.iModel is not None    and
                            oTempItem.iBrand is not None    and
                            oTempItem.iModel.bGenericModel  and
                            oTempItem.iCategory is not None and
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
                    elif (  oTempItem.iModel is not None and
                            oTempItem.iBrand is None ):
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
                            'scoring (total, hit stars, found length): %s'
                            % len( lItemFoundTemp ) )
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
                iTopScoreStars = iTopHitStars = oTopStars = None
                sTitle = sTopTitle = None
                #
                for i in range( len( lItemFoundTemp ) ):
                    #
                    oItemTemp = lItemFoundTemp[ lSortItems[i][1] ]
                    #
                    if oTempItem.iModel:
                        sTitle          = getWhatsNotInParens(
                                            oTempItem.iModel.cTitle ).upper()
                        if oTempItem.iModel.bSubModelsOK:
                            sTitle      = sTitle[ : -1 ]
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
                lItemFoundTemp = [ lItemFoundTemp[ t[1] ] for t in lSortItems ]
                #
                if bRecordSteps:
                    #
                    _appendIfNotAlreadyIn(
                            lSelect,
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
            for oTempItem in lItemFoundTemp:
                #
                iItemsFoundTemp += 1
                #
                sTitleLessParens = sTitleUPPER = ''
                #
                if oTempItem.iModel:
                    #
                    sTitleLessParens = getWhatsNotInParens(
                            oTempItem.iModel.cTitle )
                    #
                    sTitleUPPER = sTitleLessParens.upper()
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
                        lModelsStoredAlready.append( sTitleUPPER )
                        #
                        dModelsStoredAlready.setdefault(
                            sTitleUPPER, [] ).append(
                                ( oTempItem.iModel.bGenericModel,
                                  oTempItem.iModel.iBrand ) )
                        #
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
                    t = _gotFullStringOrSubStringOfListItem(
                                sTitleUPPER,
                                lModelsStoredAlready )
                    #
                    uExact, uLonger, uShort = t
                    #
                    bGotNonGenericForThis = False
                    #
                    if sTitleUPPER in dModelsStoredAlready:
                        #
                        for t in dModelsStoredAlready[ sTitleUPPER ]:
                            #
                            bThisIsGeneric, iThisBrand = t
                            #
                            bGotNonGenericForThis = (
                                    not bThisIsGeneric and
                                    iThisBrand == oTempItem.iBrand )
                            #
                            if bGotNonGenericForThis: break
                        #
                    #
                    bGotBrand = False
                    #
                    if uShort:
                        #
                        for t in dModelsStoredAlready[ uShort ]:
                            #
                            bThisIsGeneric, iThisBrand = t
                            #
                            bGotBrand = ( iThisBrand == oTempItem.iBrand )
                            #
                            if bGotBrand: break
                            #
                        #
                    #
                    if uLonger:
                        #
                        if bRecordSteps:
                            #
                            _appendIfNotAlreadyIn(
                                lSelect,
                                    'excluding %s because '
                                    'this is substring of %s' %
                                    ( sTitleLessParens, uLonger ) )
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
                                    'excluding %s because '
                                    'its root is %s' %
                                    ( sTitleLessParens, uShort ) )
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
                                    ( sTitleLessParens ) )
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
                                    ( sTitleLessParens, oTempItem.iBrand ) )
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
                                    ( sTitleLessParens, uExact ) )
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
                    if oTempItem.iModel:
                        #
                        dModelsStoredAlready.setdefault(
                            sTitleUPPER, [] ).append(
                                ( oTempItem.iModel.bGenericModel,
                                oTempItem.iModel.iBrand ) )
                        #
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



