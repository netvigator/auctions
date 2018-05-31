from os.path                import join

import logging

from django.utils           import timezone

from core.ebay_api_calls    import getSingleItem

# in __init__.py
from archive                import EBAY_ITEMS_FOLDER, dItemFields as dFields

from .forms                 import ItemForm
from .models                import Item

from core.utils_ebay        import getValueOffItemDict

from searching.models       import ItemFound, UserItemFound

from Dir.Get                import getMakeDir
from Time.Test              import isDateTimeObj
from Time.Output            import getNowIsoDateTimeFileNameSafe



class GetSingleItemNotWorkingError( Exception ): pass

logger = logging.getLogger(__name__)

logging_level = logging.INFO


getMakeDir( EBAY_ITEMS_FOLDER )


def _getJsonSingleItemResponse( sContent ):
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
    if not ( "Ack" in dResult and dResult.get( "Ack" ) == "Success" ):
        #
        if "Ack" in dResult:
            #
            sFile = join( EBAY_ITEMS_FOLDER, 
                          'single_item_response_failure_%s_.json'
                            % getNowIsoDateTimeFileNameSafe() )
            #
            sMsg = ( 'getSingleItem failure, check file %s'
                    % sFile )
            #
            logger.info( sMsg )
            #
            raise GetSingleItemNotWorkingError( sMsg )
            #
        else:
            #
            # unexpected content
            #
            sFile = join( EBAY_ITEMS_FOLDER,
                          'invalid_single_item_response_%s_.json'
                                % getNowIsoDateTimeFileNameSafe() )
            #
            sMsg = ( 'unexpected content from getSingleItem, check %s'
                    % sFile )
            #
            logger.error( sMsg )
            #
            raise GetSingleItemNotWorkingError( sMsg )
            #
        #
    #
    dItem = dResult.get( "Item" )
    #
    return dItem



def _storeJsonSingleItemResponse( sContent, **kwargs ):
    #
    if 'tNow' in kwargs:
        tNow = kwargs.pop( 'tNow' )
    else:
        tNow = timezone.now()
    #
    dItem    = _getJsonSingleItemResponse( sContent )
    #
    dGotItem = { k: getValueOffItemDict( dItem, k, v, **kwargs )
                 for k, v in dFields.items() }
    #
    if Item.objects.filter( pk = dGotItem['iItemNumb'] ).exists():
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
        if bAnyChanged:
            #
            oItem.tModify = tNow
            #
            oItem.save()
            #
        #
    else:
        #
        form = ItemForm( data = dGotItem )
        #
        iSavedRowID = None
        #
        if form.is_valid():
            #
            oItemInstance = form.save()
            #
            iSavedRowID = oItemInstance.pk
            #
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
    return iSavedRowID



def getSingleItemThenStore( iItemNumb, **kwargs ):
    #
    sContent = iSavedRowID = None
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
    if 'tNow' in kwargs:
        tNow = kwargs.pop( 'tNow' )
    else:
        tNow = timezone.now()
    #
    if sContent is not None:
        #
        iSavedRowID = _storeJsonSingleItemResponse( sContent, tNow = tNow )
        #
    #
    if iSavedRowID is not None:
        #
        oItemFound = ItemFound.objects.get( pk = iItemNumb )
        #
        if oItemFound.tTimeEnd < tNow:
            #
            oItemFound.tRetrieveFinal = tNow
            #
            if not oItemFound.tRetrieved:
                #
                oItemFound.tRetrieved = tNow
                #
            #
            oItemFound.save()
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
            oItemFound.save()
            #
            UserItemFound.objects.filter(
                    iItemNumb = iItemNumb ).update( tRetrieved = tNow )
            #
        #
    #

