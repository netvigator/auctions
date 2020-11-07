from django.utils           import timezone

from django_webtest         import TestApp

from ..utils                import ( _getIsoDateTimeOffDateTimeCol,
                                     getReverseWithUpdatedQuery,
                                     getWhatsNotInParens,
                                     getShrinkItemURL, getLink,
                                     getSaySequence,
                                     getSubstituteForReturn,
                                     oInParensFinder )

from .base                  import ( getUrlQueryStringOff, TestCasePlus,
                                     queryGotUpdated,
                                     SetUpBrandsCategoriesModelsWebTest )

from config.wsgi            import application

from ebayinfo.models        import Market
from ebayinfo.tests         import EBAY_CURRENT_VERSION_US
from ebayinfo.tests.base    import PutMarketsInDatabaseTestBase

from models.models          import Model

from pyPks.Time             import _sFormatISOdateTimeNoColon
from pyPks.Time.Test        import isISOdatetime


oAuctionBotApp = TestApp( application )


class BasicAppTestsDjangoStyle( TestCasePlus ):

    def test_basic_function( self ):
        #
        oResponse = oAuctionBotApp.get( '/' )
        #
        self.assertEqual( oResponse.status,         '200 OK'    )
        self.assertEqual( oResponse.status_int,      200        )
        self.assertEqual( oResponse.content_type,   'text/html' )
        self.assertTrue(  oResponse.mustcontain,    '<html'     )
        self.assertTrue(  oResponse.mustcontain,    '</html>'   )


class BasicAppTestCasePlus( TestCasePlus ):

    def test_testplus_get( self ):
        self.get( '/' )
        self.response_200()
        self.assertInContext( 'STATIC_URL' )


    def test_testplus_get_quick( self ):
        response = self.get_check_200( '/' )
        self.assertInContext( 'STATIC_URL' )



class DateTimeTests( TestCasePlus ):
    '''date time function tests'''

    def test_getIsoDateTimeOffDateTimeCol(self):
        #
        '''test _getIsoDateTimeOffDateTimeCol()'''
        #
        oNow = timezone.now()
        #
        sNow = _getIsoDateTimeOffDateTimeCol( oNow )
        #
        self.assertTrue( isISOdatetime( sNow, _sFormatISOdateTimeNoColon ) )

    def test_getReverseWithUpdatedQuery(self):
        #
        self.pk         = 1
        self.tModify    = timezone.now()
        #
        kwargs = { 'pk': self.pk, 'tModify': self.tModify }
        #
        sURL = getReverseWithUpdatedQuery( 'models:detail', kwargs = kwargs )
        #
        tParts = getUrlQueryStringOff( sURL )
        #
        self.assertEqual( tParts[0], '/models/%s/' % self.pk )
        #
        self.assertTrue( queryGotUpdated( tParts[1] ) )
        #
        self.assertFalse( queryGotUpdated( tParts[0] ) )


class textProcessingTests( TestCasePlus ):
    '''text processing tests'''

    def test_getWhatsNotInParens(self):
        #
        '''test getWhatsNotInParens()'''
        #
        s = 'This is for real (but not yet)'
        #
        self.assertEqual( getWhatsNotInParens(s), 'This is for real' )

    def test_getShrinkItemURL(self):
        #
        '''test getShrinkItemURL()'''
        #
        sLongURL = 'https://www.ebay.com/itm/Vintage-RCA-Tube-Amplifier/282772895981'
        #
        sWantShort = 'https://www.ebay.com/itm/282772895981'
        #
        sGotShort = getShrinkItemURL( sLongURL )
        #
        self.assertEqual( sWantShort, sGotShort )
        #

    def test_get_text_sequence( self ):
        #
        t = ( 'Moe', 'Larry', 'Curly' )
        #
        self.assertEqual( getSaySequence( t ), 'Moe, Larry & Curly' )


class TestUpdatingLoadedDictiorary( PutMarketsInDatabaseTestBase ):
    #
    def test_get_dict_siteID_2_list_vers( self ):
        #
        import ebayinfo.utils
        #
        from core.utils import updateMemoryTableUpdated
        #
        updateMemoryTableUpdated( 'markets', 'iCategoryVer' )
        #
        oUSA = Market.objects.get( cMarket = 'EBAY-US' )
        #
        self.assertEqual( oUSA.iCategoryVer, EBAY_CURRENT_VERSION_US )
        #
        iDictVers = ebayinfo.utils.dSiteID2ListVers[ oUSA.iEbaySiteID ]
        #
        self.assertEqual( iDictVers, EBAY_CURRENT_VERSION_US )
        #
        self.assertEqual( oUSA.iCategoryVer, iDictVers,
                          msg = 'table & memory values should be same' )
        #
        oUSA.iCategoryVer = 116 # current version is actually higher
        oUSA.save() # saved to table but dSiteID2ListVers should have higher
        #
        self.assertEqual( oUSA.iCategoryVer, 116 )
        #
        iDictVers = ebayinfo.utils.dSiteID2ListVers[ oUSA.iEbaySiteID ]
        #
        self.assertNotEqual( oUSA.iCategoryVer, iDictVers,
                             msg = 'table has 116, dict not updated yet' )
        #
        updateMemoryTableUpdated( 'markets', 'iCategoryVer' )
        #
        iDictVers = ebayinfo.utils.dSiteID2ListVers[ oUSA.iEbaySiteID ]
        #
        self.assertEqual( oUSA.iCategoryVer,
                          iDictVers,
                          msg = 'table has 116, dict updated' )
        #
        oUSA.iCategoryVer = EBAY_CURRENT_VERSION_US
        oUSA.save()
        #
        iDictVers = ebayinfo.utils.dSiteID2ListVers[ oUSA.iEbaySiteID ]
        #
        self.assertNotEqual( oUSA.iCategoryVer, iDictVers,
                             msg = 'table has %s, dict not updated yet' %
                                    EBAY_CURRENT_VERSION_US )
        #
        #
        updateMemoryTableUpdated( 'markets', 'iCategoryVer' )
        #
        iDictVers = ebayinfo.utils.dSiteID2ListVers[ oUSA.iEbaySiteID ]
        #
        self.assertEqual( oUSA.iCategoryVer, iDictVers )
        #


class TestGetLinksForObjects( SetUpBrandsCategoriesModelsWebTest ):

    def test_get_link( self ):
        #
        oModel = Model.objects.all()[0]
        #
        self.assertIsNotNone( oModel )



class TestGetSubstituteForReturn( TestCasePlus ):

    def test_GetSubstituteForReturn( self ):
        #
        sOrig = 'abc\ndef\rghi\r\njkl'
        #
        self.assertEqual(
                getSubstituteForReturn( sOrig ),
                'abc - def - ghi - jkl' )
        #
        self.assertEqual(
                getSubstituteForReturn( sOrig, bOmitLast = True ),
                'abc - def - ghi' )
        #
        self.assertEqual(
                getSubstituteForReturn( sOrig, '<BR>' ),
                'abc<BR>def<BR>ghi<BR>jkl' )
        #

class TestParensFinder( TestCasePlus ):

    def test_oInParensFinder( self ):
        #
        sTitle = ( 'Phillips Jan 6189W (5814A, 12AU7) Vintage vaccum tubes' )
        #
        self.assertEqual( oInParensFinder( sTitle ), ['(5814A, 12AU7)'] )
        #
        sTitle = ( 'Phillips Jan 6189W [5814A, 12AU7] Vintage vaccum tubes' )
        #
        self.assertEqual( oInParensFinder( sTitle ), ['[5814A, 12AU7]'] )
        #
        sTitle = ( 'Phillips Jan 6189W {5814A, 12AU7} Vintage vaccum tubes' )
        #
        self.assertEqual( oInParensFinder( sTitle ), ['{5814A, 12AU7}'] )
        #
        # print( oInParensFinder( sTitle ) )
