
class UnexpectedResponse( Exception ): pass

import xml.etree.ElementTree as ET

#from pprint import pprint
from six import print_ as print3

# variable referenced in tests
cCategoryVersionFile = '/tmp/Categories_Version.xml'
cCategorylistingFile = '/tmp/Categories_for_0.txt'

sXmlNameSpace   = 'urn:ebay:apis:eBLBaseComponents'
sRootTag        = 'GetCategoriesResponse'
sNameSpaceTag   = '{%s}%s'
sNamerSpacer    = sNameSpaceTag % ( sXmlNameSpace, '%s' )

sRootNameSpTag  =  sNameSpaceTag % ( sXmlNameSpace, sRootTag )

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


def getCategoryIterable( sFile = cCategorylistingFile, sWantVersion = '117' ):
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



def countCategories( sFile = cCategorylistingFile, sWantVersion = '117' ):
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


def getCategoryDicts( sFile = cCategorylistingFile, sWantVersion = '117' ):
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



def getCategoryVersion( sFile = cCategoryVersionFile ):
    #
    dTagsValues = getCategoryVersionValues( sFile )
    #
    return dTagsValues[ 'CategoryVersion' ]

# pprint( getCategoryVersion() )


