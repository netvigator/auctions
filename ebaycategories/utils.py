
class UnexpectedResponse( Exception ): pass

import xml.etree.ElementTree as ET

#from pprint import pprint
from six import print_ as print3

from core.utils import getNamerSpacer

# variable referenced in tests
cCategoryVersionFile = '/tmp/Categories_Version_for_%s.xml'
cCategorylistingFile = '/tmp/Categories_for_%s.xml'

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
    print3( 'CategoryCount line said', 
           ReadableNo( dTagsValues[ 'CategoryCount' ] ),
            'categories, actully counted', ReadableNo( i ) )


def getCategoryDicts(
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



def getCategoryVersionValues( sFile ):
    #
    tree = ET.parse( sFile )
    #
    root = tree.getroot()
    #
    return getTagsValuesGotRoot( root )



def getCategoryVersion( sMarket = 'EBAY-US', sFile = cCategoryVersionFile ):
    #
    dTagsValues = getCategoryVersionValues( sFile % sMarket )
    #
    return dTagsValues[ 'CategoryVersion' ]

# pprint( getCategoryVersion() )


