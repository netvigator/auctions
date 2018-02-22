from datetime           import timedelta

from django.test        import TestCase
from django.utils       import timezone

from core.utils_testing import BaseUserTestCase

from ..models           import Search, ItemFound, UserItemFound
from ..utils            import ( getUserItemFoundForWriting,
                            getSearchResultGenerator, getItemFoundForWriting )

from ..tests            import sExampleResponse

from File.Del           import DeleteIfExists
from File.Write         import WriteText2File

from pprint             import pprint

sExampleFile = '/tmp/search_results.json'

class getImportSearchResultsTest(TestCase):
    #
    def test_get_search_results(self):
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        WriteText2File( sExampleResponse, sExampleFile )
        #
        itemResultsIterator = getSearchResultGenerator( sExampleFile )
        #
        dThisItem = next( itemResultsIterator )
        #
        self.assertEqual( dThisItem["itemId"],  "253313715173" )
        self.assertEqual( dThisItem["title" ],
            "Simpson 360-2 Digital Volt-Ohm Milliammeter Operator's Manual" )
        self.assertEqual( dThisItem["location"],"Ruskin,FL,USA" )
        self.assertEqual( dThisItem["country"], "US" )
        self.assertEqual( dThisItem["postalCode"], "33570" )
        self.assertEqual( dThisItem["globalId"], "EBAY-US" )
        self.assertEqual( dThisItem["galleryURL"], 
            "http://thumbs2.ebaystatic.com/m/m0WO4pWRZTzusBvJHT07rtw/140.jpg" )
        self.assertEqual( dThisItem["viewItemURL"],
            "http://www.ebay.com/itm/Simpson-360-2-Digital-Volt-Ohm-"
            "Milliammeter-Operators-Manual-/253313715173" )
        #
        dListingInfo    = dThisItem["listingInfo"]
        self.assertEqual( dListingInfo["startTime"], "2017-12-15T05:22:47.000Z" )
        self.assertEqual( dListingInfo[ "endTime" ], "2018-01-14T05:22:47.000Z" )
        self.assertEqual( dListingInfo["bestOfferEnabled" ], "false" )
        self.assertEqual( dListingInfo["buyItNowAvailable"], "false" )
        #
        dPrimaryCategory= dThisItem["primaryCategory"]
        self.assertEqual( dPrimaryCategory["categoryId"  ], "58277"       )
        self.assertEqual( dPrimaryCategory["categoryName"], "Multimeters" )
        #
        dCondition      = dThisItem["condition"]
        self.assertEqual( dCondition["conditionDisplayName"  ], "Used" )
        self.assertEqual( dCondition["conditionId"           ], "3000" )
        #
        dSellingStatus  = dThisItem["sellingStatus"]
        self.assertEqual( dSellingStatus["sellingState"], "Active" )
        
        dCurrentPrice   = dSellingStatus["currentPrice"]
        self.assertEqual( dCurrentPrice["@currencyId"], "USD" )
        self.assertEqual( dCurrentPrice["__value__"  ], "10.0")
        #
        dConvertPrice   = dSellingStatus["convertedCurrentPrice"]
        self.assertEqual( dConvertPrice["@currencyId"], "USD" )
        self.assertEqual( dConvertPrice["__value__"  ], "10.0")
        #
        dPagination     = dThisItem["paginationOutput"]
        self.assertEqual( dPagination["totalEntries"], "4" )
        self.assertEqual( dPagination["thisEntry"   ], "1" )
        #
        iItems = 1
        #
        for dThisItem in itemResultsIterator:
            #
            iItems += 1
            #
        self.assertEqual( iItems, 4 )
        #
        DeleteIfExists( sExampleFile )


class StoreItemsFoundHaveOldRecordsBase(BaseUserTestCase):
    ''' create base class so multiple tests can have old records to test'''

    sTitle1     = "Great Widget"
    iItemID1    = 2823
    sTitle2     = "Phenominal Gadget"
    iItemID2    = 2418
    sTitle3     = "Awesome Thing a Ma Jig"
    iItemID3    = 2607

    def setUp(self):
        #
        iWantOlderThan = 100
        #
        oSearch = ItemFound( cTitle = self.sTitle1, iItemNumb = self.iItemID1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan -2 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        oSearch = ItemFound( cTitle = self.sTitle2, iItemNumb = self.iItemID2 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan - 9 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        oSearch = ItemFound( cTitle = self.sTitle3, iItemNumb = self.iItemID3 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan + 2 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        

class ItemsFoundRecyclingTest(StoreItemsFoundHaveOldRecordsBase):

    def test_fetch_oldest_of_the_old(self):
        #
        """
        Want to recycle old records, make sure this is working!
        """
        #
        iWantOlderThan = 100
        #
        oWriteable = getItemFoundForWriting()
        #
        self.assertEqual( oWriteable.cTitle, self.sTitle3 )
        #
        self.assertTrue( timezone.now() >= oWriteable.tCreate )
        
        tFuture = oWriteable.tCreate + timedelta( seconds = 1 )
        self.assertTrue( timezone.now() < tFuture )
        #
        oWriteable = getItemFoundForWriting( iWantOlderThan = 140 )
        #
        self.assertIsNone( oWriteable )


class UserItemsFoundRecyclingTest(BaseUserTestCase):

    def test_fetch_oldest_of_the_old(self):
        #
        """
        Want to recycle old records, make sure this is working!
        """
        #
        iWantOlderThan = 100
        #
        #
        iItemID1 = 2823
        oSearch = UserItemFound( iItemNumb = iItemID1, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan -2 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        iItemID2 = 2418
        oSearch = UserItemFound( iItemNumb = iItemID2, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan + 1 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        iItemID3 = 2607
        oSearch = UserItemFound( iItemNumb = iItemID3, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan + 2 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        oWriteable = getUserItemFoundForWriting()
        #
        self.assertEqual( oWriteable.iItemNumb, iItemID3 )
        #
        self.assertTrue( timezone.now() >= oWriteable.tCreate )
        
        tFuture = oWriteable.tCreate + timedelta( seconds = 1 )
        self.assertTrue( timezone.now() < tFuture )
        #
        oWriteable = getUserItemFoundForWriting( iWantOlderThan = 140 )
        #
        self.assertIsNone( oWriteable )


class storeItemFoundTest(StoreItemsFoundHaveOldRecordsBase):
    #
    ''' class for testing storeItemFound() '''

    def test_store_item_found(self):
        #
        ''' test storeItemFound() with actual record'''
        #
        from ..tests    import dSearchResult # in __init__.py
        from ..utils    import storeItemFound
        #
        storeItemFound( dSearchResult )
        #
        oResultRow = ItemFound.objects.filter(
                                iItemNumb = int(
                                    dSearchResult['itemId'] ) ).first()
        #
        self.assertIsNotNone( oResultRow )
        #
        self.assertEqual( oResultRow.iItemNumb,
                         int( dSearchResult['itemId'] ) )
        #



class storeUserItemFoundTest(BaseUserTestCase):
    #
    ''' class for testing storeUserItemFound() '''

    def test_store_User_item_found(self):
        #
        ''' test storeItemFound() with actual record'''
        #
        from ..tests    import dSearchResult # in __init__.py
        from ..utils    import storeUserItemFound
        #
        storeUserItemFound( dSearchResult, self.user1 )
        #
        oResultRow = UserItemFound.objects.filter(
                                iItemNumb = int(
                                    dSearchResult['itemId'] ) ).first()
        #
        self.assertIsNotNone( oResultRow )
        #
        self.assertEqual( oResultRow.iItemNumb,
                         int( dSearchResult['itemId'] ) )
        #
