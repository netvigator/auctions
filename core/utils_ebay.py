from logging            import getLogger

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
    except ( IndexError, KeyError ) as e:
        #
        if not t: # empty
            #
            uValue  = None
            #
        elif bNotInItemDict and t[0] in kwargs:
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


