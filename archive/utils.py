import logging

from archive            import dItemFields as dFields # in __init__.py

from core.utils_ebay    import getValueOffItemDict

from Time.Output        import getNowIsoDateTimeFileNameSafe

from pprint import pprint


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
    #
    return dGotItem




