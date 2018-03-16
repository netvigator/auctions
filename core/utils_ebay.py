from logging            import getLogger

from String.Find        import getRegExpress, getRegExObj

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




def _getTitleRegExress( oTableRow ):
    #
    sLook4Title = getWhatsLeft( oTableRow.cTitle )
    #
    cLookFor = oTableRow.cLookFor 
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
    return getRegExpress( sLookFor )



def _getRowRegExpressions( oTableRow ):
    #
    bRowHasKeyWords = False
    #
    if not oTableRow.sRegExLook4Title:
        #
        sFindTitle = _getTitleRegExress( oTableRow )
        #
        sKeyWords = sFindKeyWords = sFindExclude = None
        #
        bRowHasKeyWords = hasattr( oTableRow, 'cKeyWords' )
        #
        if bRowHasKeyWords: sKeyWords = oTableRow.cKeyWords
        #
        sExcludeIf = oTableRow.cExcludeIf
        #
        if sExcludeIf:
            #
            sFindExclude = getRegExpress( sExcludeIf )
            #
        if sKeyWords:
            #
            sFindKeyWords = getRegExpress( sKeyWords )
            #
        #
        oTableRow.sRegExLook4Title= sFindTitle
        oTableRow.sRegExExclude   = sFindExclude
        #
        if bRowHasKeyWords:
            oTableRow.sRegExKeyWords = sFindKeyWords
        #
        oTableRow.save()
        #
    #
    return sFindTitle, sFindExclude, sFindKeyWords



def _getRegExSearchOrNone( s ):
    #
    if s:
        oRegExObj = getRegExObj( s )
        #
        return oRegExObj.search


def _getModelRegExFinders4Test( oModel ):
    #
    t = _getRowRegExpressions( oModel )
    #
    return tuple( map( _getRegExSearchOrNone, t ) )


def _getCategoryRegExFinders4Test( oCategory ):
    #
    t = _getRowRegExpressions( oCategory )
    #
    return tuple( map( _getRegExSearchOrNone, t ) )


def _getBrandRegExFinders4Test( oBrand ):
    #
    t = _getRowRegExpressions( oBrand )
    #
    sFindTitle, sFindExclude, sFindKeyWords = t
    #
    return tuple( map( _getRegExSearchOrNone, t[:2] ) )





def _includeNotExclude( s, findExclude ):
    #
    return findExclude is None or not findExclude( s )

def _gotKeyWordsOrNoKeyWords( s, findKeyWords ):
    #
    return findKeyWords is None or findKeyWords( s )


def getFoundItemTester( oTableRow, dFinders ):
    #
    ''' pass model row instance, returns tester '''
    #
    from String.Find import getRegExObj
    #
    if oTableRow.pk in dFinders:
        #
        foundItemTester = dFinders[ oTableRow.pk ]
        #
    else:
        #
        t = _getRowRegExpressions( oTableRow )
        #
        t = tuple( map( _getRegExSearchOrNone, t ) )
        #
        findTitle, findExclude, findKeyWords = t
        #
        def foundItemTester( s ):
            #
            return    ( findTitle( s ) and
                        _includeNotExclude( s, findExclude ) and
                        _gotKeyWordsOrNoKeyWords( s, findKeyWords ) )
        #
        dFinders[ oTableRow.pk ] = foundItemTester
        #
    #
    return foundItemTester
