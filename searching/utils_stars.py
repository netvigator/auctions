from django.db.models       import Q, Max
from django.contrib.auth    import get_user_model
from django.utils           import timezone

from core.user_one          import oUserOne
from core.utils             import getWhatsLeft

from .models                import ( ItemFound, UserItemFound, ItemFoundTemp,
                                     Search, SearchLog )

from categories.models      import BrandCategory

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
                                        bSubModelsOK   = bSubModelsOK,
                                        iWordBoundChrs = WORD_BOUNDARY_MAX ) ) )
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
    bRowHasKeyWords = hasattr( oTableRow, 'cKeyWords' )
    #
    sFindKeyWords = None
    #
    if oTableRow.cRegExLook4Title:
        #
        sFindTitle          = oTableRow.cRegExLook4Title
        sFindExclude        = oTableRow.cRegExExclude
        #
        if bRowHasKeyWords:
            sFindKeyWords   = oTableRow.cRegExKeyWords
        #
    else:
        #
        sFindTitle = _getTitleRegExress( oTableRow,
                                         bAddDash     = bAddDash,
                                         bSubModelsOK = bSubModelsOK )
        #
        sKeyWords = sFindKeyWords = sFindExclude = None
        #
        #
        if bRowHasKeyWords: sKeyWords = oTableRow.cKeyWords
        #
        sExcludeIf = oTableRow.cExcludeIf
        #
        if sExcludeIf:
            #
            sFindExclude = getRegExpress(
                            sExcludeIf,
                            iWordBoundChrs = WORD_BOUNDARY_MAX )
            #
        if sKeyWords:
            #
            sFindKeyWords = getRegExpress(
                            sKeyWords,
                            iWordBoundChrs = WORD_BOUNDARY_MAX )
            #
        #
        oTableRow.cRegExLook4Title= sFindTitle
        oTableRow.cRegExExclude   = sFindExclude
        #
        if bRowHasKeyWords:
            oTableRow.cRegExKeyWords = sFindKeyWords
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
            bIncludeThis = _includeNotExclude( s, searchExclude )
            #
            return (    searchTitle( s ) and
                        bIncludeThis and
                        _gotKeyWordsOrNoKeyWords( s, searchKeyWords ),
                     not bIncludeThis )
        #
        dFinders[ oTableRow.pk ] = foundItemTester
        #
    #
    return foundItemTester


def _whichGetsCredit( bInTitle, bInHeirarchy1, bInHeirarchy2 ):
    #
    if bInTitle:
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
            bShowProgress           = False ):
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
    for o in qsSearchLogs: o.iItemHits = 0
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
    qsCategories = Category.objects.filter(
            iUser = oUser ).order_by( '-iStars' )
    #
    qsModels = ( Model.objects
                    .select_related('iBrand')
                    .filter( iUser = oUser )
                    .order_by( '-iStars' ) )
    #
    qsBrands = Brand.objects.filter( iUser = oUser ).order_by( '-iStars' )
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
        oItemFoundTemp = None
        lItemFoundTemp = []
        #
        oItemFound = ItemFound.objects.get( pk = oItem.iItemNumb )
        #
        sRelevantTitle = oItem.cTitle
        #
        if ' for ' in sRelevantTitle.lower(): # abc for xyz
            #
            sRelevantTitle = getTextBeforeC( sRelevantTitle, ' for ' )
            #
        #
        #if oItem.iItemNumb == 162988530803:
            #print('')
            #print('Item 162988530803 is here' )
            #print('sRelevantTitle:', sRelevantTitle )
        for oCategory in qsCategories:
            #
            foundItem = getFoundItemTester( oCategory, dFindersCategories )
            #
            # the following are short circuiting --
            # if one is True, the following will be True
            # and the string will not be searched
            # so don't take bInHeirarchy1 & bInHeirarchy2 literally!
            #
            bInTitle, bExcludeThis = foundItem( sRelevantTitle )
            #
            if bExcludeThis:
                #
                continue
                #
            else:
                #
                bInHeirarchy1  = ( # will be True if bInTitle is True
                        bInTitle or
                        ( oItem.iCatHeirarchy and # can be None
                          foundItem(
                              oItem.iCatHeirarchy.cCatHierarchy )[0] ) )
                #
                bInHeirarchy2  = ( # will be True if either are True
                        bInTitle or
                        bInHeirarchy1 or
                        ( oItem.i2ndCatHeirarchy and
                          foundItem(
                              oItem.i2ndCatHeirarchy.cCatHierarchy )[0] ) )
                #
            #
            bGotCategory = bInTitle or bInHeirarchy1 or bInHeirarchy2
            #
            if bGotCategory: # bInTitle or bInHeirarchy1 or bInHeirarchy2
                #
                sWhich = _whichGetsCredit(
                            bInTitle, bInHeirarchy1, bGotCategory )
                #
                oItemFoundTemp = ItemFoundTemp(
                        iItemNumb       = oItemFound,
                        iStarsCategory  = oCategory.iStars,
                        iHitStars       = oCategory.iStars,
                        iSearch         = oUserItem.iSearch,
                        iCategory       = oCategory,
                        cWhereCategory  = sWhich )
                #
                oItemFoundTemp.save()
                #
                lItemFoundTemp.append( oItemFoundTemp )
                #
                #if oItem.iItemNumb == 162988530803:
                    #print('')
                    #print('Category:', oCategory.cTitle )
            #
        #
        #if oItem.iItemNumb == 162988530803:
            #print('')
            #print('doing models now')
        for oModel in qsModels:
            #
            foundItem = getFoundItemTester( oModel, dFindersModels,
                            bAddDash = True,
                            bSubModelsOK = oModel.bSubModelsOK )
            #
            bFoundCategoryForModel = False
            #
            bInTitle, bExcludeThis = foundItem( sRelevantTitle )
            #
            #if oItem.iItemNumb == 162988530803 and oModel.cTitle == '311-90':
                #print('')
                #print('doing model 311-90 now')
                #print('bInTitle, bExcludeThis:', bInTitle, bExcludeThis )
            if bInTitle and not bExcludeThis:
                #
                for oItemFoundTemp in lItemFoundTemp:
                    #
                    if    ( oModel.iCategory == oItemFoundTemp.iCategory and
                            oItemFoundTemp.iModel is None ):
                        #
                        oItemFoundTemp.iModel       = oModel
                        #
                        oItemFoundTemp.iStarsModel  = oModel.iStars
                        #
                        iHitStars = oItemFoundTemp.iStarsCategory * oModel.iStars
                        #
                        oItemFoundTemp.iHitStars    = iHitStars
                        #
                        oItemFoundTemp.save()
                        #
                        bFoundCategoryForModel      = True
                        #
                        #if oItem.iItemNumb == 162988530803:
                            #print('')
                            #print('model found for caregory:',
                                   #oModel.cTitle, oModel.iCategory.cTitle )
                        #
                        break
                        #
                #
                if not bFoundCategoryForModel:
                    #
                    oItemFoundTemp = ItemFoundTemp(
                            iItemNumb       = oItemFound,
                            iHitStars       = oModel.iStars,
                            iStarsModel     = oModel.iStars,
                            iSearch         = oUserItem.iSearch,
                            iModel          = oModel )
                    #
                    oItemFoundTemp.save()
                    #
                    lItemFoundTemp.append( oItemFoundTemp )
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
            bInTitle, bExcludeThis = foundItem( sRelevantTitle )
            #
            #if oItem.iItemNumb == 123046984227 and oBrand.cTitle == 'GE':
                #print('brand GE')
            if bInTitle and not bExcludeThis:
                #
                #if oItem.iItemNumb == 123046984227 and oBrand.cTitle == 'GE':
                    #print('bInTitle and not bExcludeThis')
                for oItemFoundTemp in lItemFoundTemp:
                    #
                    if (    oItemFoundTemp.iModel is not None and
                            oItemFoundTemp.iBrand is None ):
                        #
                        #if (    oItem.iItemNumb == 123046984227 and
                                #oBrand.cTitle == 'GE' and
                                #oItemFoundTemp.iModel.cTitle == '5R4GA' ):
                            #print('doing 5R4GA')
                        bSaveBrand = False
                        #
                        if oBrand == oItemFoundTemp.iModel.iBrand:
                            #
                            bSaveBrand = True
                            #
                        elif oItemFoundTemp.iModel.bGenericModel:
                            #
                            bSaveBrand = BrandCategory.objects.filter(
                                iUser     = oUser,
                                iBrand    = oBrand,
                                iCategory = oItemFoundTemp.iCategory
                                ).exists()
                            #
                            #if oItem.iItemNumb == 123046984227 and oBrand.cTitle == 'GE' and oItemFoundTemp.iModel.cTitle == '5R4GA':
                                #print('did we find a BrandCategory?:', bSaveBrand )
                                #print('oUser:', oUser )
                                #print('oBrand:', oBrand )
                                #print('oItemFoundTemp.iCategory.cTitle:', oItemFoundTemp.iCategory.cTitle )
                            #
                        #
                        if bSaveBrand:
                            #
                            oItemFoundTemp.iStarsBrand  = oBrand.iStars
                            oItemFoundTemp.iBrand       = oBrand
                            #
                            iHitStars = (   oItemFoundTemp.iStarsCategory *
                                            oItemFoundTemp.iStarsModel *
                                            oBrand.iStars )
                            #
                            oItemFoundTemp.iHitStars    = iHitStars
                            #
                            oItemFoundTemp.save()
                            #
                            bFoundBrandForModel = True
                            #
                        #
                    #
                #
                if not bFoundBrandForModel:
                    #
                    oItemFoundTemp = ItemFoundTemp(
                            iItemNumb       = oItem,
                            iBrand          = oBrand,
                            iStarsBrand     = oBrand.iStars,
                            iHitStars       = oBrand.iStars,
                            iSearch         = oUserItem.iSearch )
                    #
                    oItemFoundTemp.save()
                    #
                    lItemFoundTemp.append( oItemFoundTemp )
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
                    lSortItems.append( ( lItemFoundTemp[i].iHitStars, i ) )
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
            for oItemFoundTemp in lItemFoundTemp:
                #
                iItemsFoundTemp += 1
                #
                if iItemsFoundTemp == 1:
                    #
                    oUserItem.iBrand        = oItemFoundTemp.iBrand
                    oUserItem.iCategory     = oItemFoundTemp.iCategory
                    oUserItem.iModel        = oItemFoundTemp.iModel
                    #
                    oUserItem.iHitStars     = oItemFoundTemp.iHitStars
                    oUserItem.cWhereCategory= oItemFoundTemp.cWhereCategory
                    # oUserItem.iSearch     = oItemFoundTemp.iSearch
                    #
                    oUserItem.tLook4Hits = tNow
                    #
                    oUserItem.save()
                    #
                    oSearchLog = dSearchLogs.get( oItemFoundTemp.iSearch_id )
                    #
                    if (    oItemFoundTemp.iBrand and
                            oItemFoundTemp.iCategory and
                            oItemFoundTemp.iModel ):
                        #
                        oSearchLog.iItemHits += 1
                        #
                    #
                elif (  oItemFoundTemp.iBrand and
                        oItemFoundTemp.iCategory and
                        oItemFoundTemp.iModel ):
                    #
                    # have complete hit, make an additional UserItem record
                    #
                    tNow = timezone.now()
                    #
                    oNewUserItem = UserItemFound(
                            iItemNumb       = oUserItem.iItemNumb,
                            iHitStars       = oItemFoundTemp.iHitStars,
                            iSearch         = oItemFoundTemp.iSearch,
                            iModel          = oItemFoundTemp.iModel,
                            iBrand          = oItemFoundTemp.iBrand,
                            iCategory       = oItemFoundTemp.iCategory,
                            cWhereCategory  = oItemFoundTemp.cWhereCategory,
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
        if oSearchLog.iItemHits > 0:
            #
            oSearchLog.save()
        #
    #
    if bCleanUpAfterYourself:
        #
        ItemFoundTemp.objects.all().delete()
        #
    #


 
