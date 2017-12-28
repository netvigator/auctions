# misc utils can go here

from django.contrib.auth        import get_user_model

oUser = get_user_model()

oUserOne = oUser.objects.filter( id = 1 ).first()

#                "2017-12-15T05:22:47.000Z"
EBAY_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'

if not oUserOne:
    #
    '''
    oUser = User()
    #
    oUser.first_name    = 'Rick'
    oUser.last_name     = 'Graves'
    oUser.email         = 'gravesricharde@yahoo.com'
    oUser.username      = 'netvigator'
    oUser.password      = 'tba'
    #
    oUser.save()
    #
    oUserOne = oUser
    '''
    oUserOne = get_user_model().objects.create_user(
        'netvigator',
        email           = 'gravesricharde@yahoo.com',
        password        = None,
        first_name      = 'Rick',
        last_name       = 'Graves', )


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


def getExceptionMessageFromResponse( oResponse ):
    #
    '''tested in brands.tests.py'''
    #
    l = oResponse.__dict__['context']
    #
    lLast = l[-1]
    #
    dLast = lLast.dicts[-1]
    #
    return dLast.get( 'exception' )

