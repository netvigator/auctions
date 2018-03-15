from django.contrib.auth    import get_user_model
from django.http.request    import HttpRequest
from django.test            import TestCase, RequestFactory
from django.test.client     import Client

# Create your tests here.

from brands.models          import Brand
from categories.models      import Category
from models.models          import Model

from ebayinfo.models        import EbayCategory, Market

def getDefaultMarket():
    
    if (        Market.objects.count() == 0 or
            not Market.objects.filter( pk = 3 ).exists() ):
        #
        market = Market()
        #
        market.cMarket     = 'EBAY-GB'
        market.cCountry    = 'UK'
        market.iEbaySiteID = 3
        market.iCategoryVer= 108
        market.cCurrencyDef= 'GBP'
        market.cLanguage   = 'en-UK'
        market.save()
        #
    else:
        #
        market = Market.objects.get( pk = 0 )
        #
    #
    if (        Market.objects.count() == 0 or
            not Market.objects.filter( pk = 0 ).exists() ):
        #
        market = Market()
        #
        market.cMarket     = 'EBAY-US'
        market.cCountry    = 'US'
        market.iEbaySiteID = 0
        market.iCategoryVer= 117
        market.cCurrencyDef= 'USD'
        market.cLanguage   = 'en-US'
        market.save()
        #
    else:
        #
        market = Market.objects.get( pk = 0 )
        #
    #
    return market

    # print( 'self.market.id:', Market.objects.filter( pk = 1 ) )


def getUrlQueryStringOff( sURL ):
    #
    ''' get URL parts, before and after ? for http query string '''
    #
    lParts = sURL.split('?')
    #
    lParts.append( '' )
    #
    return tuple( lParts )


def queryGotUpdated( s ):
    #
    from String.Get import getTextAfter, getTextBefore
    from Time.Test  import isISOdatetimeFileNameSafe
    #
    sQueryUTC = getTextBefore(
                    getTextAfter( s, 'updated=' ),
                    '&',
                    bWantEmptyIfNoAfter = False )
    #
    return isISOdatetimeFileNameSafe( sQueryUTC )


class getSingleEbayCategoryMixin( object ):
    
    def setUp(self):        
        #
        super( getSingleEbayCategoryMixin, self ).setUp()
        #
        self.ebc = EbayCategory(
            iCategoryID = 10,
            name        = 'hot products',
            iLevel      = 1,
            iParentID   = 1,
            iTreeVersion= 1,
            iMarket     = self.market,
            bLeafCategory = False )
        self.ebc.save()
        #
        self.client = Client()



class BaseUserTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        
        self.market  = getDefaultMarket()

        oUser = get_user_model()

        self.user1 = oUser.objects.create_user('username1', 'email@ymail.com')
        self.user1.set_password( 'mypassword')
        self.user1.first_name   = 'John'
        self.user1.last_name    = 'Citizen'
        self.user1.save()

        self.user2 = oUser.objects.create_user('username2', 'email@gmail.com')
        self.user2.set_password( 'mypassword')
        self.user2.first_name   = 'Joe'
        self.user2.last_name    = 'Blow'
        self.user2.save()
        
        self.user3 = oUser.objects.create_user( 'username3', 'email@hotmail.com' )
        self.user3.set_password( 'mypassword')
        self.user3.first_name   = 'Oscar'
        self.user3.last_name    = 'Zilch'
        self.user3.is_superuser = True
        self.user3.save()
        #
        self.request = HttpRequest()
        self.request.user = self.user1
        #
        if (  ( not isinstance( self.market, Market ) ) or
              ( not Market.objects.get( pk = 0 ) ) ):
            self.market = Market(
                cMarket     = 'EBAY-US',
                cCountry    = 'US',
                iEbaySiteID = 0,
                cLanguage   = 'en-US',
                iCategoryVer= 1,
                cCurrencyDef= 'USD' )
            self.market.save()
        #



class setUpBrandsCategoriesModels( BaseUserTestCase ):
    
    ''' handy base class that sets up some models / tables '''
    
    def setUp(self):
        #
        super( setUpBrandsCategoriesModels, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')
        #
        self.oBrand = Brand(
            cTitle      = "Cadillac",
            cLookFor    = "Caddy",
            cExcludeIf  = 'golf',
            iStars      = 5,
            iUser = self.user1 )
        #
        self.oBrand.save()
        #
        self.oCategory = Category(
            cTitle      = "Widget",
            cKeyWords   = 'Gadget',
            cLookFor    = "Gizmo",
            cExcludeIf  = 'Delta',
            iStars      = 5,
            iUser       = self.user1 )
        self.oCategory.save()
        self.CategoryID = self.oCategory.id
        #
        self.oModel = Model(
            cTitle      = "Fleetwood",
            cLookFor    = "Woodie",
            cKeyWords   = 'Eldorado',
            cExcludeIf  = 'golf',
            iStars      = 5,
            iBrand      = self.oBrand,
            iCategory   = self.oCategory,
            iUser       = self.user1 )
        self.oModel.save()



def setup_view_for_tests( view, request, *args, **kwargs ):
    """
    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to ``reverse()``
    """
    #
    view.request= request
    view.args   = args
    view.kwargs = kwargs
    #
    return view



def getTableFromScreenCaptureGenerator( sScreenCapture ):
    #
    from .utils import getSeqStripped
    #
    lLines = sScreenCapture.split( '\n' )
    #
    lHeader = []
    #
    for sLine in lLines:
        #
        lParts = list( getSeqStripped( sLine.split( '|' ) ) )
        #
        if len( lParts ) == 1: continue
        #
        if not lHeader:
            #
            lHeader = lParts
            #
        #
        yield lParts



'''
oTest = {
    'cNationality': ('Nationality', 'C'),
    'iUser_id': ('Owner', 1), 
    'cLookFor': ('Considered A Hit If This Text Is Found (Each Line '
                 'Evaluated Separately, Put Different Look For Tests '
                 'On Different Lines)', None),
    'iLegacyKey': ('Legacy Key', 3140),
    'cComment': ('Comments', ''),
    'tLegacyModify': ('Legacy Row Updated On', None),
    'tModify': ('Updated On',
            datetime.datetime(2017, 11, 5, 6, 9, 49, 259192, tzinfo=<UTC>)),
    'id': ('Id', 1021),
    'cTitle': ('Brand Name', 'Addison'),
    'tLegacyCreate': ('Legacy Row Created On',
            datetime.datetime(2001, 9, 16, 23, 49, 9, tzinfo=<UTC>)),
    'tCreate': ('Created On',
            datetime.datetime(2017, 11, 5, 6, 9, 49, 259160, tzinfo=<UTC>)),
    'bAllOfInterest': ('Want Everything From This Brand?', False),
    'bWanted': ('Want Anything From This Brand?', True),
    'cExcludeIf': ('Not A Hit If This Text Is Found (Each Line Evaluated '
                   'Separately, Put Different Exclude Tests On Different '
                   'Lines)', ''),
    'iStars': ('Desireability, 10 Star Brand Is Most Desireable', 5),
    'iUser_id': ('Owner', 1),
    'NotOnList': ('blah blah blah', None }
'''