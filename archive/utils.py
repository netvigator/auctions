import logging

from os.path                import join
from time                   import sleep

from django.conf            import settings
from django.utils           import timezone

from core.ebay_api_calls    import getSingleItem

# in __init__.py
from archive                import EBAY_ITEMS_FOLDER, dItemFields as dFields

from .forms                 import ItemForm
from .models                import Item

from core.utils             import getDownloadFileWriteToDisk
from core.utils_ebay        import getValueOffItemDict

from searching.models       import ItemFound, UserItemFound

from Dir.Get                import getMakeDir
from File.Test              import isFileThere
from File.Write             import QuietDump
from Time.Test              import isDateTimeObj
from Time.Output            import getNowIsoDateTimeFileNameSafe
from Web.Test               import isURL


class GetSingleItemNotWorkingError(  Exception ): pass
class InvalidOrNonExistentItemError( Exception ): pass


logger = logging.getLogger(__name__)

logging_level = logging.INFO

getMakeDir( EBAY_ITEMS_FOLDER )

ITEM_PICS_ROOT = join( settings.MEDIA_ROOT, 'Item_Pictures' )

getMakeDir( ITEM_PICS_ROOT )


def _writeResult( sContent, sFilePathName ):
    #
    QuietDump( sContent, sFilePathName )


def _getJsonSingleItemResponse( iItemNumb, sContent ):
    #
    '''pass in the response
    returns the resonse dictionary dResponse
    which includes dPagination for convenience'''
    #
    from json           import loads
    #
    from Dict.Maintain  import getDictValuesFromSingleElementLists
    #
    dResult = loads( sContent ) # this is for strings
    #
    dErrors = dResult.get( 'Errors', [{}] )[0]
    #
    if ( "Ack" in dResult and dResult.get( "Ack" ) == "Success" ):
        #
        pass # OK
        #
    else:
        #
        if (    "Ack" in dResult and
                dResult.get( "Ack" ) == "Failure" and
                dErrors and
                dErrors.get( 'ErrorCode' ) == '10.12' ):
            #
            # 'LongMessage': 'Invalid or non-existent item ID.'
            #
            raise InvalidOrNonExistentItemError( str( iItemNumb ) )
            #
        elif "Ack" in dResult:
            #
            sFile = join( EBAY_ITEMS_FOLDER,
                          'single_item_response_failure_%s_%s_.json'
                            % ( getNowIsoDateTimeFileNameSafe(), iItemNumb ) )
            #
            sMsg = ( 'getSingleItem failure, check file %s'
                    % sFile )
            #
            logger.info( sMsg )
            #
            _writeResult( repr( dResult ), sFile )
            #
            raise GetSingleItemNotWorkingError( sMsg )
            #
        else:
            #
            # unexpected content
            #
            sFile = join( EBAY_ITEMS_FOLDER,
                          'invalid_single_item_response_%s_%s_.json'
                            % ( getNowIsoDateTimeFileNameSafe(), iItemNumb ) )
            #
            sMsg = ( 'unexpected content from getSingleItem, check %s'
                    % sFile )
            #
            logger.error( sMsg )
            #
            _writeResult( repr( dResult ), sFile )
            #
            raise GetSingleItemNotWorkingError( sMsg )
            #
        #
    #
    dItem = dResult.get( "Item" )
    #
    return dItem



def _storeJsonSingleItemResponse( iItemNumb, sContent, **kwargs ):
    #
    '''
    gets single item result from ebay API (can pass response for testing)
    stores response in items but does NOT store in itemsfound or useritemsfound
    '''
    #
    if 'tNow' in kwargs:
        tNow = kwargs.pop( 'tNow' )
    else:
        tNow = timezone.now()
    #
    dItem    = _getJsonSingleItemResponse( iItemNumb, sContent )
    #
    dGotItem = { k: getValueOffItemDict( dItem, k, v, **kwargs )
                for k, v in dFields.items() }
    #
    iSavedRowID = sListingStatus = None
    #
    if dGotItem and Item.objects.filter( pk = iItemNumb ).exists():
        #
        bAnyChanged = False
        #
        iSavedRowID = dGotItem['iItemNumb']
        #
        oItem = Item.objects.get( pk = iSavedRowID )
        #
        for sField in dGotItem:
            #
            sValTable  = getattr( oItem, sField )
            #
            sValImport = dGotItem[ sField ]
            #
            if (    ( sValTable or sValImport ) and
                      sValTable != sValImport ):
                #
                setattr( oItem, sField, sValImport )
                #
                bAnyChanged = True
                #
            #
        #
        if bAnyChanged:
            #
            oItem.tModify = tNow
            #
            oItem.save()
            #
        #
        sListingStatus = oItem.cListingStatus
        #
    elif dGotItem:
        #
        form = ItemForm( data = dGotItem )
        #
        if form.is_valid():
            #
            oItemInstance = form.save()
            #
            iSavedRowID = oItemInstance.pk
            #
            sListingStatus = oItemInstance.cListingStatus
        else:
            #
            # ### form errors are common,
            # ### not all real categories are in the test database
            #
            # print( 'dNewResult["iCategoryID"]:', dNewResult['iCategoryID'] )
            sMsg = ('form did not save' )
            #
            logger.error( sMsg )
            #print( '' )
            #print( 'log this error, form did not save' )
            #
            if form.errors:
                for k, v in form.errors.items():
                    logger.warning( '%s -- %s' % ( k, str(v) ) )
                    # print( k, ' -- ', str(v) )
            else:
                logger.info( 'no form errors at bottom!' )
            #
            #tProblems = ( 'iItemNumb', 'cMarket', 'iCategoryID', 'cCategory',
                        #'iCatHeirarchy', 'i2ndCategoryID', 'c2ndCategory',
                        #'i2ndCatHeirarchy', 'cCountry' )
            ##
            #print( '' )
            #print( 'fields with errors:' )
            #for sField in tProblems:
                #print( 'dNewResult["%s"]:' % sField, dNewResult.get( sField ) )
            #
        #
    #
    return iSavedRowID, sListingStatus



def getSingleItemThenStore( iItemNumb, **kwargs ):
    #
    '''
    gets single item result from ebay API (can pass response for testing)
    stores response in items, itemsfound and useritemsfound
    '''
    #
    sContent = iSavedRowID = sListingStatus = None
    #
    bItemNumberStillGood = True
    #
    if 'sContent' in kwargs: # passed for testing
        #
        sContent = kwargs.pop( 'sContent' )
        #
    else:
        #
        try:
            #
            sContent = getSingleItem( iItemNumb )
            #
        except Exception as e:
            #
            logger.info(
                    'Exception for %s', str( iItemNumb ), exc_info = e )
            #
        #
    #
    if 'tNow' in kwargs:
        tNow = kwargs.pop( 'tNow' )
    else:
        tNow = timezone.now()
    #
    if sContent is not None:
        #
        try:
            #
            t = _storeJsonSingleItemResponse(
                        iItemNumb, sContent, tNow = tNow )
            #
            iSavedRowID, sListingStatus = t
            #
        except InvalidOrNonExistentItemError:
            #
            bItemNumberStillGood = False
            #
        #
    #
    if iSavedRowID is not None or not bItemNumberStillGood:
        #
        # InvalidOrNonExistentItemError:
        #
        oItemFound = ItemFound.objects.get( pk = iItemNumb )
        #
        if sListingStatus is not None:
            #
            oItemFound.cSellingState = sListingStatus
            #
        #
        if (    oItemFound.tTimeEnd and
                oItemFound.tTimeEnd < tNow and
                sListingStatus and
                sListingStatus != 'Active' ):
            #
            oItemFound.tRetrieveFinal = tNow
            #
            if oItemFound.tRetrieved:
                #
                bAlreadyRetrieved = True
                #
            else:
                #
                oItemFound.tRetrieved = tNow
                #
                bAlreadyRetrieved = False
                #
            #
            oItemFound.bCancelledItem = not bItemNumberStillGood
            #
            oItemFound.save()
            #
            # next: queryset update method
            #
            if bAlreadyRetrieved:
                #
                UserItemFound.objects.filter(
                        iItemNumb = iItemNumb ).update(
                                tRetrieveFinal = tNow )
                #
            else:
                #
                UserItemFound.objects.filter(
                        iItemNumb = iItemNumb ).update(
                                tRetrieveFinal = tNow,
                                tRetrieved     = tNow )
            #
        elif not oItemFound.tRetrieved:
            #
            oItemFound.tRetrieved = tNow
            #
            if not bItemNumberStillGood:
                #
                oItemFound.tRetrieveFinal = tNow
                #
            #
            oItemFound.save()
            #
            # next: queryset update method
            #
            if bItemNumberStillGood:
                #
                UserItemFound.objects.filter(
                        iItemNumb = iItemNumb ).update( tRetrieved = tNow )
                #
            else:
                #
                UserItemFound.objects.filter(
                        iItemNumb = iItemNumb ).update(
                                tRetrieveFinal = tNow,
                                tRetrieved     = tNow )
                #
            #
        #
    #


def getItemsFoundForUpdate():
    #
    # preliminary job:
    # do this before fetching single item results
    # item could have been fetched for another user
    # so step thru itemsfound, mark all useritemsfound
    # that have been fetched already
    #
    # code is here so it can be tested separately
    #
    # select useritemsfound that have not been marked as fetched yet
    #
    qsUserItemNumbs = ( UserItemFound.objects.filter(
                                bGetPictures        = True,
                                tRetrieved__isnull  = True )
                            .values_list( 'iItemNumb', flat = True )
                            .distinct() )
    #
    # for those item numbers, select itemsfound that have been fetched already
    #
    qsAlreadyFetched = ( ItemFound.objects
                            .filter( iItemNumb__in = qsUserItemNumbs )
                            .filter( tRetrieved__isnull = False )
                            .prefetch_related(
                                    'tRetrieved', 'tRetrieveFinal' ) )
    #
    # update useritemsfound, step thru selected itemsfound,
    # mark useritemsfound that have results fetched already
    #
    for oItemFound in qsAlreadyFetched:
        #
        qsUserItemFound = UserItemFound.filter(
                                iItemNumb = oItemFound.iItemNumb )
        #
        for oUserItemFound in qsUserItemFound:
            #
            oUserItemFound.tRetrieved     = oItemFound.tRetrieved
            oUserItemFound.tRetrieveFinal = oItemFound.tRetrieveFinal
            #
            oUserItemFound.save()
            #
        #
    #
    # for the useritemsfound that have not been marked as fetched yet,
    # select itemsfound for which we have final results
    #
    qsAlreadyFinal = ( ItemFound.objects
                            .filter( iItemNumb__in = qsUserItemNumbs )
                            .filter( tRetrieveFinal__isnull = False )
                            .prefetch_related( 'tRetrieveFinal' ) )
    #
    # update useritemsfound, step thru itemsfound,
    # mark useritemsfound for which we have final results
    #
    for oItemFound in qsAlreadyFinal:
        #
        qsUserItemFound = UserItemFound.filter(
                                iItemNumb = oItemFound.iItemNumb )
        #
        for oUserItemFound in qsUserItemFound:
            #
            oUserItemFound.tRetrieveFinal = oItemFound.tRetrieveFinal
            #
            oUserItemFound.save()
            #
        #
    #
    if qsAlreadyFetched.exists() or qsAlreadyFinal.exists():
        #
        # select useritemsfound for which we need to fetch results
        #
        qsUserItemNumbs = ( UserItemFound.objects.filter(
                                    bGetPictures        = True,
                                    tRetrieved__isnull  = True )
                                .values_list( 'iItemNumb', flat = True )
                                .distinct() )
        #
    #
    return qsUserItemNumbs



def _getPicExtension( sURL ):
    #
    from Web.Address import getFilePathNameOffURL
    #
    sPathNameExtn = getFilePathNameOffURL( sURL )
    #
    sNameExtn = sExtn = ''
    #
    if len( sPathNameExtn ) >= 2:
        #
        sNameExtn = sPathNameExtn[ -1 ]
        #
    #
    lNameExtn = sNameExtn.split( '.' )
    #
    if len( lNameExtn ) >= 2:
        #
        sExtn = lNameExtn[ -1 ]
        #
    #
    return sExtn.lower()


def _getItemPicsSubDir( uItemNumb, sItemPicsRoot = ITEM_PICS_ROOT ):
    #
    sItemNumb = str( uItemNumb )
    #
    sItemPicDirectory1st = sItemNumb[     : -10 ]
    #
    sItemPicDirectory2nd = sItemNumb[ -10 : -8 ]
    #
    sItemPicsSubDir      = join( sItemPicsRoot,
                                 sItemPicDirectory1st,
                                 sItemPicDirectory2nd )
    #
    getMakeDir( sItemPicsSubDir )
    #
    return sItemPicsSubDir



def _getPicFileNameExtn( sURL, iItemNumb, iSeq ):
    #
    sExtn = _getPicExtension( sURL ) or 'jpg'
    #
    sNameExt = '%s-%s.%s' % ( iItemNumb, str( iSeq ).zfill( 2 ), sExtn )
    #
    return sNameExt



def _getItemPicture( sURL, iItemNumb, sItemPicsSubDir, iSeq ):
    #
    sNameExt = _getPicFileNameExtn( sURL, iItemNumb, iSeq )
    #
    sFilePathNameExtn = join( sItemPicsSubDir, sNameExt )
    #
    sResult = getDownloadFileWriteToDisk( sURL, sFilePathNameExtn )
    #
    return sResult





def getItemPictures( iItemNumb, sItemPicsRoot = ITEM_PICS_ROOT ):
    #
    oItem = Item.objects.get( iItemNumb = iItemNumb )
    #
    sSubDir = _getItemPicsSubDir( iItemNumb, sItemPicsRoot )
    #
    lWantPics = [ s for s in oItem.cPictureURLs.split() if isURL( s ) ]
    #
    setGotPics = set( [] )
    #
    for iReTries in range( 5 ):
        #
        iSeq = 0
        #
        if iReTries: sleep( 2 )
        #
        for sURL in lWantPics:
            #
            if sURL not in setGotPics:
                #
                if iSeq: sleep( 1 )
                #
                sResult = _getItemPicture( sURL, iItemNumb, sSubDir, iSeq )
                #
                if isFileThere( sSubDir, sResult ):
                    #
                    setGotPics.add( sURL )
                    #
                elif iReTries == 4: # last try
                    #
                    logger.warning( 'cannot get pic from %s, got result: ' % ( sURL, sResult ) )
                    #
                #
            #
        #
        bGotAllPics = len( lWantPics ) == len( setGotPics )
        #
        if bGotAllPics: break
        #
    #
    if bGotAllPics:
        #
        oItem.bGotPictures = True
        #
    #
    oItem.tGotPictures = timezone.now()
    #
    oItem.save()
    #
