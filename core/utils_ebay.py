from logging            import getLogger

from String.Find        import getRegExpObj

from .utils             import getWhatsLeft

from brands.models      import Brand
from categories.models  import Category
from models.models      import Model


logger = getLogger(__name__)


_dBlankValue = { None: '', int: 0 }


def getValueOffItemDict( k, dItem, dFields, **kwargs ):
    #
    t = dFields[ k ][ 't' ] # t is for tuple (of keys)
    #
    bOptional = dFields[ k ].get( 'bOptional',  False )
    bCalculate= dFields[ k ].get( 'bCalculate', False )
    #
    bNotInItemDict = bOptional or bCalculate
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
        if bNotInItemDict and t[0] in kwargs:
            #
            uValue  = kwargs[ t[0] ]
            #
        elif bOptional:
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




def _getTitleRegExObj( cTitle, cLookFor = '' ):
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
    return getRegExpObj( sLookFor )


def _getOtherRegExObj( cField ):
    #
    sExcludeIf = cField.strip()
    #
    if sExcludeIf:
        #
        oFinder = getRegExpObj( sExcludeIf )
        #
    else:
        #
        oFinder = None
        #
    return oFinder


def getRegExObjs( cTitle, cLookFor, cExcludeIf, cKeyWords = None ):
    #
    findTitle   = _getTitleRegExObj( cTitle, cLookFor )
    #
    if cExcludeIf:
        #
        findExclude = _getOtherRegExObj( cExcludeIf )
        #
    else:
        #
        findExclude = None
        #
    #
    if cKeyWords:
        #
        findKeyWords = _getOtherRegExObj( cKeyWords  )
        #
    else:
        #
        findKeyWords = None
        #
    #
    return ( findTitle, findExclude, findKeyWords )




def _getTableRegExFinders( oDjModel ):
    #
    if not oDjModel.oRegExLook4Title:
        #
        t = getRegExObjs(
                oDjModel.cTitle,
                oDjModel.cLookFor,
                oDjModel.cExcludeIf,
                oDjModel.cKeyWords )
        #
        findTitle, findExclude, findKeyWords = t
        #
        oDjModel.oRegExLook4Title= findTitle
        oDjModel.oRegExExclude   = findExclude
        oDjModel.oRegExKeyWords  = findKeyWords
        #
        oDjModel.save()
        #
    #
    return (    oDjModel.oRegExLook4Title.search,
                oDjModel.oRegExExclude.search,
                oDjModel.oRegExKeyWords.search )



def getModelRegExFinders( oModel ):
    #
    return _getTableRegExFinders( oModel )



def getCategoryRegExFinders( oCategory ):
    #
    return _getTableRegExFinders( oCategory )




def getBrandRegExFinders( oBrand ):
    #
    if not oBrand.oRegExLook4Title:
        #
        t = getRegExObjs(
                oBrand.cTitle,
                oBrand.cLookFor,
                oBrand.cExcludeIf )
        #
        findTitle, findExclude, findKeyWords = t
        #
        oBrand.oRegExLook4Title= findTitle
        oBrand.oRegExExclude   = findExclude
        #
        oBrand.save()
        #
    #
    return (    oBrand.oRegExLook4Title.search,
                oBrand.oRegExExclude.search )


