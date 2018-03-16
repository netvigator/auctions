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




def _getTitleRegExObj( cTitle, cLookFor = '', bDeBug = False ):
    #
    sLook4Title = getWhatsLeft( cTitle )
    #
    if cLookFor:
        #
        cLookFor = cLookFor.strip()
        #
        sLookFor = '\r'.join( ( sLook4Title, cLookFor ) )
        #
    else:
        #
        sLookFor = sLook4Title
        #
    #
    oRegExObj = getRegExpObj( sLookFor )
    #
    if bDeBug:
        print( 'RegExpObj:', oRegExObj )
    #
    return oRegExObj


def _getOtherRegExObj( cField ):
    #
    sOther = cField.strip()
    #
    if sOther:
        #
        oFinder = getRegExpObj( sOther )
        #
    else:
        #
        oFinder = None
        #
    return oFinder


def getRegExObjs( cTitle, cLookFor, cExcludeIf, cKeyWords = None,
                  bDeBug = False ):
    #
    findTitle   = _getTitleRegExObj( cTitle, cLookFor, bDeBug = bDeBug )
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




def _getTableRegExFinders( oTableRow, bDeBug = False ):
    #
    bRowHasKeyWords = False
    #
    if not oTableRow.oRegExLook4Title:
        #
        bRowHasKeyWords = hasattr( oTableRow, 'cKeyWords' )
        #
        cKeyWords = None
        #
        if bRowHasKeyWords: cKeyWords = oTableRow.cKeyWords
        #
        t = getRegExObjs(
                oTableRow.cTitle,
                oTableRow.cLookFor,
                oTableRow.cExcludeIf,
                          cKeyWords )
        #
        findTitle, findExclude, findKeyWords = t
        #
        oTableRow.oRegExLook4Title= findTitle
        oTableRow.oRegExExclude   = findExclude
        #
        if bRowHasKeyWords:
            oTableRow.oRegExKeyWords = findKeyWords
        #
        oTableRow.save()
        #
    #
    if bDeBug:
        print( 'Title RegExpObj:', oTableRow.oRegExLook4Title )
    #
    oReturnLook4Title = oTableRow.oRegExLook4Title.search
    #
    oReturnExclude = oReturnKeyWords = None
    #
    if oTableRow.oRegExExclude is not None:
        #
        oReturnExclude = oTableRow.oRegExExclude.search
        #
    if bRowHasKeyWords and oTableRow.oRegExKeyWords is not None:
        #
        oReturnKeyWords = oTableRow.oRegExKeyWords.search
        #
    #    
    return oReturnLook4Title, oReturnExclude, oReturnKeyWords



def _getModelRegExFinders4Test( oModel ):
    #
    return _getTableRegExFinders( oModel )


def _getCategoryRegExFinders4Test( oCategory ):
    #
    return _getTableRegExFinders( oCategory )


def _getBrandRegExFinders4Test( oBrand ):
    #
    oReturnLook4Title, oReturnExclude, oReturnKeyWords = _getTableRegExFinders( oBrand )
    #
    return oReturnLook4Title, oReturnExclude





def _includeNotExclude( s, findExclude ):
    #
    return findExclude is None or not findExclude( s )

def _gotKeyWordsOrNoKeyWords( s, findKeyWords ):
    #
    return findKeyWords is None or findKeyWords( s )


def getFoundItemTester( oTableRow, bDeBug = False ):
    #
    ''' pass model row instance, returns tester '''
    #
    findTitle, findExclude, findKeyWords = _getTableRegExFinders(
                                                oTableRow, bDeBug = bDeBug )
    #
    def foundItemTester( s ):
        #
        return    ( findTitle( s ) and
                    _includeNotExclude( s, findExclude ) and
                    _gotKeyWordsOrNoKeyWords( s, findKeyWords ) )
    #
    return foundItemTester
