from logging        import getLogger

logger = getLogger(__name__)


_dBlankValue = { None: '', int: 0 }

def getValueOffItemDict( k, dItem, dFields, **kwargs ):
    #
    t = dFields[ k ][ 't' ]
    #
    bOptional = dFields[ k ].get( 'bOptional', False )
    #
    f = dFields[ k ].get( 'f' )
    #
    try:
        #
        uValue  = dItem[ t[0] ]
        #
        tRest   = t[ 1 : ]
        #
        for sKey in tRest:
            uValue = uValue[ sKey ]
        #
    except KeyError:
        #
        if bOptional:
            #
            uValue = _dBlankValue.get( f )
            #
        else:
            #
            raise
            #
        #
    #
    sValue  = uValue
    #
    if f is None:
        #
        uReturn = sValue
        #
    else:
        #
        try:
            #
            uReturn = f( sValue )
            #
        except ValueError:
            #
            print( '\n', 'field:', k, '\n' )
            raise
        #
    #
    return uReturn




def storeEbayInfo( dItem, dFields, Form, getValue, **kwargs ):
    #
    '''can store a row in either ItemFound or UserItemFound'''
    #
    dNewResult = kwargs
    #
    dNewResult.update( { k: getValue( k, dItem, dFields, **kwargs ) for k in dFields } )
    #
    #if 'iSearch' in dNewResult:
        #print( "dNewResult['iSearch']:", dNewResult['iSearch'] )
    #
    form = Form( data = dNewResult )
    #
    if form.is_valid():
        #
        form.save()
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
    
