from django.db.models       import Q
from django.contrib.auth    import get_user_model
from django.utils           import timezone

from core.user_one          import oUserOne
from core.utils             import getWhatsLeft

from .models                import ItemFound, UserItemFound, ItemFoundTemp

from String.Find            import getRegExpress, getRegExObj
from String.Output          import ReadableNo
from Utils.Progress         import TextMeter, DummyMeter

from searching              import WORD_BOUNDARY_MAX

def _getTitleRegExress( oTableRow, bAddDash = False, bSubModelsOK = False ):
    #
    sLook4Title = getWhatsLeft( oTableRow.cTitle )
    #
    cLookFor = oTableRow.cLookFor
    #
    if cLookFor:
        #
        cLookFor = cLookFor.strip()
        #
        sLookFor = '\r'.join( ( sLook4Title, cLookFor ) )
        #
        sRegExpress = getRegExpress( sLookFor,
                                     bSubModelsOK   = bSubModelsOK,
                                     iWordBoundChrs = WORD_BOUNDARY_MAX )
        
    else:
        #
        sRegExpress = getRegExpress( sLook4Title,
                                     bAddDash       = bAddDash,
                                     bSubModelsOK   = bSubModelsOK,
                                     iWordBoundChrs = WORD_BOUNDARY_MAX )
        #
    #
    return sRegExpress



def _getRowRegExpressions( oTableRow,
                           bAddDash = False, bSubModelsOK = False ):
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
            #print( 'oTableRow   :', oTableRow.cTitle )
            #print( 'sFindTitle  :', sFindTitle )
            #print( 'sFindExclude:', sFindExclude )
            #if bRowHasKeyWords:
                #print( 'sFindKeyWords:', sFindKeyWords)
        #
    #
    return sFindTitle, sFindExclude, sFindKeyWords



def _getRegExSearchOrNone( s ):
    #
    if s:
        oRegExObj = getRegExObj( s )
        #
        return oRegExObj.search


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
        t = tuple( map( _getRegExSearchOrNone, t ) )
        #
        findTitle, findExclude, findKeyWords = t
        #
        def foundItemTester( s ):
            #
            bIncludeThis = _includeNotExclude( s, findExclude )
            #
            return (    findTitle( s ) and
                        bIncludeThis and
                        _gotKeyWordsOrNoKeyWords( s, findKeyWords ),
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



def findSearchHits( iUser = oUserOne.id,
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
    ItemFoundTemp.objects.all().delete()
    #
    qsItems = ItemFound.objects.filter(
                pk__in = UserItemFound.objects
                    .filter( iUser = oUser,
                             tlook4hits__isnull = True )
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
        sLineB4 = 'determining hit stars for items found ...'
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
    for oItem in qsItems:
        #
        iSeq  += 1
        #
        oProgressMeter.update( iSeq )
        #
        oUserItem = UserItemFound.objects.get( 
                iItemNumb   = oItem.iItemNumb,
                iUser       = oUser )
        #
        bGotCategory   = False
        #
        oItemFoundTemp = None
        #
        qsCategories = Category.objects.filter( iUser = oUser )
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
            bInTitle, bExcludeThis = foundItem( oItem.cTitle )
            #
            if bExcludeThis:
                #
                bInHeirarchy1 = bInHeirarchy2 = False
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
                oItemFound = ItemFound.objects.get( pk = oItem.iItemNumb )
                #
                oItemFoundTemp = ItemFoundTemp(
                        iItemNumb       = oItemFound,
                        iHitStars       = oCategory.iStars,
                        iSearch         = oUserItem.iSearch,
                        iCategory       = oCategory,
                        cWhereCategory  = sWhich )
                #
                oItemFoundTemp.save()
                #
            #
        #
        if bExcludeThis: continue
        #
        qsBrands = Brand.objects.filter( iUser = oUser ).order_by( '-iStars' )
        #
        bFoundBrand = False
        #
        for oBrand in qsBrands:
            #
            foundItem = getFoundItemTester( oBrand, dFindersBrands )
            #
            bInTitle, bExcludeThis = foundItem( oItem.cTitle )
            #
            if bInTitle and not bExcludeThis:
                #
                bFoundBrand = True
                #
                if oItemFoundTemp is None:
                    #
                    oItemFoundTemp = ItemFoundTemp(
                            iItemNumb       = oItem,
                            iBrand          = oBrand,
                            iHitStars       = oBrand.iStars,
                            iSearch         = oUserItem.iSearch )
                    #
                    oItemFoundTemp.save()
                    #
                else:
                    #
                    oItemFoundTemp.iHitStars *= oBrand.iStars
                    oItemFoundTemp.iBrand     = oBrand
                    #
                    oItemFoundTemp.save()
                #
                break # maybe keep looking?
                #
            #
        #
        if oItemFoundTemp is None or bExcludeThis: continue
        #
        if bFoundBrand:
            #
            qsModels = ( Model.objects.filter( iUser  = oUser )
                    .filter(
                        Q( bGenericModel = True ) |
                        Q( iBrand        = oBrand ) )
                    .order_by( '-iStars' ) )
            #
        else:
            #
            qsModels = Model.objects.filter(
                    iUser = oUser ).order_by( '-iStars' )
            #
        #
        for oModel in qsModels:
            #
            foundItem = getFoundItemTester( oModel, dFindersModels,
                            bAddDash = True,
                            bSubModelsOK = oModel.bSubModelsOK )
            #
            bInTitle, bExcludeThis = foundItem( oItem.cTitle )
            #
            if bInTitle and not bExcludeThis:
                #
                oItemFoundTemp.iHitStars *= oModel.iStars
                oItemFoundTemp.iModel     = oModel
                #
                oItemFoundTemp.save()
                #
                break
                #
            #
        #
    #
    oProgressMeter.end( iSeq )
    #
    # now update UserItemFound with ItemFoundTemp
    #
    tNow = timezone.now()
    #
    bPrintUserItems = False
    #
    if bShowProgress: # progress meter for running in shell, no need to test
        #
        oProgressMeter = TextMeter()
        #
        print('')
        sLineB4 = 'updating the items found table ...'
        sOnLeft = "%s %s" % ( ReadableNo( iItemsFound ), 'items found' )
        #
        oProgressMeter.start( iItemsFound, sOnLeft, sLineB4 )
        #
    #
    iSeq = 0
    #
    for oItem in qsItems:
        #
        iSeq  += 1
        #
        oProgressMeter.update( iSeq )
        #
        bGotUserItem = UserItemFound.objects.filter(
                            iItemNumb = oItem.pk, iUser = oUser.id ).exists()
        #
        if bGotUserItem:
            #
            oUserItem = UserItemFound.objects.get(
                            iItemNumb = oItem.pk, iUser = oUser.id )
            #
            oUserItem.tlook4hits = tNow
            #
            if ItemFoundTemp.objects.filter( iItemNumb = oItem.pk ).exists():
                #
                oItemFoundTemp = ( ItemFoundTemp.objects
                                    .filter( iItemNumb = oItem.pk )
                                    .order_by( '-iHitStars' ).first() )
                #
                oUserItem.iBrand        = oItemFoundTemp.iBrand
                oUserItem.iCategory     = oItemFoundTemp.iCategory
                oUserItem.iModel        = oItemFoundTemp.iModel
                #
                oUserItem.iHitStars     = oItemFoundTemp.iHitStars
                oUserItem.cWhereCategory= oItemFoundTemp.cWhereCategory
                # oUserItem.iSearch     = oItemFoundTemp.iSearch
                #
            #
            oUserItem.save()
            #
        else:
            #
            logger.error( 'UserItem not found for:', oItem.pk, oItem )
            #
            bPrintUserItems = True
        #
    #
    oProgressMeter.end( iSeq )
    #
    if bPrintUserItems:
        #
        for oUserItem in UserItemFound.objects.all():
            #
            logger.error( oUserItem.pk, oUserItem )
            #
    #
    if bCleanUpAfterYourself:
        #
        ItemFoundTemp.objects.all().delete()
        #
    #


 
