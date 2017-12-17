# misc utils can go here

from django.contrib.auth        import get_user_model

oUser = get_user_model()

oUserOne = oUser.objects.filter( id = 1 ).first()

if not oUserOne:
    #
    '''
    oUser = User()
    #
    oUser.first_name    = 'Rick'
    oUser.last_name     = 'Graves'
    oUser.email         = 'gravesricharde@yahoo.com'
    oUser.username      = 'aardvigator'
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