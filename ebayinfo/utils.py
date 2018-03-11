import xml.etree.ElementTree as ET

#from pprint import pprint

from core.utils             import getNamerSpacer
from django.core.exceptions import ObjectDoesNotExist
from django.db              import DataError

from .models                import Market

from String.Output          import ReadableNo
from Utils.Progress         import TextMeter, DummyMeter
from Web.HTML               import getChars4HtmlCodes

class UnexpectedResponse( Exception ): pass

'''
utils for handling info from ebay API 
note the actual calls to the ebay API are in 
core.ebay_wrapper.py
'''

# variable referenced in tests
sCategoryVersionFile = '/tmp/Categories_Ver_%s.xml'
sCategorylistingFile = '/tmp/Categories_All_%s.xml.gz'

sRootTag = 'GetCategoriesResponse'

sNamerSpacer, sRootNameSpTag = getNamerSpacer( sRootTag,
                sXmlNameSpace = 'urn:ebay:apis:eBLBaseComponents' )


tVersionChildTags = (
    'Timestamp', 'Ack', 'Version', 'Build', 'UpdateTime', 'CategoryVersion' )

tListingChildTags = (
    'Timestamp', 'Ack', 'Version', 'Build', 'UpdateTime', 'CategoryVersion',
    'CategoryCount', )

tCategoryArrayTags = (
    'CategoryID', 'CategoryLevel', 'CategoryName', 'CategoryParentID',
    'LeafCategory' )


def getTagsValuesGotRoot( root, tTags = tVersionChildTags, sFile = None ):
    #
    if root.tag != sRootNameSpTag:
        #
        raise UnexpectedResponse(
            'Check file %s for correct output!' % sFile  )
        #
    #
    dTagsValues = {}
    #
    for sChildTag in tTags:
        #
        try:
            dTagsValues[ sChildTag ] = root.find(
                                        sNamerSpacer % sChildTag ).text
        except AttributeError:
            raise( UnexpectedResponse(
                'Check file %s for tag "%s"!' %
                ( sFile , sChildTag ) ) )
            #
    #
    if dTagsValues[ 'Ack' ] != 'Success':
        raise( UnexpectedResponse(
            'Check file %s for tag "Ack" -- should be "Success"!' % sFile ) )
    #
    return dTagsValues


def getCategoryIterable(
        sFile = sCategorylistingFile % 'EBAY-US', sWantVersion = '117' ):
    #
    tree = ET.parse( sFile )
    #
    root = tree.getroot()
    #
    dTagsValues = getTagsValuesGotRoot(
            root, tTags = tListingChildTags, sFile = sFile )
    #
    if dTagsValues[ 'CategoryVersion' ] != sWantVersion:
        #
        raise( UnexpectedResponse(
            'Check file %s for tag "CategoryVersion" -- should be %s!' %
            ( sFile , sWantVersion ) ) )
        #
    #
    oCategories = root.find( sNamerSpacer % 'CategoryArray' )
    #
    return oCategories.findall( sNamerSpacer % 'Category' ), dTagsValues



def countCategories(
        sFile = sCategorylistingFile % 'EBAY-US', sWantVersion = '117',
        bSayCount = False ):
    #
    from String.Output import ReadableNo
    #
    oCategories, dTagsValues = getCategoryIterable( sFile, sWantVersion )
    #
    i = 0
    #
    for oCategory in oCategories:
        #
        i += 1
        #
    #
    if bSayCount:
        print( 'CategoryCount line said', 
            ReadableNo( dTagsValues[ 'CategoryCount' ] ),
                'categories, actully counted', ReadableNo( i ) )
    #
    return dTagsValues[ 'CategoryCount' ], i



def getCategoryDictGenerator(
        sFile = sCategorylistingFile % 'EBAY-US', sWantVersion = '117' ):
    #
    oCategories, dTagsValues = getCategoryIterable( sFile, sWantVersion )
    #
    for oCategory in oCategories:
        #
        dCategory = {}
        #
        for sAttribute in tCategoryArrayTags:
            #
            oGotAttribute = oCategory.find( sNamerSpacer % sAttribute )
            #
            if oGotAttribute is None:
                sSayAttribute = ''
            else:
                sSayAttribute = oGotAttribute.text
            #
            dCategory[ sAttribute ] = sSayAttribute
            #
        #
        dCategory [ 'CategoryVersion' ] = dTagsValues[ 'CategoryVersion' ]
        #
        yield dCategory


'''
categoryDictIterable = getCategoryDictGenerator()
pprint( next( categoryDictIterable ) )
returns
{'CategoryID': '20081',
 'CategoryLevel': '1',
 'CategoryName': 'Antiques',
 'CategoryParentID': '20081',
 'CategoryVersion': '117',
 'LeafCategory': ''}
'''


def putCategoriesInDatabase( sMarket = 'EBAY-US', sWantVersion = '117',
            bShowProgress = False ):
    #
    from .models import EbayCategory, Market
    #
    oMarket = Market.objects.get( cMarket = sMarket )
    #
    # getCategoryDictGenerator checks for the expected version
    #
    categoryDictIterable = getCategoryDictGenerator(
        sFile = sCategorylistingFile % sMarket, sWantVersion = sWantVersion )
    #
    if bShowProgress: # progress meter for running in shell, no need to test
        #
        oProgressMeter = TextMeter()
        #
        print( 'counting categories ...' )
        #
        iCount = 0
        #
        for dCategory in categoryDictIterable: iCount +=1
        #
        categoryDictIterable = getCategoryDictGenerator(
            sFile = sCategorylistingFile % sMarket,
            sWantVersion = sWantVersion )
        #
        sLineB4 = 'stepping thru ebay categories ...'
        sOnLeft = "%s %s" % ( ReadableNo( iCount ), 'categories' )
        #
        oProgressMeter.start( iCount, sOnLeft, sLineB4 )
        #
    else:
        #
        oProgressMeter = DummyMeter()
        #
    #
    iWantVersion = int( sWantVersion )
    #
    oRootCategory = EbayCategory()
    #
    try: # look for a root category for this market & tree version
        #
        oRootCategory = EbayCategory.objects.get(
            iMarket         = oMarket,
            iTreeVersion    = iWantVersion,
            iCategoryID     = 0 )
        #
    except ObjectDoesNotExist: # if the root is not there yet, put it in
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iMarket         = oMarket,
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
    iSeq = 0
    #
    for dCategory in categoryDictIterable:
        #
        iSeq  += 1
        #
        oProgressMeter.update( iSeq )
        #
        sConfirmVersion = dCategory['CategoryVersion']
        #
        oCategory = EbayCategory()
        #
        try:
            #
            oCategory = EbayCategory.objects.get(
                iMarket         = oMarket, 
                iCategoryID     = int( dCategory['CategoryID'] ) )
            #
        except ObjectDoesNotExist:
            #
            oCategory = EbayCategory(
                iCategoryID     = int( dCategory['CategoryID'] ),
                iMarket         = oMarket )
        #
        sCategoryName = getChars4HtmlCodes( dCategory['CategoryName'] )
        #
        oCategory.name          = sCategoryName
        oCategory.iLevel        = int( dCategory['CategoryLevel'   ] )
        oCategory.bLeafCategory = bool(dCategory['LeafCategory'    ] )
        oCategory.iTreeVersion  = iWantVersion
        oCategory.iParentID     = int( dCategory['CategoryParentID'] )
        #
        if dCategory['CategoryID'] == dCategory['CategoryParentID']:
            #
            # level 1 category, CategoryID == CategoryParentID
            #
            oCategory.parent = oRootCategory
            #
        else:
            #
            oCategory.parent = EbayCategory.objects.get(
                iMarket     = oMarket, 
                iCategoryID = dCategory['CategoryParentID'],
                iTreeVersion= iWantVersion )
            #
        #
        try:
            oCategory.save()
        except DataError:
            raise DataError( 'too long: %s' % sCategoryName )
        #

    #
    oProgressMeter.end( iSeq )
    #
    oMarket.iCategoryVer = int( sWantVersion )
    #
    oMarket.save()





def getCategoryVersionValues( sFile ):
    #
    tree = ET.parse( sFile )
    #
    root = tree.getroot()
    #
    return getTagsValuesGotRoot( root, sFile = sFile )



def getCategoryVersion( sMarket = 'EBAY-US', sFile = sCategoryVersionFile ):
    #
    '''get the version from a file already downloaded'''
    #
    dTagsValues = getCategoryVersionValues( sFile % sMarket )
    #
    return dTagsValues[ 'CategoryVersion' ]


'''
['id',
 'cMarket',
 'cCountry',
 'cLanguage',
 'iEbaySiteID',
 'bHasCategories',
 'iCategoryVer',
 'cCurrencyDef',
 'cUseCategoryID',
 'iUtcPlusOrMinus']
'''

def getMarketsIntoDatabase():
    #
    from ebayinfo           import sMarketsTable # in __init__.py
    #
    from core.utils_testing import getTableFromScreenCaptureGenerator
    #
    from .models            import Market
    #
    from Utils.Config       import getBoolOffYesNoTrueFalse as getBool
    #
    oTableIter = getTableFromScreenCaptureGenerator( sMarketsTable )
    #
    lHeader = next( oTableIter )
    #
    for lParts in oTableIter:
        #
        oMarket = Market(
                    id              = int(      lParts[0] ),
                    cMarket         =           lParts[1],
                    cCountry        =           lParts[2],
                    cLanguage       =           lParts[3],
                    iEbaySiteID     = int(      lParts[4] ),
                    bHasCategories  = getBool(  lParts[5] ),
                    cCurrencyDef    =           lParts[7],
                    iUtcPlusOrMinus = int(      lParts[9] ) )
        #
        if lParts[6]:
            oMarket.iCategoryVer    = int(      lParts[6] )
        #
        if lParts[8]:
            oMarket.cUseCategoryID  =           lParts[8]
        #
        oMarket.save()
        


def getDictMarket2SiteID():
    #
    dMarket2SiteID = {}
    #
    for oMarket in Market.objects.all():
        #
        dMarket2SiteID[ oMarket.cMarket ] = oMarket.iEbaySiteID
        #
    #
    return dMarket2SiteID



def _getDictMarket2ID():
    #
    dMarket2ID = {}
    #
    for oMarket in Market.objects.all():
        #
        dMarket2ID[ oMarket.cMarket ] = oMarket.id
        #
    #
    return dMarket2ID


dMarket2ID = _getDictMarket2ID()