from logging            import getLogger

from core.utils_ebay    import getValueOffItemDict
from ebayinfo.utils     import dMarket2SiteID

from .models            import ItemFound, UserItemFound

logger = getLogger(__name__)

class SearchNotWorkingError( Exception ): pass
class SearchGotZeroResults(  Exception ): pass
class ItemAlreadyInTable(    Exception ): pass




def storeEbayInfo( dItem, dFields, Form, getValue, **kwargs ):
    #
    '''can store a row in either ItemFound or UserItemFound'''
    #
    from ebayinfo.models import CategoryHierarchy
    #
    dNewResult = kwargs
    #
    dNewResult.update( { k: getValue( k, dItem, dFields, **kwargs ) for k in dFields } )
    #
    form = Form( data = dNewResult )
    #
    iSavedRowID = None
    #
    if form.is_valid():
        #
        oForm = form.save()
        #
        iSavedRowID = oForm.pk
        #
    else:
        #
        logger.error( 'log this error, form did not save' )
        #
        if form.errors:
            for k, v in form.errors.items():
                logger.error( k, ' -- ', str(v) )
        else:
            logger.info( 'no form errors at bottom!' )
        #
        bGotHierarchy = CategoryHierarchy.objects.filter( pk = kwargs[ 'iCatHeirarchy' ] ).exists()
        #
    #
    return iSavedRowID



def getSearchResultGenerator( sFile ):
    #
    ''' search saves results to file, this returns an interator to set through
    in __init__.py: sResultFileNamePattern = 'Search_%s_%s_ID_%s.json'
    '''
    #
    from json           import load
    #
    from Dict.Get       import getAnyValue
    from Dict.Maintain  import getDictValuesFromSingleElementLists
    from File.Get       import getFileSpecHereOrThere
    #
    sFile = getFileSpecHereOrThere( sFile )
    #
    dResults = load( open( sFile ) )
    #
    # findItemsAdvancedResponse
    # findItemsByCategoryResponse
    # findItemsByKeywordsResponse
    #
    lResponse = getAnyValue( dResults ) # should be only 1 value to get
    #
    if lResponse is None or len( lResponse ) != 1:
        #
        raise SearchNotWorkingError( 'content of "%s" invalid' % sFile )
        #
    #
    dResponse = lResponse[0]
    #
    if dResponse.get( "ack" ) != ["Success"]:
        #
        sMessage = 'ack returned "%s"' % dResponse[ "ack" ][0]
        #
        raise SearchNotWorkingError( sMessage )
        #
    #
    dPagination = dResponse[ "paginationOutput" ][0]
    #
    # do not apply getDictValuesFromSingleElementLists directly to dResponse!
    #### if the search finds only one item, the function trashes it! ###
    #
    getDictValuesFromSingleElementLists( dPagination )
    #
    iEntries    = int( dPagination[ "totalEntries" ] )
    #
    iPages      = int( dPagination[ "totalPages" ] )
    #
    if iPages > 1:
        #
        # actually iEntries is a minimum, the actual number of entries is more
        #
        iEntries = (
            1 + ( iPages - 1 ) * int( dPagination[ "entriesPerPage" ] ) )
        #
    #
    if not iEntries:
        #
        raise SearchGotZeroResults( "search executed OK but returned no items" )
        #
    #
    dPagination[ "totalEntries" ] = dPagination[ "totalEntries" ]
    #
    dResultDict = dResponse[ "searchResult" ][0]
    #
    iThisItem = 0
    #
    lResults = dResultDict.get('item')
    #
    for dItem in lResults:
        #
        iThisItem += 1
        #
        getDictValuesFromSingleElementLists( dItem )
        #
        dPagination["thisEntry"] = str( iThisItem )
        #
        dItem["paginationOutput"]= dPagination
        #
        yield dItem


def getSearchResults( iSearchID = None ):
    #
    '''sends search request to the ebay API, stores the response in /tmp'''
    #
    from os.path                import join
    #
    from django.contrib.auth    import get_user_model
    #
    from core.ebay_wrapper  import (
                    getItemsByKeyWords, getItemsByCategory, getItemsByBoth )
    #
    from searching          import sResultFileNamePattern
    from .models            import Search
    from ebayinfo.models    import Market
    #
    from File.Write         import QuietDump
    from String.Split       import getWhiteCleaned
    #
    User = get_user_model()
    #
    if iSearchID is None:
        #
        oSearch = Search.objects.filter( iUser_id = 1 ).first()
        #
    else:
        #
        # Two Sccops recommends AGAINST passin objects to async processes
        # instead, only pass json serializable values
        # (integers, floats, strings, lists, tuples and dictionaries)
        # so passing a user object is not good.
        #
        oSearch = Search.objects.get( pk = iSearchID )
        #
    #
    oUser       = User.objects.get( id = oSearch.iUser.id )
    #
    oMarket = Market.objects.get( id = oUser.iMarket_id )
    #
    sMarket = oMarket.cMarket
    #
    sUserName   = oUser.username
    #
    sKeyWords       = getWhiteCleaned( oSearch.cKeyWords )
    iEbayCategory   = oSearch.iEbayCategory
    #
    sFileName       = (
        sResultFileNamePattern % ( sMarket, sUserName, oSearch.id ) )
    #  'Search_%s_%s_ID_%s.json'
    #
    tSearch = ( oSearch.cTitle, str( oSearch.id ) )
    #
    if sKeyWords and iEbayCategory:
        #
        logger.info(
            'executing "%s" search (ID %s) for keywords in category ...' %
            tSearch )
        #
        QuietDump(
            getItemsByBoth( sKeyWords, iEbayCategory, sMarketID = sMarket ),
            sFileName )
        #
    elif sKeyWords:
        #
        logger.info(
            'executing "%s" search (ID %s) for keywords '
            '(in all categories) ...' % tSearch )
        #
        QuietDump(
            getItemsByKeyWords( sKeyWords, sMarketID = sMarket ),
            sFileName )
        #
    elif iEbayCategory:
        #
        logger.info(
            'executing "%s" search (ID %s) in category '
            '(without key words) ...' % tSearch )
        #
        QuietDump(
            getItemsByCategory( iEbayCategory, sMarketID = sMarket ),
            sFileName )
        #
    #
    logger.info(
        'completed without error "%s" search (ID %s)' % tSearch )
    #
    sFileName = join( '/tmp', sFileName )
    #
    return sFileName



'''
oIter = getSearchResultGenerator( sFullFileSpec )




#
sGot = eatFromWithin( 'This is for real (but not yet)', oInParensFinder )
#
'''


def _getValueUserOrOther( k, dItem, dFields, oUser = None, **kwargs ):
    #
    if k == 'iUser':
        return oUser.id
    elif k in kwargs:
        return kwargs[ k ]
    else:
        return getValueOffItemDict( k, dItem, dFields )





def _getCategoryHierarchyID(
            iCategoryID, iEbaySiteID, dEbayCatHierarchies ):
    #
    from ebayinfo.models    import EbayCategory, CategoryHierarchy, Market
    #
    tCategoryID = iCategoryID, iEbaySiteID
    
    if tCategoryID in dEbayCatHierarchies:
        #
        iCatHeirarchy = dEbayCatHierarchies[ tCategoryID ]
        #
        bOkCatHeirarchy = CategoryHierarchy.objects.filter( pk = iCatHeirarchy ).exists()
        #
    elif CategoryHierarchy.objects.filter( 
                            iCategoryID = iCategoryID,
                            iMarket     = iEbaySiteID ).exists():
        #
        iCatHeirarchy = CategoryHierarchy.objects.get(
                            iCategoryID = iCategoryID,
                            iMarket     = iEbaySiteID ).pk
        #
        dEbayCatHierarchies[ tCategoryID ] = iCatHeirarchy
        #
    else:
        #
        oEbayCategory   = EbayCategory.objects.get(
                            iCategoryID = iCategoryID,
                            iMarket     = iEbaySiteID )
        #
        lCatHeirarchy = [ oEbayCategory.name ]
        #
        while oEbayCategory.iLevel > 1:
            #
            oEbayCategory = oEbayCategory.parent
            #
            lCatHeirarchy.append( oEbayCategory.name )
            #
        #
        lCatHeirarchy.reverse()
        #
        sCatHeirarchy = '\r'.join( lCatHeirarchy ) # django uses return, but
        # return only does not work in shell, each line overwrites the prior one
        #
        oCategoryHierarchy = CategoryHierarchy(
                iCategoryID     = iCategoryID,
                iMarket         = Market.objects.get(
                                    iEbaySiteID = iEbaySiteID ),
                cCatHierarchy   = sCatHeirarchy )
        #
        oCategoryHierarchy.save()
        #
        iCatHeirarchy = oCategoryHierarchy.pk
        #
        dEbayCatHierarchies[ tCategoryID ] = iCatHeirarchy
        #
    #
    return iCatHeirarchy



def getEbayCategoryHierarchies( dItem, dEbayCatHierarchies ):
    #
    ''' return the ebay category hierarchy for a search find item category
    that is, this returns the id of the category hierarchy table row
    note:
    1) items can optionally have a secondary category
    2) this function has a side effect, it updates dEbayCatHierarchies
    '''
    #
    from ebayinfo.models    import EbayCategory
    #
    iCategoryID = int( dItem.get( 'primaryCategory' ).get( 'categoryId' ) )
    #
    iEbaySiteID = dMarket2SiteID.get( dItem.get( 'globalId' ) )
    #
    iCatHeirarchy = _getCategoryHierarchyID(
                        iCategoryID, iEbaySiteID, dEbayCatHierarchies )
    #
    s2ndCategoryID = dItem.get( 'secondaryCategory', {} ).get( 'categoryId' )
    #
    if s2ndCategoryID:
        #
        i2ndCategoryID = int( s2ndCategoryID )
        #
        i2ndCatHeirarchy = _getCategoryHierarchyID(
                    i2ndCategoryID, iEbaySiteID, dEbayCatHierarchies )
        #
    else:
        #
        i2ndCatHeirarchy = None
        #
    #
    return iCatHeirarchy, i2ndCatHeirarchy



def storeItemFound( dItem, dEbayCatHierarchies = {} ):
    #
    from .forms         import ItemFoundForm
    #
    from searching      import dItemFoundFields # in __init__.py
    #
    from ebayinfo.models import CategoryHierarchy
    #
    #
    iItemID         = int(            dItem['itemId'  ] )
    iSiteID         = dMarket2SiteID[ dItem['globalId'] ]
    #
    bAlreadyInTable = ItemFound.objects.filter( iItemNumb = iItemID ).exists()
    #
    if bAlreadyInTable:
        #
        raise ItemAlreadyInTable(
                'ItemID %s is already in the ItemFound table' % iItemID )
        #
    #
    iCount = CategoryHierarchy.objects.all().count()
    #
    tCatHeirarchies = getEbayCategoryHierarchies( dItem, dEbayCatHierarchies )
    #
    return storeEbayInfo(
            dItem, dItemFoundFields, ItemFoundForm, getValueOffItemDict,
            iCatHeirarchy   = tCatHeirarchies[0],
            i2ndCatHeirarchy= tCatHeirarchies[1],
            iMarket         = iSiteID )



def storeUserItemFound( dItem, iItemNumb, oUser, iSearch ):
    #
    from .forms     import UserItemFoundForm
    from searching  import dUserItemFoundFields # in __init__.py
    #
    bAlreadyInTable = UserItemFound.objects.filter(
                            iItemNumb   = iItemNumb,
                            iUser       = oUser ).exists()
    #
    if bAlreadyInTable:
        #
        raise ItemAlreadyInTable(
                'ItemFound %s is already in the UserItemFound table for %s' %
                ( iItemNumb, oUser.username ) )
        #
    #
    return storeEbayInfo(
            dItem, dUserItemFoundFields, UserItemFoundForm, _getValueUserOrOther,
            oUser       = oUser,
            iItemNumb   = iItemNumb,
            iSearch     = iSearch )



def doSearchStoreResults( iSearchID = None, sFileName = None ):
    #
    '''put search results in the database
    can do a search, or use the results file from completed ebay API request
    pass Search ID to search ebay via the api, or pass
    a file name to process the results of a prior search'''
    #
    from django.contrib.auth import get_user_model
    #
    from String.Get import getTextBefore
    #
    User = get_user_model()
    #
    if sFileName is None:
        #
        sFileName = getSearchResults( iSearchID )
        #
    #
    # 'Search-%s-%s-ID-%s.json' % ( sMarket, sUserName, oSearch.id ) )
    #
    lParts = sFileName.split( '_' )
    #
    sUserName   =                     lParts[ 2]
    iSearch     = int( getTextBefore( lParts[-1], '.json' ) )
    #
    oUser = User.objects.get( username = sUserName )
    #
    oItemIter = getSearchResultGenerator( sFileName )
    #
    iItems = iStoreItems = iStoreUsers = 0
    #
    dEbayCatHierarchies = {}
    #
    for dItem in oItemIter:
        #
        iItems += 1
        #
        iItemNumb = None
        #
        try:
            iItemNumb = storeItemFound( dItem, dEbayCatHierarchies )
            iStoreItems += 1
        except ItemAlreadyInTable:
            #
            iItemNumb      = int(            dItem['itemId'  ] )
            #
        except ValueError as e:
            #
            logger.error( 'ValueError: %s | %s' %
                          ( str(e), repr(dItem) ) )
        #
        if iItemNumb is not None:
            #
            try:
                storeUserItemFound( dItem, iItemNumb, oUser, iSearch )
                iStoreUsers += 1
            except ItemAlreadyInTable:
                pass
        #
    #
    return iItems, iStoreItems, iStoreUsers



def trySearchCatchExceptions( iSearchID = None, sFileName = None ):
    #
    '''high level script, does a search, catches exceptions, logs errors'''
    #
    iItems = iStoreItems = iStoreUsers = 0
    #
    try:
        iItems, iStoreItems, iStoreUsers = doSearchStoreResults(
                    iSearchID = iSearchID, sFileName = sFileName )
    except SearchNotWorkingError as e:
        logger.error( 'SearchNotWorkingError: %s' % e )
    except SearchGotZeroResults as e:
        logger.error( 'SearchGotZeroResults: %s' % e )
    #
    return iItems, iStoreItems, iStoreUsers 



def _includeNotExclude( s, findExclude ):
    #
    return findExclude is None or not findExclude( s )

def _gotKeyWordsOrNoKeyWords( s, findKeyWords ):
    #
    return findKeyWords is None or findKeyWords( s )

def whichGetsCredit( bInTitle, bInHeirarchy1, bInHeirarchy2 ):
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


def findSearchHits( oUser ):
    #
    from brands.models      import Brand
    from categories.models  import Category
    from models.models      import Model
    #
    from core.utils_ebay    import ( getBrandRegExFinders,
                                     getCategoryRegExFinders,
                                     getModelRegExFinders )
    #
    from .models            import ItemFoundTemp
    #
    ItemFoundTemp.objects.all().delete()
    #
    oItemQuerySet = ItemFound.objects.filter(
                pk__in = UserItemFound.objects
                    .filter( iUser = oUser,
                             tlook4hits__isnull = True )
                    .values_list( 'iItemNumb', flat=True ) )
    #
    #print( '\n' )
    #print( 'len( oItemQuerySet ):', len( oItemQuerySet ) )
    #
    for oItem in oItemQuerySet:
        #
        oUserItem = UserItemFound.objects.get( 
                iItemNumb   = oItem.iItemNumb,
                iUser       = oUser )
        #
        oItemFoundTemp = None
        #
        oCategoryQuerySet = Category.objects.filter( iUser = oUser )
        #
        #print( '\n' )
        #print( 'len( oCategoryQuerySet ):', len( oCategoryQuerySet ) )
        #print( 'oItem.iItemNumb:', oItem.iItemNumb )
        #print( 'oUser:', oUser )
        #
        #
        #
        for oCategory in oCategoryQuerySet:
            #
            t = getCategoryRegExFinders( oCategory )
            #
            findTitle, findExclude, findKeyWords = t
            #
            def foundItem( s ):
                #
                return    ( findTitle( s ) and
                            _includeNotExclude( s, findExclude ) and
                            _gotKeyWordsOrNoKeyWords( s, findKeyWords ) )
            #
            # the following are short circuiting --
            # if one is True, the following will be True
            # and the string will not be searched
            #
            bInTitle       = foundItem( oItem.cTitle )
            #
            bInHeirarchy1  = ( # will be True if bInTitle is True
                    bInTitle or
                    foundItem( oItem.iCatHeirarchy.cCatHierarchy ) )
            #
            bInHeirarchy2  = ( # will be True if either are True
                    bInTitle or
                    bInHeirarchy1 or
                    ( oItem.i2ndCatHeirarchy and
                      foundItem( oItem.i2ndCatHeirarchy.cCatHierarchy ) ) )
            #
            if bInHeirarchy2: # bInTitle or bInHeirarchy1 or bInHeirarchy2
                #
                sWhich = whichGetsCredit(
                            bInTitle, bInHeirarchy1, bInHeirarchy2 )
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
        oBrandQuerySet = Brand.objects.filter(
                iUser = oUser ).order_by( '-iStars' )
        #
        bFoundBrand = False
        #
        for oBrand in oBrandQuerySet:
            #
            t = getBrandRegExFinders( oBrand )
            #
            findTitle, findExclude = t
            #
            def foundItem( s ):
                #
                return    ( findTitle( s ) and
                            _includeNotExclude( s, findExclude ) )
            #
            bInTitle = foundItem( oItem.cTitle )
            #
            if bInTitle:
                #
                bFoundBrand = True
                #
                if oItemFoundTemp is None:
                    #
                    oItemFoundTemp = ItemFoundTemp(
                            iItemNumb       = oItem.iItemNumb,
                            iBrand          = oBrand,
                            iHitStars       = oBrand.iStars,
                            iSearch         = oUserItem.iSearch,
                            iCategory       = oBrand.pk )
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
            #
            break # maybe keep looking?
            #
        #
        if oItemFoundTemp is None: continue
        #
        if bFoundBrand:
            #
            oModelQuerySet = Model.objects.filter(
                    iUser = oUser,
                    iBrand = oBrand ).order_by( '-iStars' )
            #
        else:
            #
            oModelQuerySet = Model.objects.filter(
                    iUser = oUser ).order_by( '-iStars' )
            #
        #
        for oModel in oModelQuerySet:
            #
            t = getModelRegExFinders( oModel )
            #
            findTitle, findExclude, findKeyWords = t
            #
            def foundItem( s ):
                #
                return    ( findTitle( s ) and
                            _includeNotExclude( s, findExclude ) and
                            _gotKeyWordsOrNoKeyWords( s, findKeyWords ) )
            #
            bInTitle = foundItem( oItem.cTitle )
            #
            if bInTitle:
                #
                oItemFoundTemp.iHitStars *= oModel.iStars
                oItemFoundTemp.iModel     = oModel
                #
                oItemFoundTemp.save()
                #
            #
            break
            #
        #
    

    
