import logging


from archive            import dItemFields as dFields # in __init__.py
from .forms             import ItemForm
from .models            import Item

from core.utils_ebay    import getValueOffItemDict

from Time.Test          import isDateTimeObj
from Time.Output        import getNowIsoDateTimeFileNameSafe




class GetSingleItemNotWorkingError( Exception ): pass

logger = logging.getLogger(__name__)

logging_level = logging.INFO





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
            sFile = ( '/tmp/single_item_response_failure_%s_.json'
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
            sFile = (   '/tmp/invalid_single_item_response_%s_.json'
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



def storeJsonSingleItemResponse( sContent, **kwargs ):
    #
    dItem    = _getJsonSingleItemResponse( sContent )
    #
    dGotItem = { k: getValueOffItemDict( dItem, k, v, **kwargs )
                 for k, v in dFields.items() }
    #
    bAnyChanged = False
    #
    if Item.objects.filter( pk = dGotItem['iItemNumb'] ).exists():
        #
        iSavedRowID = dGotItem['iItemNumb']
        #
        oItem = Item.objects.get( pk = dGotItem['iItemNumb'] )
        #
        form = ItemForm( instance = oItem )
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




