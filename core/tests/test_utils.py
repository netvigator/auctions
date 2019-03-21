from django.utils       import timezone

from ..utils            import ( _getIsoDateTimeOffDateTimeCol,
                                 getReverseWithUpdatedQuery,
                                 getWhatsNotInParens,
                                 getShrinkItemURL )
from ..utils_test       import ( getUrlQueryStringOff,
                                 queryGotUpdated )

from core.utils_test    import TestCasePlus

from ebayinfo           import EBAY_US_CURRENT_VERSION

from ebayinfo.models    import Market

from ebayinfo.utils_test import ( getMarketsIntoDatabase,
                                  PutMarketsInDatabaseTest )

from Time               import sFormatISOdateTimeNoColon
from Time.Test          import isISOdatetime



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
        self.assertTrue( isISOdatetime( sNow, sFormatISOdateTimeNoColon ) )

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


class TestUpdatingLoadedDictiorary( PutMarketsInDatabaseTest ):
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
        self.assertEqual( oUSA.iCategoryVer, EBAY_US_CURRENT_VERSION )
        #
        iDictVers = ebayinfo.utils.dSiteID2ListVers[ oUSA.iEbaySiteID ]
        #
        self.assertEqual( iDictVers, EBAY_US_CURRENT_VERSION )
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
        oUSA.iCategoryVer = 115
        oUSA.save()
        #
        iDictVers = ebayinfo.utils.dSiteID2ListVers[ oUSA.iEbaySiteID ]
        #
        self.assertNotEqual( oUSA.iCategoryVer, iDictVers,
                             msg = 'table has 115, dict not updated yet' )
        #
        #
        updateMemoryTableUpdated( 'markets', 'iCategoryVer' )
        #
        iDictVers = ebayinfo.utils.dSiteID2ListVers[ oUSA.iEbaySiteID ]
        #
        self.assertEqual( oUSA.iCategoryVer, iDictVers )
        #


