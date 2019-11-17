from logging            import getLogger

from brands.models      import Brand
from categories.models  import Category
from models.models      import Model


logger = getLogger(__name__)


_dBlankValue = { None: '', int: 0 }


def getValueOffItemDict( dItem, k, dThisField, **kwargs ):
    #
    '''the test has a tester for the dThisField dict, best to use it!'''
    #
    t = dThisField[ 't' ] # t is for tuple (of keys)
    #
    bOptional = dThisField.get( 'bOptional',  False )
    bCalculate= dThisField.get( 'bCalculate', False )
    #
    bNotInItemDict = bOptional or bCalculate
    #
    f = dThisField.get( 'f' ) # f is for function
    #
    uValue = None
    #
    if not t: # empty, IndexError
        #
        pass
        #
    elif t[0] in dItem:
        #
        uValue  = dItem[ t[0] ]
        #
        tRest   = t[ 1 : ]
        #
        if bOptional and tRest and not tRest[0] in uValue:
            #
            uValue = None
            #
        else:
            #
            for sKey in tRest:
                uValue = uValue[ sKey ]
            #
        #
    elif bNotInItemDict and t[0] in kwargs:
        #
        uValue  = kwargs[ t[0] ]
        #
    elif bNotInItemDict and bOptional: # form will accept None
        #
        # 2019-02-10 had this condition on top of the if tests
        # BIG MISTAKE, all optional field data was dropped !!!!
        # I had moved it up for some reason ????
        # don't do that again !!!
        #
        pass
        #
    elif bNotInItemDict:
        #
        uValue = _dBlankValue.get( f )
        #
    elif bOptional: # got Celery error for missing GalleryURL
        #
        pass
        #
    else:
        #
        sMsg = 'expecting key but did not find in info from ebay'
        #
        logger.error( 'KeyError, field * %s * -- %s' % ( t[0], sMsg ) )
        #
    #
    sValue  = uValue
    #
    if sValue is None or isinstance( sValue, bool ):
        #
        uReturn = sValue
        #
    elif f is None:
        #
        uReturn = str( sValue )
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


