
class UnexpectedResponse( Exception ): pass

import xml.etree.ElementTree as ET

#from pprint import pprint

from core.utils     import getNamerSpacer
from django.core.exceptions import ObjectDoesNotExist
from django.db      import DataError

from String.Output  import ReadableNo
from Utils.Progress import TextMeter, DummyMeter
from Web.HTML       import getChars4HtmlCodes

'''
utils for handling info from ebay API 
note the actual calls to the ebay API are in 
core.ebay_wrapper.py
'''

# variable referenced in tests
cCategoryVersionFile = '/tmp/Categories_Ver_%s.xml'
cCategorylistingFile = '/tmp/Categories_All_%s.xml.gz'

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


def getTagsValuesGotRoot( root, tTags = tVersionChildTags ):
    #
    if root.tag != sRootNameSpTag:
        #
        raise UnexpectedResponse(
            'Check file %s for correct output!' % sFile  )
        #
    #
    dTagsValues = {}
    #
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
            'Check file %s for tag "Ack" -- should be "Success"!' %
            ( sFile , ) ) )
    #
    return dTagsValues


def getCategoryIterable(
        sFile = cCategorylistingFile % 'EBAY-US', sWantVersion = '117' ):
    #
    tree = ET.parse( sFile )
    #
    root = tree.getroot()
    #
    dTagsValues = getTagsValuesGotRoot( root, tTags = tListingChildTags )
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
        sFile = cCategorylistingFile % 'EBAY-US', sWantVersion = '117' ):
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
    print( 'CategoryCount line said', 
           ReadableNo( dTagsValues[ 'CategoryCount' ] ),
            'categories, actully counted', ReadableNo( i ) )


def getCategoryDictGenerator(
        sFile = cCategorylistingFile % 'EBAY-US', sWantVersion = '117' ):
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
    categoryDictIterable = getCategoryDictGenerator(
        sFile = cCategorylistingFile % sMarket, sWantVersion = sWantVersion )
    #
    if bShowProgress:
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
            sFile = cCategorylistingFile % sMarket,
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
        if sConfirmVersion != sWantVersion:
            #
            raise UnexpectedResponse(
                'expecting CategoryVersion "%s", got "%s"!' %
                ( sWantVersion, sConfirmVersion ) )
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
            print( '\ntoo long: %s\n' % sCategoryName )
            oCategory.name  = sCategoryName[:48]
            oCategory.save()
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
    return getTagsValuesGotRoot( root )



def getCategoryVersion( sMarket = 'EBAY-US', sFile = cCategoryVersionFile ):
    #
    '''get the version from a file already downloaded'''
    #
    dTagsValues = getCategoryVersionValues( sFile % sMarket )
    #
    return dTagsValues[ 'CategoryVersion' ]





