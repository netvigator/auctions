import logging

from os.path                import join
from time                   import sleep

from django.conf            import settings
from django.utils           import timezone

from core.ebay_api_calls    import getSingleItem
from core.utils             import getPriorDateTime

# in __init__.py
from keepers            import EBAY_ITEMS_FOLDER, dItemFields as dFields

from .forms             import KeeperForm
from .models            import Keeper, KeeperImage

from core.utils         import getDownloadFileWriteToDisk
from core.utils_ebay    import getValueOffItemDict

from searching.models   import ItemFound, UserItemFound

from Dir.Get            import getMakeDir
from File.Test          import isFileThere
from File.Write         import QuietDump
from String.Find        import getRegExObj
from String.Output      import StrPadZero
from Time.Test          import isDateTimeObj
from Time.Output        import getNowIsoDateTimeFileNameSafe
from Web.Test           import isURL

class GetSingleItemNotWorkingError(  Exception ): pass
class InvalidOrNonExistentItemError( Exception ): pass


logger = logging.getLogger(__name__)

logging_level = logging.INFO

getMakeDir( EBAY_ITEMS_FOLDER )

ITEM_PICS_ROOT = join( settings.MEDIA_ROOT, 'Keeper_Pictures' )

getMakeDir( ITEM_PICS_ROOT )


oErrObj = getRegExObj(
            r'^(?:ProtocolError|ConnectionError|ConnectionResetError)' )

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
    stores response in keepers but NOT in itemsfound or useritemsfound
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
    # temporary work around, ebay glitch 2018-12-14,
    # ebay returning CustomCode as country code for Serbia (instead of RS)
    #
    # made more general 2019-01-21 cuz getting more items from Serbian seller
    #
    if dGotItem['cCountry'] == 'CustomCode':
        #
        # print( '%s:' % dGotItem['iItemNumb'], dGotItem['cLocation'] )
        #
        if dGotItem['cLocation'] in ( 'Ritopek', 'Belgrade' ):
            #
            dGotItem['cCountry'] = 'RS'
            #
        #
    #
    oItemFound = None # testing without an ItemFound
    #
    qsItemFound = ItemFound.objects.filter( pk = iItemNumb )
    #
    if qsItemFound: oItemFound = qsItemFound[0]
    #
    if oItemFound:
        dGotItem['iShippingType'] = oItemFound.iShippingType
    #
    if dGotItem and Keeper.objects.filter( pk = iItemNumb ).exists():
        #
        bAnyChanged = False
        #
        iSavedRowID = dGotItem['iItemNumb']
        #
        oItemKeep = Keeper.objects.get( pk = iSavedRowID )
        #
        for sField in dGotItem:
            #
            sValTable  = getattr( oItemKeep, sField )
            #
            sValImport = dGotItem[ sField ]
            #
            if (    ( sValTable or sValImport ) and
                      sValTable != sValImport ):
                #
                setattr( oItemKeep, sField, sValImport )
                #
                bAnyChanged = True
                #
            #
        #
        if bAnyChanged:
            #
            oItemKeep.tModify = tNow
            #
            oItemKeep.save()
            #
        #
        sListingStatus = oItemKeep.cListingStatus
        #
    elif dGotItem:
        #
        form = KeeperForm( data = dGotItem )
        #
        if form.is_valid():
            #
            oItemKeepInstance = form.save()
            #
            iSavedRowID = oItemKeepInstance.pk
            #
            sListingStatus = oItemKeepInstance.cListingStatus
            #
        else:
            #
            # ### form errors are common,
            # ### not all real categories are in the test database
            #
            # print( 'dNewResult["iCategoryID"]:', dNewResult['iCategoryID'] )
            sMsg = 'in keepers: form did not save, item %s' % dGotItem['iItemNumb']
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
    return iSavedRowID, sListingStatus, oItemFound



def getSingleItemThenStore( iItemNumb, **kwargs ):
    #
    '''
    gets single item result from ebay API (can pass response for testing)
    stores response in items, itemsfound and useritemsfound
    '''
    #
    sContent = iSavedRowID = sListingStatus = oItemFound = None
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
                    'Exception for %s (%s)', str( iItemNumb ), exc_info = e )
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
            iSavedRowID, sListingStatus, oItemFound = t
            #
        except InvalidOrNonExistentItemError:
            #
            bItemNumberStillGood = False
            #
        #
        #
    #
    if oItemFound is None:
        #
        if not settings.TESTING:
            #
            logger.info( 'oItemFound is None! %s', str( iItemNumb ) )
            #
        #
    elif iSavedRowID is not None or not bItemNumberStillGood:
        #
        # InvalidOrNonExistentItemError:
        # 2018-08-08 DoesNotExist: ItemFound matching query does not exist.
        #
        # oItemFound = ItemFound.objects.get( pk = iItemNumb )
        #
        # moved to _storeJsonSingleItemResponse() 2019.03.06
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
            # next: queryset update method
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
            # next: queryset update method
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


def getItemPicsSubDir( uItemNumb, sItemPicsRoot = ITEM_PICS_ROOT ):
    #
    sItemNumb = str( uItemNumb )
    #
    sItemPicDirectory1st = StrPadZero( sItemNumb[     : -10 ], 2 )
    #
    sItemPicDirectory2nd = StrPadZero( sItemNumb[ -10 :  -8 ], 2 )
    #
    sItemPicDirectory3rd = StrPadZero( sItemNumb[  -8 :  -6 ], 2 )
    #
    sItemPicDirectory4th = StrPadZero( sItemNumb[  -6 :  -4 ], 2 )
    #
    sItemPicsSubDir      = join( sItemPicsRoot,
                                 sItemPicDirectory1st,
                                 sItemPicDirectory2nd,
                                 sItemPicDirectory3rd,
                                 sItemPicDirectory4th )
    #
    getMakeDir( sItemPicsSubDir )
    #
    return sItemPicsSubDir



def _getPicFileNameExtn( sURL, iItemNumb, iSeq, sExtn = None ):
    #
    if sExtn is None: sExtn = _getPicExtension( sURL ) or 'jpg'
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


def movePicsLower():
    #
    '''now putting pics deeper, move existing pics'''
    #
    from os         import listdir, rename
    from os.path    import isfile, join
    #
    lTopDirs = listdir( ITEM_PICS_ROOT )
    #
    for sTopDir in lTopDirs:
        #
        sTopDirFullPath = join( ITEM_PICS_ROOT, sTopDir )
        #
        for s2ndTier in listdir( sTopDirFullPath ):
            #
            s2ndTierFullPath = join( sTopDirFullPath, s2ndTier )
            #
            if isfile( s2ndTierFullPath ): continue # should be dir only
            #
            for s3rdTier in listdir( s2ndTierFullPath ):
                #
                s3rdTierFullPath = join( s2ndTierFullPath, s3rdTier )
                #
                if not isfile( s3rdTierFullPath ): continue # only want files
                #
                sItemNumb = s3rdTier.split('-')[0]
                #
                sSubDir = getItemPicsSubDir( sItemNumb, ITEM_PICS_ROOT )
                #
                sWantMoved = join( sSubDir, s3rdTier )
                #
                rename( s3rdTierFullPath, sWantMoved )
                #
            #
        #
    #









def getItemPictures( iItemNumb, sItemPicsRoot = ITEM_PICS_ROOT ):
    #
    oItem = Keeper.objects.get( iItemNumb = iItemNumb )
    #
    sSubDir = getItemPicsSubDir( iItemNumb, sItemPicsRoot )
    #
    lWantPics = [ s for s in oItem.cPictureURLs.split() if isURL( s ) ]
    #
    dGotPics = { s : None for s in lWantPics }
    #
    for iReTries in range( 5 ):
        #
        iSeq = 0
        #
        if iReTries: sleep( 2 )
        #
        for sURL in lWantPics:
            #
            # need to catch:
            # cannot get pic from <URL>,
            # got result: responsecode=404,responsemessage=Not Found
            #
            if dGotPics[ sURL ] not in ( 'success', 'Not Found' ):
                #
                if iSeq: sleep( 1 )
                #
                sResult = _getItemPicture( sURL, iItemNumb, sSubDir, iSeq )
                #
                if 'responsecode' in sResult and 'responsemessage' in sResult:
                    #
                    if 'Not Found' in sResult:
                        #
                        dGotPics[ sURL ] = 'Not Found' # can quit trying
                        #
                    #
                elif isFileThere( sSubDir, sResult ):
                    #
                    dGotPics[ sURL ] = 'success'
                    #
                elif iReTries == 4: # last try
                    #
                    logger.warning(
                        'cannot get pic from %s, got result: %s' %
                        ( sURL, sResult ) )
                    #
                elif oErrObj.search( sResult ):
                    #
                    # ProtocolError|ConnectionError|ConnectionResetError
                    #
                    pass # try again
                    #
                #
            #
            iSeq += 1
            #
        #
        bGotAllPics = len( lWantPics ) == len( dGotPics )
        #
        if bGotAllPics: break
        #
    #
    if bGotAllPics:
        #
        oItem.bGotPictures = True
        #
    #
    oItem.iGotPictures = len( dGotPics )
    #
    oItem.tGotPictures = timezone.now()
    #
    oItem.save()
    #


def getItemsForPicsDownloading( iLimit = 50 ):
    #
    qsGetPics = Keeper.objects.filter(
                    tGotPictures__isnull = True
                    ).order_by( 'tTimeEnd'
                    ).values_list( 'iItemNumb', flat = True
                    )[ : iLimit ]
    #
    return qsGetPics



def deleteKeeperUserItem( uItemNumb, oUser ):
    #
    from glob       import glob
    from os         import listdir, remove
    from os.path    import isfile, join
    #
    sItemNumb = str( uItemNumb )
    iItemNumb = int( uItemNumb )
    #
    tYesterday = getPriorDateTime( iDaysAgo = 1 )
    #
    bTooNewToDelete = False
    #
    qsItem = ItemFound.objects.filter( iItemNumb = iItemNumb )
    #
    if qsItem:
        #
        bTooNewToDelete = qsItem[0].tTimeEnd >= tYesterday
        #
    #
    qsDumpThese = UserItemFound.objects.filter(
                    iItemNumb = iItemNumb, iUser = oUser )
    #
    print( 'len( qsDumpThese ):', len( qsDumpThese ) )
    #
    sSubDir = getItemPicsSubDir( sItemNumb, ITEM_PICS_ROOT )
    #
    sFileSpec = '%s*' % join( sSubDir, sItemNumb )
    #
    print( 'sFileSpec:', sFileSpec )
    #
    lFiles = glob( sFileSpec )
    #
    #
    print( 'found %s files for item %s' % ( len( lFiles ), iItemNumb ) )
    #
    if bTooNewToDelete:
        #
        print( 'too early to delete UserItem:', iItemNumb )
        #
    #
    qsOtherUsersForThis = UserItemFound.objects.filter(
                iItemNumb = iItemNumb, bListExclude = False ).exclude(
                iUser     = oUser)
    #
    if qsOtherUsersForThis:
        #
        print( 'got other user who wants item %s' % iItemNumb )
        #
        # pass # keep the pictures and ItemFound row
        #
    else:
        #
        if lFiles:
            #
            lFiles.sort()
            #
            for sFile in lFiles:
                #
                print( 'would delete %s' % sFile )
                #
                # remove( sFile )
                #
            #
            print( 'KeeperImage.objects.filter(' )
            print( '        iItemNumb = iItemNumb, iUser = oUser ).delete()' )
            #
            # KeeperImage.objects.filter(
            #         iItemNumb = iItemNumb, iUser = oUser ).delete()
            #
        #
        if bTooNewToDelete:
            #
            # next: queryset update method
            # next: queryset update method
            # next: queryset update method
            #
            print( 'too new to delete, instead would call queryset '
                   'update method setting bListExclude to True' )
            #
            # UserItemFound.objects.filter(
            #     iItemNumb = iItemNumb, iUser = oUser
            #         ).update( bListExclude = True )
            #
        else:
            #
            print( 'ItemFound.objects.filter( iItemNumb = iItemNumb ).delete()' )
            #
            # ItemFound.objects.filter( iItemNumb = iItemNumb ).delete()
            #
            print( 'UserItemFound.objects.filter(' )
            print( '    iItemNumb = iItemNumb, iUser = oUser ).delete()' )
            #
            # UserItemFound.objects.filter(
            #    iItemNumb = iItemNumb, iUser = oUser ).delete()
            #
        #
        print( 'Keeper.objects.filter( iItemNumb = iItemNumb ).delete()' )
        #
        # Keeper.objects.filter( iItemNumb = iItemNumb ).delete()
        #




