import logging

from glob                   import glob
from json                   import loads, JSONDecodeError
from os                     import listdir, remove, rename, walk
from os.path                import isfile, join
from pytz                   import UTC
from socket                 import timeout
from time                   import sleep

from django.conf            import settings
from django.utils           import timezone

from django.core.wsgi       import get_wsgi_application

application = get_wsgi_application()

from core.ebay_api_calls    import getSingleItem
from core.utils             import getPriorDateTime

# in __init__.py
from keepers                import EBAY_ITEMS_FOLDER, dItemFields as dFields

from .forms                 import KeeperForm
from .models                import Keeper, UserKeeper, KeeperImage

from core.utils             import getDownloadFileWriteToDisk
from core.utils_ebay        import getValueOffItemDict

from finders.models         import ItemFound, UserItemFound, UserFinder

from pyPks.Dict.Maintain    import getDictValuesFromSingleElementLists
from pyPks.Dir.Get          import getMakeDir
from pyPks.File.Test        import isFileThere
from pyPks.File.Write       import QuietDump, openAppendClose
from pyPks.String.Find      import getRegExObj
from pyPks.String.Output    import StrPadZero, ReadableNo
from pyPks.Time.Convert     import getDateTimeObjFromIsoDateStr
from pyPks.Time.Test        import isDateTimeObj
from pyPks.Time.Output      import getNowIsoDateTimeFileNameSafe
from pyPks.Utils.Progress   import TextMeter
from pyPks.Web.Address      import getFilePathNameOffURL
from pyPks.Web.Test         import isURL

class GetSingleItemNotWorkingError(  Exception ): pass
class InvalidOrNonExistentItemError( Exception ): pass


logger = logging.getLogger(__name__)

logging_level = logging.INFO

if settings.TESTING: # logging during tests
    errorLogger = logger.info # does not output to screen during tests
    ITEM_PICS_ROOT = '/tmp/pictures_test_directory'
    getMakeDir( ITEM_PICS_ROOT )
else:
    errorLogger = logger.error # outputs to screen during tests
    ITEM_PICS_ROOT = join( settings.MEDIA_ROOT, 'Keeper_Pictures' )

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
            sMsg = ( 'getSingleItem failure for item %s, check file %s'
                    % ( iItemNumb, sFile ) )
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
            sMsg = ( 'unexpected content from getSingleItem for item %s, check %s'
                    % ( iItemNumb, sFile ) )
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
        if dGotItem['cLocation'] in ( 'Ritopek', 'Belgrade', 'Centa' ):
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
            sMsg = ( 'in keepers: form did not save, item %s\nContent:\n%s' %
                     ( dGotItem['iItemNumb'], sContent ) )
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
            #              'iCat***Heirarchy', 'i2ndCategoryID', 'c2ndCategory',
            #              'i2nd***CatHeirarchy', 'cCountry' )
            #
            #print( '' )
            #print( 'fields with errors:' )
            #for sField in tProblems:
            #    print( 'dNewResult["%s"]:' % sField, dNewResult.get( sField ) )
            #
        #
    #
    return iSavedRowID, sListingStatus, oItemFound




def _makeUserKeeperRow( oUserFinder ):
    #
    qsAlreadyGotUserKeeper = UserKeeper.objects.filter(
            iItemNumb_id    = oUserFinder.iItemNumb_id,
            iUser           = oUserFinder.iUser,
            iModel          = oUserFinder.iModel,
            iBrand          = oUserFinder.iBrand )
    #
    bUpdateUserFinder = False
    #
    if qsAlreadyGotUserKeeper:
        #
        bUpdateUserFinder = not oUserFinder.tPutInKeepers
        #
    else: # not qsAlreadyGotUserKeeper
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
        bUpdateUserFinder = True
        #
    #
    if bUpdateUserFinder:
        #
        oUserFinder.tPutInKeepers = timezone.now()
        #
        oUserFinder.save()
        #
    #



def getSingleItemThenStore( iItemNumb, oAuthToken = None, **kwargs ):
    #
    '''
    gets single item result from ebay API (can pass response for testing)
    stores response in keepers, userkeepers, itemsfound and useritemsfound
    if results have been retrieved, removes the item from user finders

    todo ?:
    ### for useritemsfound and userkeepers, should be user specific !!! ###
    '''
    #
    sContent = iSavedRowID = sListingStatus = oItemFound = None
    #
    bItemNumberStillGood = True
    bGot_503_SkipForNow  = False
    bGot_token_OAuth_app = False
    #
    if 'sContent' in kwargs: # passed for testing
        #
        sContent = kwargs.pop( 'sContent' )
        #
    else:
        #
        try:
            #
            sContent = getSingleItem( iItemNumb, oAuthToken = oAuthToken )
            #
        except timeout as e: # ebay timed out 2020-01-18 & 2020-06-05
            #
            if not e: e = 'no Exception info!' # ebay timed out 2020-01-18
            #
            logger.info(
                    'ebay is slow, timeout for %s (%s)', str( iItemNumb ), str(e) )
            #
        # now getting Exception for 201754968613
        #(('Connection aborted.',
        #   ConnectionResetError(104, 'Connection reset by peer')))
        #[2020-06-05 09:35:29,770: INFO/ForkPoolWorker-1]
        #  oItemFound is None! 201754968613
        #
        except Exception as e:
            #
            if not e: e = 'no Exception info!'
            #
            logger.info(
                    'Exception for %s (%s)', str( iItemNumb ), str(e) )
            #
        #
    #
    if 'tNow' in kwargs:
        tNow = kwargs.pop( 'tNow' )
    else:
        tNow = timezone.now()
    #
    if sContent:
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
        except JSONDecodeError: # 503 service unavailable
            #
            bGot_503_SkipForNow  = True
            #
        except GetSingleItemNotWorkingError: # token issue
            #
            bGot_token_OAuth_app = True
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
        UserFinder.objects.filter(
                iItemNumb = iItemNumb ).delete()
        #
    elif bGot_503_SkipForNow:
        #
        logger.info( 'got JSONDecodeError probably 503 temp problem! %s', str( iItemNumb ) )
        #
    elif bGot_token_OAuth_app:
        #
        logger.info( 'got OATH token error! %s', str( iItemNumb ) )
        #
    elif oItemFound is None:
        #
        if not settings.TESTING:
            #
            logger.info( 'oItemFound is None! %s', str( iItemNumb ) )
            #
        #
    elif iSavedRowID:
        #
        # oItemFound = ItemFound.objects.get( pk = iItemNumb )
        #
        # moved to _storeOneJsonItemInKeepers() 2019.03.06
        #
        if sListingStatus:
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
        UserFinder.objects.filter( iItemNumb_id = iItemNumb ).delete()
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
    # qsUserItemNumbs = ( UserItemFound.objects.filter(
    #                             bGetResult         = True,
    #                             tRetrieved__isnull  = True )
    #                         .values_list( 'iItemNumb', flat = True )
    #                         .distinct() )
    #
    qsUserFinderNumbs = ( UserFinder.objects.filter(
                                bGetResult = True )
                            .values_list( 'iItemNumb', flat = True )
                            .distinct() ) # UserFinder anit got tRetrieved
    #
    # for those item numbers, select itemsfound that have been fetched already
    #
    # qsAlreadyFetched = ( ItemFound.objects
    #                         .filter( iItemNumb__in = qsUserItemNumbs )
    #                         .filter( tRetrieved__isnull = False ) )
    #
    qsAlreadyFetched = ( ItemFound.objects
                            .filter( iItemNumb__in = qsUserFinderNumbs )
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
        qsUserFinder = UserFinder.objects.filter(
                            iItemNumb = oItemFound.iItemNumb ).delete()
        #
    #
    # for the useritemsfound that have not been marked as fetched yet,
    # select itemsfound for which we have final results
    #
    # qsAlreadyFinal = ( ItemFound.objects
    #                         .filter( iItemNumb__in = qsUserItemNumbs,
    #                                  tRetrieveFinal__isnull = False ) )
    #
    qsAlreadyFinal = ( ItemFound.objects
                            .filter( iItemNumb__in = qsUserFinderNumbs,
                                     tRetrieveFinal__isnull = False ) )
    #
    # update useritemsfound, step thru itemsfound,
    # mark useritemsfound for which we have final results
    #
    for oItemFound in qsAlreadyFinal:
        #
        # qsUserItemFound = UserItemFound.objects.filter(
        #                         iItemNumb = oItemFound.iItemNumb )
        #
        # for oUserItemFound in qsUserItemFound:
        #     #
        #     oUserItemFound.tRetrieveFinal = oItemFound.tRetrieveFinal
        #     #
        #     oUserItemFound.save()
        #     #
        #
        qsUserFinder = UserItemFound.objects.filter(
                                iItemNumb = oItemFound.iItemNumb )
        #
        for oUserItemFound in qsUserFinder:
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
    # qsUserItemNumbs = ( UserItemFound.objects.filter(
    #                             bGetResult         = True,
    #                             tRetrieved__isnull  = True )
    #                         .values_list( 'iItemNumb', flat = True )
    #                         .distinct() )
    #
    qsUserFinderNumbs = ( UserFinder.objects.filter(
                                bGetResult = True )
                            .values_list( 'iItemNumb', flat = True )
                            .distinct() ) # UserFinder aint got tRetrieved
    #
    #
    return qsUserFinderNumbs



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




def getPicFileList( uItemNumb, sItemPicsRoot = ITEM_PICS_ROOT ):
    #
    sItemNumb = str( uItemNumb )
    #
    sSubDir = getItemPicsSubDir( sItemNumb, sItemPicsRoot )
    #
    return glob( '%s*' % join( sSubDir, sItemNumb ) )





def gotPicsForItem( uItemNumb, sItemPicsRoot = ITEM_PICS_ROOT ):
    #
    '''
    pass the item number, returns the integer # of pictures we got
    boolean value of 0     is False,
    boolean value of n > 0 is True
    '''
    #
    return len( getPicFileList( uItemNumb, sItemPicsRoot ) )





def _updateKeeperRow( iItemNumb ):
    #
    iGotPictures = gotPicsForItem( iItemNumb )
    #
    bFixed, bNoPics = False, False
    #
    try:
        oItem = Keeper.objects.get( iItemNumb = iItemNumb )
    except Keeper.DoesNotExist:
        pass
    else:
        #
        if oItem.iGotPictures != iGotPictures:
            #
            oItem.iGotPictures = iGotPictures
            oItem.bGotPictures = iGotPictures > 0
            #
            oItem.save()
            #
            bFixed = True
            #
            if iGotPictures == 0:
                #
                bNoPics = True
                #
            #
    #
    return bFixed, bNoPics


def doRestoredPicsUpdate():
    #
    qsGotPics = Keeper.objects.all(
                ).order_by( 'tTimeEnd'
                ).values_list( 'iItemNumb', flat = True )
    #
    oProgressMeter = TextMeter()
    #
    iCount = len( qsGotPics )
    #
    sSayRows = ReadableNo( iCount )
    #
    sLineB4 = 'stepping thru all keepers ...'
    sOnLeft = "%s %s" % ( sSayRows, 'keepers' )
    #
    oProgressMeter.start( iCount, sOnLeft, sLineB4 )
    #
    iSeq = 0
    iFix = 0
    iNoP = 0
    #
    for iItemNumb in qsGotPics:
        #
        iSeq += 1
        #
        bFixed, bNoPics = _updateKeeperRow( iItemNumb )
        #
        if bFixed:  iFix +=1
        #
        if bNoPics: iNoP +=1
        #
        oProgressMeter.update( iSeq )
        #
    #
    oProgressMeter.end( iSeq )
    #
    print( '\nOf %s rows, %s (%s%%) did not have correct picture count' %
           ( sSayRows, ReadableNo( iFix ), 100 * iFix // iCount ) )
    #
    iGotPics = iFix - iNoP
    #
    tSaySplit = ( ReadableNo( iNoP ), ReadableNo( iGotPics ) )
    #
    print( 'among those, %s no pictures were found, '
           'while %s items had pictures' % tSaySplit )


def doMissingPicsSearch():
    #
    tBefore = timezone.now() - timezone.timedelta( days = 92 )
    #
    qsGotPics = Keeper.objects.filter(
                    tGotPictures__isnull = False,
                    tTimeEnd__gt = tBefore,
                    iGotPictures__gt = 0,
                ).order_by( 'tTimeEnd'
                ).values_list( 'iItemNumb', flat = True )
    #
    oProgressMeter = TextMeter()
    #
    iCount = len( qsGotPics )
    #
    sSayRows = ReadableNo( iCount )
    #
    sLineB4 = 'stepping thru recent keepers ...'
    sOnLeft = "%s %s" % ( sSayRows, 'keepers' )
    #
    oProgressMeter.start( iCount, sOnLeft, sLineB4 )
    #
    iSeq = 0
    iFix = 0
    #
    for iItemNumb in qsGotPics:
        #
        iSeq += 1
        #
        if gotPicsForItem( iItemNumb ) > 0: continue
        #
        oItem = Keeper.objects.get( iItemNumb = iItemNumb )
        #
        oItem.iGotPictures = 0
        oItem.bGotPictures = False
        oItem.tGotPictures = None
        #
        oItem.save()
        #
        iFix +=1
        #
        oProgressMeter.update( iSeq )
        #
    #
    oProgressMeter.end( iSeq )
    #
    print( '\nOf %s rows, %s (%s%%) did not actually have any pictures' %
           ( sSayRows, ReadableNo( iFix ), 100 * iFix // iCount ) )




def getItemPictures( iItemNumb, sItemPicsRoot = ITEM_PICS_ROOT ):
    #
    '''downloads & stores pictures for an ebay item'''
    #
    oItem = Keeper.objects.get( iItemNumb = iItemNumb )
    #
    sSubDir = getItemPicsSubDir( iItemNumb, sItemPicsRoot )
    #
    lWantPics = [ s for s in oItem.cPictureURLs.split() if isURL( s ) ]
    #
    dGotPics = { s : None for s in lWantPics }
    #
    bTried2GetAllPics = False
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
                        logger.warning(
                            'sequence %s pic not found for %s, got result: %s' %
                            ( iSeq, iItemNumb, sResult ) )
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
        bTried2GetAllPics = len( lWantPics ) == len( dGotPics )
        #
        if bTried2GetAllPics: break
        #
    #
    iPicsOnDisk = gotPicsForItem( iItemNumb )
    #
    if bTried2GetAllPics:
        #
        oItem.bGotPictures = iPicsOnDisk > 0
        #
    #
    oItem.iGotPictures = iPicsOnDisk
    #
    oItem.tGotPictures = timezone.now()
    #
    oItem.save()
    #


def getItemsForPicsDownloading( iLimit = 50, iTooOldDays = 95 ):
    #
    # bGetPictures = True, not implemented yet
    #
    tTooOld = timezone.now() - timezone.timedelta( iTooOldDays )
    #
    qsGetPics = Keeper.objects.filter(
                    tGotPictures__isnull = True,
                    tTimeEnd__gt         = tTooOld,
                    iBidCount__gt        = 0,
                ).order_by( 'tTimeEnd'
                ).values_list( 'iItemNumb', flat = True
                )[ : iLimit ]
    #
    iWantPics = iLimit / 10
    #
    if iLimit > len( qsGetPics ):
        #
        iWantPics = iLimit - len( qsGetPics )
        #
    #
    # qsZeroBids = Keeper.objects.filter(
    #                 tGotPictures__isnull = True, iBidCount = 0
    #                 ).values_list( 'iItemNumb', flat = True )
    #
    qsZeroBids = Keeper.objects.filter(
                        iBidCount           = 0,
                        tTimeEnd__gt        = tTooOld,
                        cListingType        = 'FixedPriceItem',
                        tGotPictures__isnull= True
                    ).values_list( 'iItemNumb', flat = True
                    )[ : iWantPics ]
    #
    return qsGetPics.union( qsZeroBids )



def _deleteItemPics( uItemNumb ):
    #
    lFiles = getPicFileList( uItemNumb, ITEM_PICS_ROOT )
    #
    if lFiles:
        #
        for sFile in lFiles:
            #
            # print( 'would delete %s' % sFile )
            #
            remove( sFile )
            #
        #
        # next: queryset delete method
        # next: queryset delete method
        # next: queryset delete method
        #
        KeeperImage.objects.filter( iItemNumb = int( uItemNumb ) ).delete()
        #
    #



def deleteKeeperUserItem( uItemNumb, oUser ):
    #
    '''
    delete the userKeepr row now, so user gets instant result (last step)
    finished if any other user wants to keep this one
    if auction is over, delete the keeper row and pictures, hide useritemsfound
    if auction aint over yet, mark keeper row with bDeleteMaybe = True
      dont delete yet cuz later, another user might want to keep that item
    daily or so, after fetching final results,
      query keeper ended auctions for rows marked with bDeleteMaybe = True
      if any found, delete pictures and keeper rows
    '''
    #
    sItemNumb = str( uItemNumb )
    iItemNumb = int( uItemNumb )
    #
    #
    qsOtherUsersForThis = UserKeeper.objects.filter(
                iItemNumb = iItemNumb ).exclude(
                iUser     = oUser)
    #
    if qsOtherUsersForThis:
        #
        # print( 'got other user who wants item %s' % iItemNumb )
        #
        pass # keep the pictures and Keeper row for now
        #
    else:
        #
        #
        tAncientHistory = getPriorDateTime( iDaysAgo = 10 )
        #
        bTooNewToDelete = False
        #
        qsItem = Keeper.objects.filter( iItemNumb = iItemNumb )
        #
        if qsItem:
            #
            bTooNewToDelete = qsItem[0].tTimeEnd >= tAncientHistory
            #
        #
        if bTooNewToDelete:
            #
            # print( 'too early to delete UserItem:', iItemNumb )
            #
            # next: queryset update method
            # next: queryset update method
            # next: queryset update method
            #
            Keeper.objects.filter( iItemNumb = iItemNumb
                                ).update( bDeleteMaybe = True )
            #
        else: # old enough to dump
            #
            _deleteItemPics( uItemNumb )
            #
            # next: queryset update method
            # next: queryset update method
            # next: queryset update method
            #
            UserItemFound.objects.filter(
                iItemNumb = iItemNumb, iUser = oUser
                    ).update( bListExclude = True )
            #
        #
    #
    # print( 'UserKeeper.objects.filter(' )
    # print( '    iItemNumb = iItemNumb, iUser = oUser ).delete()' )
    #
    # next: queryset delete method
    # next: queryset delete method
    # next: queryset delete method
    #
    UserKeeper.objects.filter( iItemNumb = iItemNumb, iUser = oUser ).delete()
    #



def makeUserKeeperRows():
    #
    '''
    this is a utility to fix keepers that
    for some reason do not have any userkeeper row
    implemented Dec 2019
    next step: implement testing to make sure
    newly created keepers have user keeper rows
    '''
    #
    print()
    print( 'counting keepers & user items ...' )
    #
    lKeeperNumbs = ( Keeper.objects.all().values_list(
                        'iItemNumb', flat = True ) )
    #
    #        tRetrieveFinal__isnull = False,
    qsNotDoneYet = UserItemFound.objects.filter(
            tPutInKeepers__isnull  = True,
            iItemNumb__in = lKeeperNumbs )
    #
    oProgressMeter = TextMeter()
    #
    iCount = len( qsNotDoneYet )
    #
    sLineB4 = 'stepping thru User Items Found ...'
    sOnLeft = "%s %s" % ( ReadableNo( iCount ), 'user items' )
    #
    oProgressMeter.start( iCount, sOnLeft, sLineB4 )
    #
    iSeq = 0
    #
    for oUserFinder in qsNotDoneYet:
        #
        iSeq  += 1
        #
        oProgressMeter.update( iSeq )
        #
        _makeUserKeeperRow( oUserFinder )
        #
    #
    oProgressMeter.end( iSeq )
    #




def findPicsPopulateTable():
    #
    '''I think we want table rows for existing pics'''
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

back up plan
1.3G    11
1.2G    12
1.1G    13
1.4G    14

1.9G    15
1.0G    16
2.4G    17

1.7G    18
1.7G    19
975M    20
2.0G    22

1.3G    23
1.4G    25
1.7G    26
1.4G    27

2.4G    28
1.4G    29
1.5G    30

2.1G    31
1.6G    32
1.2G    33
941M    35

235M    36
789M    37
406M    38
477M    39
649M    40
'''


def getOrphanPicsReports( sDateBeg = None, sDateEnd = None ):
    #
    def getDateObj( sDate ):
        #
        return getDateTimeObjFromIsoDateStr( sDate, oTimeZone = UTC )
    #
    def getItemNumberOffFileName( sFile ):
        #
        return sFile.split( '-' )[0]
    #
    def fileWalkGenerator():
        #
        for root, dirs, files in walk( ITEM_PICS_ROOT ):
            #
            for file in files:
                #
                yield root, file
    #
    if sDateBeg is None:
        #
        tDateBeg = getDateObj( '2017-01-01' )
        #
    else:
        #
        tDateBeg = getDateObj( sDateBeg )
        #
    #
    if sDateEnd is None:
        #
        tDateEnd = timezone.now()
        #
    else:
        #
        tDateEnd = getDateObj( sDateEnd )
        #
    #
    qsKeepersGotPics = Keeper.objects.filter(
            tGotPictures__gte = tDateBeg,
            tGotPictures__lte = tDateEnd )
    #
    setKeepersGotPicsRight = set( [] )
    setKeepersGotPicsZero  = set( [] )
    setKeepersGotPicsLess  = set( [] )
    setKeepersGotPicsMore  = set( [] )
    #
    for oItem in qsKeepersGotPics:
        #
        if not oItem.iGotPictures: continue
        #
        iItemNumb = oItem.iItemNumb
        #
        iGotPics = gotPicsForItem( iItemNumb )
        #
        if not iGotPics:
            #
            openAppendClose( sText, *sFileSpec )
            #
            setKeepersGotPicsZero.add( iItemNumb )
            #
        elif iGotPics == oItem.iGotPictures:
            #
            openAppendClose( sText, *sFileSpec )
            #
            setKeepersGotPicsRight.add( iItemNumb )
            #
        elif iGotPics < oItem.iGotPictures:
            #
            openAppendClose( sText, *sFileSpec )
            #
            setKeepersGotPicsLess.add( iItemNumb )
            #
        elif iGotPics > oItem.iGotPictures:
            #
            openAppendClose( sText, *sFileSpec )
            #
            setKeepersGotPicsMore.add( iItemNumb )
            #
        #
    #
    setKeepersGotPicsRight = frozenset( setKeepersGotPicsRight )
    setKeepersGotPicsZero  = frozenset( setKeepersGotPicsZero  )
    setKeepersGotPicsLess  = frozenset( setKeepersGotPicsLess  )
    setKeepersGotPicsMore  = frozenset( setKeepersGotPicsMore  )
    #
    setKeepersGotPics = (   setKeepersGotPicsRight |
                            setKeepersGotPicsLess  |
                            setKeepersGotPicsMore )
    #
    oFilesWalk  = fileWalkGenerator()
    #
    t           = next( oFilesWalk )
    #
    sThisDir, sThisFile = t
    #
    sLastDir    = sThisDir
    #
    setItemsHere= set( [] )
    #
    while sThisFile:
        #
        while sLastDir == sThisDir:
            #
            setItemsHere.add( getItemNumberOffFileName( sThisFile ) )
            #
            sThisDir, sThisFile = next( oFilesWalk )
            #
        #
        for sItemNumb in setItemsHere:
            #
            iItemNumb = int( sItemNumb )
            #
            if iItemNumb in setKeepersGotPics: continue
            #
            qsKeeper = Keepers.objects.filter( iItemNumb = iItemNumb )
            #
            if qsKeeper.exists():
                #
                openAppendClose( sText, *sFileSpec )
                #
            else:
                #
                openAppendClose( sText, *sFileSpec )
                #
            #
        #
        sLastDir        = sThisDir
        setItemsHere    = set( [] )
        #
    #


def update_some_keeper_rows(
        log_file   = '/tmp/got_pics.txt',
        error_file = '/tmp/got_no_pics.txt' ):
    #
    oProgressMeter = TextMeter()
    #
    iCount = sum( 1 for line in open( log_file ) )
    #
    sSayRows = ReadableNo( iCount )
    #
    sLineB4 = 'stepping thru some keepers ...'
    sOnLeft = "%s %s" % ( sSayRows, 'keepers' )
    #
    oProgressMeter.start( iCount, sOnLeft, sLineB4 )
    #
    iSeq = 0
    iFix = 0
    #
    for iItemNumb in open( log_file ):
        #
        iSeq += 1
        #
        if not iItemNumb: continue
        #
        bFixed, bNoPics = _updateKeeperRow( int( iItemNumb ) )
        #
        if bFixed:
            iFix +=1
        else:
            openAppendClose( str( iItemNumb ), error_file )
        #
        oProgressMeter.update( iSeq )
        #
    #
    oProgressMeter.end( iSeq )
    #
    print( '\nOf %s rows, %s (%s%%) did not have correct picture count' %
           ( sSayRows, ReadableNo( iFix ), 100 * iFix // iCount ) )
    #


def move_errant_pics():
    #
    from os                 import walk, rename
    from os.path            import join

    from pyPks.String.Get   import getTextBefore

    # correct_dir = '/srv/big/media/Keeper_Pictures'
    mistake_dir = '/srv/big/media/Keeper_Pictures/Keeper_Pictures'

    setItemIDs = set( () )
    log_file = '/tmp/got_pics.txt'
    #
    for root, dirs, files in walk( mistake_dir ):
        #
        correct_dir = root.replace(
                'Keeper_Pictures/Keeper_Pictures', 'Keeper_Pictures' )
        #
        for file in files:
            #
            correct_file = join( correct_dir, file )
            #
            if isFileThere( correct_file):
                # print( '%s is where is should be' % correct_file )
                pass
            else:
                # print( '%s is NOT where is should be' % correct_file )
                wrong_place = join( root, file )
                # print( 'would move \n%s to \n%s\n' % ( wrong_place, correct_file ) )
                # getMakeDir( correct_dir )
                #
                rename( wrong_place, correct_file )
                #
                item_id = getTextBefore( file, '-' )
                #
                if False and item_id not in setItemIDs:
                    #
                    setItemIDs.add( item_id )
                    print( 'would move pics for item id %s' %  item_id )
                    openAppendClose( item_id, log_file )
                    #
                #
            #
        #


def deleteSomePics( error_file = '/tmp/got_no_pics.txt' ):
    #
    for iItemNumb in open( error_file ):
        #
        if not iItemNumb: continue
        #
        _deleteItemPics( iItemNumb )
