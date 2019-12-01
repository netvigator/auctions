from core.dj_import     import reverse, HttpRequest, get_user_model
from django.db.utils    import IntegrityError
from django.test        import RequestFactory
from django.test.client import Client

from django_webtest     import WebTest, TestApp
from test_plus.test     import TestCase

from config.settings.base import LOGIN_URL
from config.wsgi        import application

from brands.models      import Brand
from categories.models  import Category
from models.models      import Model

# in __init__.py
from ebayinfo           import ( EBAY_US_CURRENT_VERSION,
                                 EBAY_GB_CURRENT_VERSION,
                                 sCategoryDump )

from ebayinfo.models    import EbayCategory, Market

from pyPks.String.Find  import getRegExObj
from pyPks.String.Get   import getTextAfter, getTextBefore
from pyPks.Time.Test    import isISOdatetimeFileNameSafe
from pyPks.Utils.Config import getBoolOffYesNoTrueFalse as getBool


class TestCasePlus( TestCase ):
    """subclass of test_plus.test TestCase
    allows implementation of project specific helper methods"""
    #
    pass


class BaseUserTestPlusCase( TestCasePlus ):

    def setUp(self):
        #
        self.user1 = self.make_user( 'u1' )
        self.user2 = self.make_user( 'u2' )
        self.user3 = self.make_user( 'u3' )
        #
        self.market  = getDefaultMarket()
        #
        self.login( self.user1 )
        #
        self.factory = RequestFactory()
        #
        self.market  = getDefaultMarket()
        #
        self.tUsers = ( self.user3, self.user2, self.user1 )
        #
        # putting user1 last saves the user1 records in self




oAuctionBotApp = TestApp( application )




oFindColumnSplits          = getRegExObj( r'(?: \|)|(?:\| )' )

def getDefaultMarket():

    if (        Market.objects.count() == 0 or
            not Market.objects.filter( pk = 3 ).exists() ):
        #
        market = Market()
        #
        market.cMarket     = 'EBAY-GB'
        market.cCountry    = 'UK'
        market.iEbaySiteID = 3
        market.iCategoryVer= EBAY_GB_CURRENT_VERSION
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
        market.iCategoryVer= EBAY_US_CURRENT_VERSION
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
            iEbaySiteID = self.market,
            bLeafCategory = False )
        self.ebc.save()
        #
        self.client = Client()



class BaseUserWebTestCase( WebTest ):

    def setUp(self):

        self.factory = RequestFactory()

        self.market  = getDefaultMarket()

        oUserModel = get_user_model()

        self.user1 = oUserModel.objects.create_user(
                                    'username1', 'email@ymail.com')
        self.user1.set_password( 'mypassword')
        self.user1.first_name   = 'John'
        self.user1.last_name    = 'Citizen'
        self.user1.save()

        self.user2 = oUserModel.objects.create_user(
                                    'username2', 'email@gmail.com')
        self.user2.set_password( 'mypassword')
        self.user2.first_name   = 'Joe'
        self.user2.last_name    = 'Blow'
        self.user2.save()

        self.user3 = oUserModel.objects.create_user(
                                    'username3', 'email@hotmail.com' )
        self.user3.set_password( 'mypassword')
        self.user3.first_name   = 'Oscar'
        self.user3.last_name    = 'Zilch'
        self.user3.is_superuser = True
        self.user3.save()
        #
        self.request = HttpRequest()
        self.request.user = self.user1
        #
        self.client.login(username ='username1', password='mypassword')
        #
        # putting user1 last saves the user1 records in self
        #
        self.tUsers = ( self.user3, self.user2, self.user1 )
        #

    def loginWebTest( self, username ='username1', password = 'mypassword' ):
        #
        form = self.app.get( reverse( LOGIN_URL ) ).form
        form['login']    = username
        form['password'] = password
        response = form.submit()
        #


class SetUpBrandsCategoriesModelsMixin( object ):
    #
    '''reuse setup code for WebTest and TestCasePlus '''
    #
    def setUp(self):
        #
        super( SetUpBrandsCategoriesModelsMixin, self ).setUp()
        #
        for oUser in self.tUsers:
            #
            self.setUpBrandsCategoriesModels( oUser )
            #
            # putting user1 last saves the user1 records in self


    def setUpBrandsCategoriesModels( self, oUser ):
        #
        self.oBrand_hp = Brand(
            cTitle      = "Hewlett-Packard",
            cLookFor    = "hp",
            cExcludeIf  = '',
            iStars      = 5,
            iUser       = oUser )
        #
        self.oBrand_hp.save()
        #
        self.oBrand_GT = Brand(
            cTitle      = "Groove Tube",
            cLookFor    = "Groove Tubes",
            cExcludeIf  = '',
            iStars      = 4,
            iUser       = oUser )
        #
        self.oBrand_GT.save()
        #
        self.oBrand = Brand(
            cTitle      = "Cadillac",
            cLookFor    = "Caddy",
            cExcludeIf  = 'golf',
            iStars      = 5,
            iUser       = oUser )
        #
        self.oBrand.save()
        #
        self.oCategory = Category(
            cTitle      = "Widget",
            cKeyWords   = 'Gadget',
            cLookFor    = "Gizmo",
            cExcludeIf  = 'Delta',
            iStars      = 5,
            iUser       = oUser )
        self.oCategory.save()
        #
        #
        self.CategoryID = self.oCategory.id
        #
        #
        oModel = Model(
            cTitle      = "601b",
            bSubModelsOK= True,
            iStars      = 5,
            iBrand      = self.oBrand,
            iCategory   = self.oCategory,
            iUser       = oUser )
        oModel.save()
        #
        oModel = Model(
            cTitle      = "Model 2",
            cLookFor    = "Model Two",
            iStars      = 5,
            iBrand      = self.oBrand,
            iCategory   = self.oCategory,
            iUser       = oUser )
        oModel.save()
        #
        # overwrite
        #
        self.oModel = Model(
            cTitle      = "Fleetwood",
            cLookFor    = "Woodie",
            cKeyWords   = 'Eldorado',
            cExcludeIf  = 'golf\rtournament', # used in tests/test_stars.py
            iStars      = 5,
            iBrand      = self.oBrand,
            iCategory   = self.oCategory,
            iUser       = oUser )
        self.oModel.save()





class SetUpBrandsCategoriesModelsWebTest(
            SetUpBrandsCategoriesModelsMixin, BaseUserWebTestCase ):

    ''' handy base class that sets up some models / tables '''

    def setUp(self):
        #
        super( SetUpBrandsCategoriesModelsWebTest, self ).setUp()
        #
        # putting user1 last saves the user1 records in self
        #



class SetUpBrandsCategoriesModelsTestPlus(
            SetUpBrandsCategoriesModelsMixin, BaseUserTestPlusCase ):

    ''' handy base class that sets up some models / tables '''

    def setUp(self):
        #
        super( SetUpBrandsCategoriesModelsTestPlus, self ).setUp()
        #
        # putting user1 last saves the user1 records in self
        #



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



def getNamePositionDict( lHeader ):
    #
    '''utility for getTableFromScreenCaptureGenerator()'''
    #
    dNamePosition = {}
    #
    i = 0
    #
    for sName in lHeader:
        #
        dNamePosition[ sName ] = i
        #
        i += 1
        #
    #
    return dNamePosition


def getTableFromScreenCaptureGenerator( uScreenCapture ):
    #
    from .utils import getSeqStripped
    #
    if isinstance( uScreenCapture, str ):
        #
        oLines = uScreenCapture.split( '\n' )
        #
    else:
        #
        oLines = uScreenCapture
        #
    #
    for sLine in oLines:
        #
        lParts = list( getSeqStripped( oFindColumnSplits.split( sLine ) ) )
        #
        if len( lParts ) == 1: continue
        #
        yield lParts



class GetEbayCategoriesWebTestSetUp( SetUpBrandsCategoriesModelsWebTest ):

    def setUp(self):
        #
        super( GetEbayCategoriesWebTestSetUp, self ).setUp()
        #
        self.iCategories = 0
        #
        self.market  = getDefaultMarket()
        #
        sMarket, sWantVersion = 'EBAY-US', '117'
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iEbaySiteID     = self.market,
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        sMarket, sWantVersion = 'EBAY-GB', '108'
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iEbaySiteID_id  = 3,
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        oTableIter = getTableFromScreenCaptureGenerator( sCategoryDump )
        #
        lHeader = next( oTableIter )
        #
        iCategories = 0
        #
        setTestCategories = set( [] )
        #
        for lParts in oTableIter:
            #
            iCategoryID             = int( lParts[1] )
            iEbaySiteID             = int( lParts[7] )
            #
            if EbayCategory.objects.filter(
                        iCategoryID     = iCategoryID,
                        iEbaySiteID_id  = iEbaySiteID ).exists():
                #
                print('for market %s, iCategoryID already exists: %s -- '
                    'clean up the list!' % (lParts[7],lParts[1] ) )
                #
                continue
                #
            #
            setTestCategories.add( ( iEbaySiteID, iCategoryID ) )
            #
            oCategory = EbayCategory(
                    iCategoryID     =           iCategoryID,
                    name            =           lParts[2],
                    iLevel          = int(      lParts[3] ),

                    bLeafCategory   = getBool(  lParts[5] ),
                    iTreeVersion    = int(      lParts[6] ),
                    iEbaySiteID_id  =           iEbaySiteID, )
            #
            if lParts[3] == '1': # top level iParentID
                oCategory.iParentID = oRootCategory.iCategoryID
                oCategory.parent    = oRootCategory
            else:
                oCategory.iParentID = int(     lParts[4] )
                #
                if EbayCategory.objects.filter(
                                iCategoryID = int( lParts[4] ),
                                iEbaySiteID = oCategory.iEbaySiteID ).exists():
                    #
                    oCategory.parent = EbayCategory.objects.get(
                                    iCategoryID = int( lParts[4] ),
                                    iEbaySiteID = oCategory.iEbaySiteID )
                    #
                else:
                    #
                    print('in market %s, cannot find iCategoryID %s, '
                          'parent of iCategoryID %s' %
                          ( lParts[7], lParts[4], lParts[1] ) )
                #
            #
            oCategory.save()
            #
            iCategories += 1
            #
        #
        self.iCategories = iCategories + 2 # add 2 root categories
        #
        self.setTestCategories = frozenset( setTestCategories )
        #


class AssertEmptyMixin( object ):

    def assertEmpty(self, obj):
        self.assertFalse(obj)


class AssertNotEmptyMixin( object ):

    def assertNotEmpty(self, obj):
        self.assertTrue(obj)


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
