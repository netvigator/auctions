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


def _getTitleRegExress( oTableRow, bAddDash = False, bSubModelsOK = False ):
    #
    '''gets the RegEx expression for title + look for
    (comibines title & look for into one RegEx expression)'''
    #
    sLook4Title = getWhatsLeft( oTableRow.cTitle )
    #
    sRegExpress = getRegExpress( sLook4Title,
                                 bAddDash       = bAddDash,
                                 bSubModelsOK   = bSubModelsOK,
                                 iWordBoundChrs = WORD_BOUNDARY_MAX )
    #
    if oTableRow.cLookFor is not None and oTableRow.cLookFor:
        #
        sLookFor = oTableRow.cLookFor.strip()
        #
        sRegExpress = '|'.join( (   sRegExpress,
                                    getRegExpress(
                                        sLookFor,
                                        bAddDash       = bAddDash,
                                        iWordBoundChrs = WORD_BOUNDARY_MAX ) ) )
        #
        # removed 2018-06-12 solve Altec 803 problem
        #                               bSubModelsOK   = bSubModelsOK,
        #
    #
    return sRegExpress



def _getRowRegExpressions( oTableRow,
                           bAddDash = False, bSubModelsOK = False ):
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
                                         bSubModelsOK = bSubModelsOK )
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
                        iWordBoundChrs = WORD_BOUNDARY_MAX )
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
                        bAddDash = False, bSubModelsOK = False ):
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
                                   bSubModelsOK = bSubModelsOK )
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



def findSearchHits(
            iUser                   = oUserOne.id,
            bCleanUpAfterYourself   = True,
            bShowProgress           = False,
            bRecordSteps            = False ):
    #
    from brands.models      import Brand
    from categories.models  import Category
    from models.models      import Model
    #
    oForWithFinder = getRegExObj( r' (?:for|with|fits) ' )
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
            ( 'brands',     [] ) ) )
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
        sRelevantTitle = oForWithFinder.split( oItem.cTitle )[0]
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
            foundItem = getFoundItemTester( oCategory, dFindersCategories )
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
                    lCategories.append( 'excluded: %s' % oCategory.cTitle )
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
                        lCategories.append( '%s in title' % sInTitle )
                        #
                    elif bInHeirarchy1:
                        #
                        lCategories.append(
                            '%s in primary caregory' % oCategory.cTitle )
                        #
                    elif bInHeirarchy2:
                        #
                        lCategories.append(
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
            foundItem = getFoundItemTester( oModel, dFindersModels,
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
                    lModels.append( 'excluded: %s' % oCategory.oModel )
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
                        lModels.append( '%s in title' % sInTitle )
                        #
                    else:
                        #
                        lModels.append(
                            'for model "%s", "%s" is in title' %
                            ( oModel.cTitle, sInTitle ) )
                        #
                    #
                #
                for oTempItem in lItemFoundTemp:
                    #
                    if    ( oModel.iCategory == oTempItem.iCategory and
                            oTempItem.iModel is None ):
                        #
                        if bRecordSteps:
                            #
                            lModels.append( 'item has category for model %s' % oModel.cTitle )
                            #
                        #
                        oTempItem.iModel            = oModel
                        #
                        oTempItem.iStarsModel       = oModel.iStars
                        #
                        # reduce the length boost if the match is in parens
                        #
                        if sGotInParens and sInTitle in sGotInParens:
                            #
                            oTempItem.iFoundModelLen= getLen( sInTitle ) // 3
                            #
                        else:
                            #
                            oTempItem.iFoundModelLen= getLen( sInTitle )
                            #
                        #
                        iHitStars = oTempItem.iStarsCategory * oModel.iStars
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
                if not bFoundCategoryForModel:
                    #
                    if bRecordSteps:
                        #
                        lModels.append( 'item does not have category for model %s' % oModel.cTitle )
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
                    #if oItem.iItemNumb == 162988530803:
                        #print('')
                        #print('model found but no category:', oModel.cTitle )
                    #
                #
            #
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
            if sInTitle and not bExcludeThis:
                #
                #if oItem.iItemNumb == 123046984227 and oBrand.cTitle == 'GE':
                    #print('sInTitle and not bExcludeThis')
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
                        bSaveBrand = False
                        #
                        if oBrand == oTempItem.iModel.iBrand:
                            #
                            bSaveBrand = True
                            #
                        elif oTempItem.iModel.bGenericModel:
                            #
                            bSaveBrand = BrandCategory.objects.filter(
                                iUser     = oUser,
                                iBrand    = oBrand,
                                iCategory = oTempItem.iCategory
                                ).exists()
                            #
                            #if oItem.iItemNumb == 123046984227 and oBrand.cTitle == 'GE' and oTempItem.iModel.cTitle == '5R4GA':
                                #print('did we find a BrandCategory?:', bSaveBrand )
                                #print('oUser:', oUser )
                                #print('oBrand:', oBrand )
                                #print('oTempItem.iCategory.cTitle:', oTempItem.iCategory.cTitle )
                            #
                        #
                        if bSaveBrand:
                            #
                            oTempItem.iStarsBrand  = oBrand.iStars
                            oTempItem.iBrand       = oBrand
                            #
                            iHitStars = (   oTempItem.iStarsCategory *
                                            oTempItem.iStarsModel *
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
                    oTempItem = ItemFoundTemp(
                            iItemNumb       = oItem,
                            iBrand          = oBrand,
                            iStarsBrand     = oBrand.iStars,
                            iHitStars       = oBrand.iStars,
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
        if lItemFoundTemp:
            #
            if len( lItemFoundTemp ) > 1:
                #
                lSortItems = []
                #
                for i in range( len( lItemFoundTemp ) ):
                    #
                    iScoreStars = ( lItemFoundTemp[i].iFoundModelLen *
                                    lItemFoundTemp[i].iHitStars )
                    #
                    lSortItems.append( ( iScoreStars, i ) )
                    #
                #
                lSortItems.sort()
                #
                lSortItems.reverse()
                #
                lItemFoundTemp = [ lItemFoundTemp[ t[1] ] for t in lSortItems ]
                #
            #
            iItemsFoundTemp = 0
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
                else:
                    #
                    break
                    #
                #
            #
        else: # not lItemFoundTemp
            #
            oUserItem.tLook4Hits = tNow
            #
            oUserItem.save()
            #
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



