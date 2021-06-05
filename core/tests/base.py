from django.urls            import reverse

from django.db.utils        import IntegrityError
from django.test            import RequestFactory
from django.test.client     import Client

from django_webtest         import WebTest
from test_plus.test         import TestCase, CBVTestCase

from core.dj_import         import HttpRequest, get_user_model
from core.utils             import getWhatsNotInParens

from config.settings.base   import LOGIN_URL

from brands.models          import Brand
from categories.models      import Category
from models.models          import Model

from ebayinfo.tests         import ( EBAY_CURRENT_VERSION_US,
                                     EBAY_CURRENT_VERSION_GB,
                                     EBAY_CURRENT_VERSION_Mo,
                                     EBAY_CURRENT_VERSION_ENCA,
                                     sEbayCategoryDump )

from ebayinfo.models        import EbayCategory, Market

from pyPks.String.Find      import getRegExObj
from pyPks.String.Get       import getTextAfter, getTextBefore
from pyPks.Time.Test        import isISOdatetimeFileNameSafe, isDateTimeObj
from pyPks.Utils.Config     import getBoolOffYesNoTrueFalse as getBool
from pyPks.Utils.DataBase   import getTableFromScreenCaptureGenerator


class UserSetUpMixin( object ):

    @classmethod
    def setUpTestData( cls ):

        cls.factory = RequestFactory()

        cls.market  = getDefaultMarket()

        oUserModel = get_user_model()

        cls.user1 = oUserModel.objects.create_user(
                                    'username1', 'email@ymail.com')
        cls.user1.set_password( 'mypassword')
        cls.user1.first_name   = 'John'
        cls.user1.last_name    = 'Citizen'
        cls.user1.save()

        cls.user2 = oUserModel.objects.create_user(
                                    'username2', 'email@gmail.com')
        cls.user2.set_password( 'mypassword')
        cls.user2.first_name   = 'Joe'
        cls.user2.last_name    = 'Blow'
        cls.user2.save()

        cls.user3 = oUserModel.objects.create_user(
                                    'username3', 'email@hotmail.com' )
        cls.user3.set_password( 'mypassword')
        cls.user3.first_name   = 'Oscar'
        cls.user3.last_name    = 'Zilch'
        cls.user3.is_superuser = True
        cls.user3.save()
        #
        cls.request = HttpRequest()
        cls.request.user = cls.user1
        #
        #
        # putting user1 last saves the user1 records in self
        #
        cls.tUsers = ( cls.user3, cls.user2, cls.user1 )
        #

    def setUp(self):
        #
        self.client.login(username ='username1', password='mypassword')
        #


class TestCasePlus( TestCase ):
    """subclass of test_plus.test TestCase
    allows implementation of project specific helper methods"""
    #
    pass


class BaseUserTestPlusCase( UserSetUpMixin, TestCasePlus ):

    pass


class BaseUserViewTestPlusCase( UserSetUpMixin, CBVTestCase ):

    pass




def getDefaultMarket():

    if Market.objects.count() == 0:
        #
        market = Market()
        #
        market.cMarket     = 'EBAY-ENCA'
        market.cCountry    = 'CA'
        market.iEbaySiteID = 2
        market.iCategoryVer= EBAY_CURRENT_VERSION_ENCA
        market.cCurrencyDef= 'CAD'
        market.cLanguage   = 'en-CA'
        market.save()
        #
        #
        market = Market()
        #
        market.cMarket     = 'EBAY-GB'
        market.cCountry    = 'UK'
        market.iEbaySiteID = 3
        market.iCategoryVer= EBAY_CURRENT_VERSION_GB
        market.cCurrencyDef= 'GBP'
        market.cLanguage   = 'en-UK'
        market.save()
        #
        #
        market = Market()
        #
        market.cMarket     = 'EBAY-MOTOR'
        market.cCountry    = 'US'
        market.iEbaySiteID = 100
        market.iCategoryVer= EBAY_CURRENT_VERSION_Mo
        market.cCurrencyDef= 'USD'
        market.cLanguage   = 'en-US'
        market.save()
        #
        #
        market = Market()
        #
        market.cMarket     = 'EBAY-US'
        market.cCountry    = 'US'
        market.iEbaySiteID = 0
        market.iCategoryVer= EBAY_CURRENT_VERSION_US
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

    @classmethod
    def setUpTestData( cls ):
        #
        super().setUpTestData()
        #
        cls.ebc = EbayCategory(
            iCategoryID = 10,
            name        = 'hot products',
            iLevel      = 1,
            iParentID   = 1,
            iTreeVersion= 1,
            iEbaySiteID = cls.market,
            bLeafCategory = False )
        cls.ebc.save()
        #
        cls.client = Client()




class BaseUserWebTestCase( UserSetUpMixin, WebTest ):

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
    @classmethod
    def setUpTestData( cls ):
        #
        super().setUpTestData() # absolutely need for this mixin !!!
        #
        for oUser in cls.tUsers:
            #
            cls.setUpBrandsCategoriesModels( cls, oUser )
            #
            # putting user1 last saves the user1 records in cls


    def setUpBrandsCategoriesModels( cls, oUser ):
        #
        cls.oBrand_hp = Brand(
            cTitle      = "Hewlett-Packard",
            cLookFor    = "hp",
            cExcludeIf  = '',
            iStars      = 5,
            iUser       = oUser )
        #
        cls.oBrand_hp.save()
        #
        cls.oBrand_GT = Brand(
            cTitle      = "Groove Tube",
            cLookFor    = "Groove Tubes",
            cExcludeIf  = '',
            iStars      = 4,
            iUser       = oUser )
        #
        cls.oBrand_GT.save()
        #
        cls.oBrand = Brand(
            cTitle      = "Cadillac",
            cLookFor    = "Caddy",
            cExcludeIf  = 'golf',
            iStars      = 5,
            iUser       = oUser )
        #
        cls.oBrand.save()
        #
        cls.oCategory = Category(
            cTitle      = "Capacitor Checker",
            cLookFor    = "Capacitor Tester\r"
                          "Capacitance Checker\r"
                          "Capacitance Tester",
            iStars      = 5,
            iUser       = oUser )
        cls.oCategory.save()
        #
        oBrand = Brand(
            cTitle      = "Digital",
            cLookFor    = "",
            cExcludeIf  = '',
            iStars      = 4,
            iUser       = oUser )
        #
        oBrand.save()
        #
        oModel = Model(
            cTitle      = "470mF",
            bSubModelsOK= False,
            iStars      = 4,
            iBrand      = oBrand,
            iCategory   = cls.oCategory,
            iUser       = oUser )
        oModel.save()
        #
        cls.oCategory = Category(
            cTitle      = "Widget",
            cKeyWords   = 'Gadget',
            cLookFor    = "Gizmo",
            cExcludeIf  = 'Delta',
            iStars      = 5,
            iUser       = oUser )
        cls.oCategory.save()
        #
        cls.CategoryID = cls.oCategory.id
        #
        cls.WidgetCategory = cls.oCategory
        #
        #
        cls.oCategory = Category(
            cTitle      = "Manual",
            iStars      = 3,
            iUser       = oUser )
        cls.oCategory.save()
        #
        cls.ManualCategory = cls.oCategory
        #
        #
        #
        oModel = Model(
            cTitle      = "601b",
            bSubModelsOK= True,
            iStars      = 5,
            iBrand      = cls.oBrand,
            iCategory   = cls.oCategory,
            iUser       = oUser )
        oModel.save()
        #
        oModel = Model(
            cTitle      = "Model 2",
            cLookFor    = "Model Two",
            iStars      = 5,
            iBrand      = cls.oBrand,
            iCategory   = cls.oCategory,
            iUser       = oUser )
        oModel.save()
        #
        # overwrite
        #
        cls.oModel = Model(
            cTitle      = "Fleetwood",
            cLookFor    = "Woodie",
            cKeyWords   = 'Eldorado',
            cExcludeIf  = 'golf\rtournament', # used in tests/test_stars.py
            iStars      = 5,
            iBrand      = cls.oBrand,
            iCategory   = cls.oCategory,
            iUser       = oUser )
        cls.oModel.save()
        #
        cls.iModelID = cls.oModel.id





class SetUpBrandsCategoriesModelsWebTest(
            SetUpBrandsCategoriesModelsMixin, BaseUserWebTestCase ):

    ''' handy base class that sets up some models / tables '''

    #
    pass # putting user1 last saves the user1 records in self



class SetUpBrandsCategoriesModelsTestPlus(
            SetUpBrandsCategoriesModelsMixin, BaseUserTestPlusCase ):

    ''' handy base class that sets up some models / tables '''

    #
    pass # putting user1 last saves the user1 records in self



class SetUpBrandsCategoriesModelsViewTestPlus(
            SetUpBrandsCategoriesModelsMixin, BaseUserViewTestPlusCase ):

    ''' handy base class that sets up some models / tables '''

    #
    pass # putting user1 last saves the user1 records in self



def setup_view_for_tests( view, request, *args, **kwargs ):
    #
    """
    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to reverse()``
    """
    #
    view.request= request
    view.args   = args
    view.kwargs = kwargs
    #
    return view




class GetEbayCategoriesWebTestSetUp( SetUpBrandsCategoriesModelsWebTest ):

    @classmethod
    def setUpTestData( cls ):
        #
        super().setUpTestData()
        #
        cls.iCategories = 0
        #
        cls.market  = getDefaultMarket()
        #
        sMarket, sWantVersion = 'EBAY-US', EBAY_CURRENT_VERSION_US
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iEbaySiteID     = cls.market,
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        sMarket, sWantVersion = 'EBAY-GB', EBAY_CURRENT_VERSION_GB
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iEbaySiteID_id  = 3, # on copy & paste, this varies !!!!!
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        sMarket, sWantVersion = 'EBAY-ENCA', EBAY_CURRENT_VERSION_ENCA
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iEbaySiteID_id  = 2, # on copy & paste, this varies !!!!!
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        sMarket, sWantVersion = 'EBAY-MOTOR', EBAY_CURRENT_VERSION_Mo
        #
        iWantVersion = int( sWantVersion )
        #
        oRootCategory = EbayCategory(
            name            = \
                '%s version %s Root' % ( sMarket, sWantVersion ),
            iCategoryID     = 0,
            iEbaySiteID_id  = 100, # on copy & paste, this varies !!!!!
            iTreeVersion    = iWantVersion,
            iLevel          = 0,
            bLeafCategory   = False,
            iParentID       = 0 )
        #
        oRootCategory.save()
        #
        oTableIter = getTableFromScreenCaptureGenerator( sEbayCategoryDump )
        #
        tHeader = next( oTableIter )
        #
        iCategories = 0
        #
        setTestCategories = set( [] )
        #
        oPriorRoot = oRootCategory
        #
        dCategoryEbaySiteIDs = {}
        #
        for lParts in oTableIter:
            #
            iCategoryID             = int( lParts[1] )
            iParentOfThis           = int( lParts[4] )
            iThisLevel              = int( lParts[3] )
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
                    iLevel          =           iThisLevel,
                    bLeafCategory   = getBool(  lParts[5] ),
                    iTreeVersion    = int(      lParts[6] ),
                    iEbaySiteID_id  =           iEbaySiteID )
            #
            if iThisLevel == 1: # top level iParentID
                #
                if oPriorRoot.iEbaySiteID_id != iEbaySiteID:
                    #
                    oRootCategory = EbayCategory.objects.get(
                        iEbaySiteID_id  = iEbaySiteID,
                        iLevel          = 0 )
                    #
                    oPriorRoot = oRootCategory
                    #
                #
                oCategory.iParentID = oRootCategory.iCategoryID
                oCategory.parent    = oRootCategory
                #
            else:
                #
                oParent         = EbayCategory.objects.get(
                                        iCategoryID     = iParentOfThis,
                                        iEbaySiteID_id  = iEbaySiteID )
                #
                oCategory.iParentID = iParentOfThis
                #
                bGotCategory4Market = False
                #
                bGotCategory4Market = (
                        ( iParentOfThis, iEbaySiteID )
                        in
                        dCategoryEbaySiteIDs )
                #
                if bGotCategory4Market:
                    #
                    iParentID = dCategoryEbaySiteIDs[ ( iParentOfThis, iEbaySiteID ) ]
                    #
                    oCategory.parent_id = iParentID
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
            dCategoryEbaySiteIDs[ ( iCategoryID, iEbaySiteID ) ] = oCategory.id
            #
            iCategories += 1
            #
        #
        cls.iCategories = iCategories + 4 # add root categories
        #
        cls.setTestCategories = frozenset( setTestCategories )
        #



class AssertEmptyMixin( object ):

    def assertEmpty(self, obj):
        self.assertFalse(obj)


class AssertNotEmptyMixin( object ):

    def assertNotEmpty(self, obj):
        self.assertTrue(obj)


class AssertEqualIgnoreParensMixin( object ):

    def assertEqualIgnoreParens( self, sTitle, sTarget ):
        self.assertEqual( getWhatsNotInParens( sTitle ), sTarget )


class AssertIsDateTimeValueMixin( object ):

    def assertIsDateTimeValue( self, uDateTime ):
        #
        self.assertTrue( isDateTimeObj( uDateTime ) )


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
