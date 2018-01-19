# misc utils can go here
from django.db.models           import ForeignKey


#                "2017-12-15T05:22:47.000Z"
EBAY_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'


def getNamerSpacer( sRootTag, sXmlNameSpace = 'urn:ebay:apis:eBLBaseComponents' ):
    #
    '''for extracting values from xml files returned by ebay'''
    #
    sNameSpaceTag   = '{%s}%s'
    #
    sNamerSpacer    = sNameSpaceTag % ( sXmlNameSpace, '%s' )
    #
    sRootNameSpTag  =  sNameSpaceTag % ( sXmlNameSpace, sRootTag )
    #
    return sNamerSpacer, sRootNameSpTag


def getDateTimeObj( sDateTime ):
    #
    '''convert ebay string dates into python datetime objects'''
    #
    from Time.Convert import getDateTimeObjFromString
    #
    #
    return getDateTimeObjFromString( sDateTime, EBAY_DATE_FORMAT )


def getLastDictFromResponse( oResponse ):
    #
    l = oResponse.__dict__['context']
    #
    oLast = l[-1]
    #
    return oLast.dicts[-1]


def getExceptionMessageFromResponse( oResponse ):
    #
    '''
    exception message is burried in the response object,
    here is my struggle to get it out
    '''
    #
    dLast = getLastDictFromResponse( oResponse )
    #
    return dLast.get( 'exception' )


# Iterate over model instance field names and values in template
# https://stackoverflow.com/a/14625776/6366075
def model_to_dict(instance):
    dObj = {}
    for field in instance._meta.fields:
        dObj[field.name] = field.value_from_object(instance)
        if isinstance(field, ForeignKey):
            dObj[field.name] = field.rel.to.objects.get(pk=dObj[field.name])
    return dObj
