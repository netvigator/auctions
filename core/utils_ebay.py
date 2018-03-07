from logging            import getLogger

from String.Find        import getRegExpFinder

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



def getModelFinders( iModelID ):
    #
    oModel = Model.objects.get( pk = iModelID )
    #
    if oModel.oRegExLook4Title is None or oModel.oRegExLook4Title == '':
        #
        t = getFinders(
                oModel.cTitle,
                oModel.cLookFor,
                oModel.cExcludeIf,
                oModel.cKeyWords )
        #
        findTitle, findExclude, findKeyWords = t
        #
        oModel.oRegExLook4Title= findTitle
        oModel.oRegExKeyWords  = findKeyWords
        oModel.oRegExExclude   = findExclude
        #
        oModel.save()
        
    #
    return (    oModel.oRegExLook4Title,
                oModel.oRegExKeyWords,
                oModel.oRegExExclude )



def getCategoryFinders( iCategoryID ):
    #
    oCategory = Category.objects.get( pk = iCategoryID )
    #
    if oCategory.oRegExLook4Title is None or oCategory.oRegExLook4Title == '':
        #
        t = getFinders(
                oCategory.cTitle,
                oCategory.cLookFor,
                oCategory.cExcludeIf,
                oCategory.cKeyWords )
        #
        findTitle, findExclude, findKeyWords = t
        #
        oCategory.oRegExLook4Title= findTitle
        oCategory.oRegExKeyWords  = findKeyWords
        oCategory.oRegExExclude   = findExclude
        #
        oCategory.save()
        
    #
    return (    oCategory.oRegExLook4Title,
                oCategory.oRegExKeyWords,
                oCategory.oRegExExclude )



def getBrandFinders( iBrandID ):
    #
    oBrand = Brand.objects.get( pk = iBrandID )
    #
    if oBrand.oRegExLook4Title is None or oBrand.oRegExLook4Title == '':
        #
        t = getFinders(
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
    return (    oBrand.oRegExLook4Title,
                oBrand.oRegExExclude )


