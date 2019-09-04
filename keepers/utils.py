import logging

from glob                   import glob
from json                   import loads
from os                     import listdir, remove
from os.path                import isfile, join
from time                   import sleep

from django.conf            import settings
from django.utils           import timezone

from core.ebay_api_calls    import getSingleItem
from core.utils             import getPriorDateTime

# in __init__.py
from keepers                import EBAY_ITEMS_FOLDER, dItemFields as dFields

from .forms                 import KeeperForm
from .models                import Keeper, UserKeeper, KeeperImage

from core.utils             import getDownloadFileWriteToDisk
from core.utils_ebay        import getValueOffItemDict

from finders.models         import ItemFound, UserItemFound

from pyPks.Dict.Maintain    import getDictValuesFromSingleElementLists
from pyPks.Dir.Get          import getMakeDir
from pyPks.File.Test        import isFileThere
from pyPks.File.Write       import QuietDump
from pyPks.String.Find      import getRegExObj
from pyPks.String.Output    import StrPadZero
from pyPks.Time.Test        import isDateTimeObj
from pyPks.Time.Output      import getNowIsoDateTimeFileNameSafe
from pyPks.Web.Address      import getFilePathNameOffURL
from pyPks.Web.Test         import isURL

class GetSingleItemNotWorkingError(  Exception ): pass
class InvalidOrNonExistentItemError( Exception ): pass


logger = logging.getLogger(__name__)

logging_level = logging.INFO

if settings.TESTING: # logging during tests
    errorLogger = logger.info # does not output to screen during tests
    ITEM_PICS_ROOT = '/tmp/pictures_test_directory'
else:
    errorLogger = logger.error # outputs to screen during tests
    ITEM_PICS_ROOT = join( settings.MEDIA_ROOT, 'Keeper_Pictures' )

getMakeDir( EBAY_ITEMS_FOLDER )



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
            errorLogger( sMsg )
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



def _storeOneJsonItemInKeepers( iItemNumb, sContent, **kwargs ):
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
            errorLogger( sMsg )
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




def _makeUserKeeperRow( oUserFinder ):
    #
    qsAlreadyGotUserKeeper = UserKeeper.objects.filter(
            iItemNumb_id= oUserFinder.iItemNumb_id,
            iUser       = oUserFinder.iUser,
            iModel      = oUserFinder.iModel,
            iBrand      = oUserFinder.iBrand )
    #
    if not qsAlreadyGotUserKeeper:
        #
        oNewUserKeeper = UserKeeper()
        #
        for oField in oUserFinder._meta.fields:
            #
            if oField.name == 'iItemNumb':
                #
                oNewUserKeeper.iItemNumb_id = oUserFinder.iItemNumb_id
                #
            else:
                #
                setattr( oNewUserKeeper,
                        oField.name,
                        getattr( oUserFinder, oField.name ) )
                #
            #
        #
        oNewUserKeeper.save()
        #
    #



def getSingleItemThenStore( iItemNumb, **kwargs ):
    #
    '''
    gets single item result from ebay API (can pass response for testing)
    stores response in keepers, userkeepers, itemsfound and useritemsfound
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
            t = _storeOneJsonItemInKeepers(
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
    if not bItemNumberStillGood: # this item was purged for some reason
        #
        # InvalidOrNonExistentItemError:
        # 2018-08-08 DoesNotExist: ItemFound matching query does not exist.
        #
        # next: queryset update method
        # next: queryset update method
        # next: queryset update method
        #
        ItemFound.objects.filter(
                iItemNumb = iItemNumb ).update(
                    tRetrieveFinal = tNow,
                    bCancelledItem = True )
        #
        UserItemFound.objects.filter(
                iItemNumb = iItemNumb ).update(
                        tRetrieveFinal = tNow,
                        tRetrieved     = tNow )
        #
    elif oItemFound is None:
        #
        if not settings.TESTING:
            #
            logger.info( 'oItemFound is None! %s', str( iItemNumb ) )
            #
        #
    elif iSavedRowID is not None:
        #
        # oItemFound = ItemFound.objects.get( pk = iItemNumb )
        #
        # moved to _storeOneJsonItemInKeepers() 2019.03.06
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
            oItemFound.bCancelledItem = False
            #
            oItemFound.save()
            #
            # next: queryset update method
            # next: queryset update method
            # next: queryset update method
            #
            # below is commented cuz tRetrieveFinal & tRetrieved
            # no longer stored in UserKeeper
            #
            if bAlreadyRetrieved:
                #
                UserItemFound.objects.filter(
                        iItemNumb = iItemNumb ).update(
                                tRetrieveFinal = tNow )
                #
                # UserKeeper.objects.filter(
                #         iItemNumb = iItemNumb ).update(
                #                 tRetrieveFinal = tNow )
                #
            else:
                #
                UserItemFound.objects.filter(
                        iItemNumb = iItemNumb ).update(
                                tRetrieveFinal = tNow,
                                tRetrieved     = tNow )
                #
                # UserKeeper.objects.filter(
                #         iItemNumb = iItemNumb ).update(
                #                 tRetrieveFinal = tNow,
                #                 tRetrieved     = tNow )
                #
            #
        elif not oItemFound.tRetrieved:
            #
            oItemFound.tRetrieved = tNow
            #
            oItemFound.save()
            #
            # next: queryset update method
            # next: queryset update method
            # next: queryset update method
            #
            UserItemFound.objects.filter(
                    iItemNumb = iItemNumb ).update( tRetrieved = tNow )
            #
        #
        qsUserItems = UserItemFound.objects.filter( iItemNumb = iItemNumb )
        #
        for oUserFinder in qsUserItems:
            #
            _makeUserKeeperRow( oUserFinder )
            #
        #
    #


def getFindersForResultsFetching():
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
                            .filter( tRetrieved__isnull = False ) )
    #
    # update useritemsfound, step thru selected itemsfound,
    # mark useritemsfound that have results fetched already
    #
    for oItemFound in qsAlreadyFetched:
        #
        qsUserItemFound = UserItemFound.objects.filter(
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
                            .filter( iItemNumb__in = qsUserItemNumbs,
                                     tRetrieveFinal__isnull = False ) )
    #
    # update useritemsfound, step thru itemsfound,
    # mark useritemsfound for which we have final results
    #
    for oItemFound in qsAlreadyFinal:
        #
        qsUserItemFound = UserItemFound.objects.filter(
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
    # if qsAlreadyFetched.exists() or qsAlreadyFinal.exists():
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


# one off change 2019-03-08 or thereabouts
#def movePicsLower():
#    #
#    '''now putting pics deeper, move existing pics'''
#    #
#    from os         import listdir, rename
#    from os.path    import isfile, join
#    #
#    lTopDirs = listdir( ITEM_PICS_ROOT )
#    #
#    for sTopDir in lTopDirs:
#        #
#        sTopDirFullPath = join( ITEM_PICS_ROOT, sTopDir )
#        #
#        for s2ndTier in listdir( sTopDirFullPath ):
#            #
#            s2ndTierFullPath = join( sTopDirFullPath, s2ndTier )
#            #
#            if isfile( s2ndTierFullPath ): continue # should be dir only
#            #
#            for s3rdTier in listdir( s2ndTierFullPath ):
#                #
#                s3rdTierFullPath = join( s2ndTierFullPath, s3rdTier )
#                #
#                if not isfile( s3rdTierFullPath ): continue # only want files
#                #
#                sItemNumb = s3rdTier.split('-')[0]
#                #
#                sSubDir = getItemPicsSubDir( sItemNumb, ITEM_PICS_ROOT )
#                #
#                sWantMoved = join( sSubDir, s3rdTier )
#                #
#                rename( s3rdTierFullPath, sWantMoved )
#                #
#            #
#        #
#    #









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
    qsDumpThese = UserKeeper.objects.filter(
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
    print( 'found %s files for item %s' % ( len( lFiles ), sItemNumb ) )
    #
    if bTooNewToDelete:
        #
        print( 'too early to delete UserItem:', iItemNumb )
        #
    #
    qsAllUsersForThis = UserKeeper.objects.filter(
                iItemNumb = iItemNumb )
    #
    print( 'got %s user(s) in keepers who want item %s' %
            ( len( qsAllUsersForThis ), iItemNumb ) )
    #
    qsOtherUsersForThis = UserKeeper.objects.filter(
                iItemNumb = iItemNumb ).exclude(
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
            # UserKeeper.objects.filter(
            #     iItemNumb = iItemNumb, iUser = oUser
            #         ).update( bListExclude = True )
            #
        else:
            #
            print( 'ItemFound.objects.filter( iItemNumb = iItemNumb ).delete()' )
            #
            # ItemFound.objects.filter( iItemNumb = iItemNumb ).delete()
            #
            print( 'UserKeeper.objects.filter(' )
            print( '    iItemNumb = iItemNumb, iUser = oUser ).delete()' )
            #
            # UserKeeper.objects.filter(
            #    iItemNumb = iItemNumb, iUser = oUser ).delete()
            #
        #
        print( 'Keeper.objects.filter( iItemNumb = iItemNumb ).delete()' )
        #
        # Keeper.objects.filter( iItemNumb = iItemNumb ).delete()
        #



def makeUserKeeperRows():
    #
    lKeeperNumbs = ( Keeper.objects.all().values_list(
                        'iItemNumb', flat = True ) )
    #
    qsNotDoneYet = UserItemFound.objects.filter(
            tRetrieveFinal__isnull = False,
            tPutInKeepers__isnull  = True,
            iItemNumb__in = ( lKeeperNumbs ) )
    #
    for oUserFinder in qsNotDoneYet:
        #
        _makeUserKeeperRow( oUserFinder )
        #
        oUserFinder.tPutInKeepers = timezone.now()
        #
        oUserFinder.save()
        #
    #




def findPicsPopulateTable():
    #
    '''I think we want table rows for existing pics'''
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
            for s3rdTier in listdir( s2ndTierFullPath ):
                #
                s3rdTierFullPath = join( s2ndTierFullPath, s3rdTier )
                #
                for s4thTier in listdir( s3rdTierFullPath ):
                    #
                    s4thTierFullPath = join( s3rdTierFullPath, s4thTier )
                    #
                    for s5thTier in listdir( s4thTierFullPath ):
                        #
                        s5thTierFullPath = join( s4thTierFullPath, s5thTier )
                        #
                        if not isfile( s5thTierFullPath ): continue # only want files
                        #
                        sItemNumb = s5thTier.split('-')[0]
                        #
                        iItemNumb = int( sItemNumb )
                        #
                        qsUsers4This = UserKeeper.objects.filter( iItemNumb = iItemNumb )
                        #
                        #


                #
            #
        #
    #
'''
ITEM_PICS_ROOT = '/home/Common/AuctionPics/Keeper_Pictures'
from os         import listdir, rename
from os.path    import isfile, join
from keepers.models import UserKeeper
lTopDirs = listdir( ITEM_PICS_ROOT )
lTopDirs
sTopDir = lTopDirs[0]
sTopDir
sTopDirFullPath = join( ITEM_PICS_ROOT, sTopDir )
sTopDirFullPath
l2ndTier = listdir( sTopDirFullPath )
l2ndTier
s2ndTier = l2ndTier[0]
s2ndTier
s2ndTierFullPath = join( sTopDirFullPath, s2ndTier )
s2ndTierFullPath
l3rdTier = listdir( s2ndTierFullPath )
l3rdTier
s3rdTier = l3rdTier[0]
s3rdTier
s3rdTierFullPath = join( s2ndTierFullPath, s3rdTier )
s3rdTierFullPath
l4thTier = listdir( s3rdTierFullPath )
l4thTier
s4thTier = l4thTier[0]
s4thTier
s4thTierFullPath = join( s3rdTierFullPath, s4thTier )
s4thTierFullPath
l5thTier = listdir( s4thTierFullPath )
l5thTier
s5thTier = l5thTier[0]
s5thTier
s5thTierFullPath = join( s4thTierFullPath, s5thTier )
s5thTierFullPath
isfile( s5thTierFullPath )
sItemNumb = s5thTier.split('-')[0]
sItemNumb
iItemNumb = int( sItemNumb )
iItemNumb
qsUsers4This = UserKeeper.objects.filter( iItemNumb = iItemNumb )
len( qsUsers4This )


def _updateRetrieved():
    #
    for oKeeper in Keeper.objects.all():
        #
        qsUserKeeper = UserKeeper.objects.filter( iItemNumb = oKeeper.iItemNumb )
        #
        if qsUserKeeper:
            #
            oUserKeeper = qsUserKeeper[0]
            #
            oKeeper.tRetrieved      = oUserKeeper.tRetrieved
            oKeeper.tRetrieveFinal  = oUserKeeper.tRetrieveFinal
            #
            oKeeper.save()
'''
