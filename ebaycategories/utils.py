
class UnexpectedResponse( Exception ): pass

import xml.etree.ElementTree as ET

# from pprint import pprint

# variable referenced in tests
cCategoryVersionFile = '/tmp/Categories_Version.xml'

tree = ET.parse( cCategoryVersionFile )

root = tree.getroot()

sXmlNameSpace   = 'urn:ebay:apis:eBLBaseComponents'
sRootTag        = 'GetCategoriesResponse'
sNameSpaceTag   = '{%s}%s'

sRootNameSpTag  =  sNameSpaceTag % ( sXmlNameSpace, sRootTag )

tChildTags = ( 'Timestamp', 'Ack', 'Version', 'Build', 'UpdateTime', 'CategoryVersion' )

def getCategoryVersionValues():
    #
    if root.tag != sRootNameSpTag:
        #
        raise UnexpectedResponse(
            'Check file %s for correct output!' % cCategoryVersionFile )
        #
    #
    dTagsValues = {}
    #
    sTagBase = sNameSpaceTag % ( sXmlNameSpace, '%s' )
    #
    for sChildTag in tChildTags:
        #
        try:
            dTagsValues[ sChildTag ] = root.find( sTagBase % sChildTag ).text
        except AttributeError:
            raise( UnexpectedResponse(
                'Check file %s for tag "%s"!' %
                ( cCategoryVersionFile, sChildTag ) ) )
            #
    #
    if dTagsValues[ 'Ack' ] != 'Success':
        raise( UnexpectedResponse(
            'Check file %s for tag "Ack" -- should be "Success"!' %
            ( cCategoryVersionFile, ) ) )
    #
    return dTagsValues



def getCategoryVersion():
    #
    dTagsValues = getCategoryVersionValues()
    #
    return dTagsValues[ 'CategoryVersion' ]

# pprint( getCategoryVersion() )


