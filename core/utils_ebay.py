from logging        import getLogger

from String.Find    import getRegExpFinder

from .utils         import getWhatsLeft


logger = getLogger(__name__)


_dBlankValue = { None: '', int: 0 }

def getValueOffItemDict( k, dItem, dFields, **kwargs ):
    #
    t = dFields[ k ][ 't' ] # t is for tuple (of keys)
    #
    bOptional = dFields[ k ].get( 'bOptional', False )
    #
    f = dFields[ k ].get( 'f' ) # f is for function
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
    except KeyError as e:
        #
        if bOptional:
            #
            uValue = _dBlankValue.get( f )
            #
        else:
            #
            logger.error( 'KeyError', 'field:', t[0], str(e) )
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
        except ValueError as e:
            #
            logger.error( 'ValueError', 'field:', k, str(e) )
            #
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


def _getTitleFinder( cTitle, cLookFor = '' ):
    #
    sLook4Title = getWhatsLeft( cTitle )
    #
    cLookFor = cLookFor.strip()
    #
    if cLookFor:
        #
        sLookFor = '\r'.join( ( sLook4Title, cLookFor ) )
        #
    else:
        #
        sLookFor = sLook4Title
        #
    #
    return getRegExpFinder( sLookFor )


def _getOtherFinder( cField ):
    #
    sExcludeIf = cField.strip()
    #
    if sExcludeIf:
        #
        oFinder = getRegExpFinder( sExcludeIf )
        #
    else:
        #
        oFinder = None
        #
    return oFinder


def getFinders( cTitle, cLookFor, cExcludeIf, cKeyWords = None ):
    #
    findTitle   = _getTitleFinder( cTitle, cLookFor )
    #
    if cExcludeIf:
        #
        findExclude = _getOtherFinder( cExcludeIf )
        #
    else:
        #
        findExclude = None
        #
    #
    if cKeyWords:
        #
        findKeyWords = _getOtherFinder( cKeyWords  )
        #
    else:
        #
        findKeyWords = None
        #
    #
    return ( findTitle, findExclude, findKeyWords )

