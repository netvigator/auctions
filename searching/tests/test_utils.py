from datetime           import timedelta

from django.test.client import Client, RequestFactory
from django.test        import TestCase
from django.utils       import timezone

from core.test_utils    import BaseUserTestCase, getDefaultMarket

from ..models           import Search, ItemFound
from ..utils            import (
                            getSearchResultGenerator, getItemFoundForWriting )

from .test_big_text     import sExampleResponse

from File.Del           import DeleteIfExists
from File.Write         import WriteText2File



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




class ItemsFoundRecyclingTest(BaseUserTestCase):

    def test_fetch_oldest_of_the_old(self):
        #
        """
        Want to recycle old records, make sure this is working!
        """
        #
        iWantOlderThan = 120
        #
        #
        sItemTitle1 = "Great Widget"
        iItemID     = 2823
        oSearch = ItemFound( cTitle = sItemTitle1,
                             iItemNumb = iItemID, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan -2 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        sItemTitle2 = "Phenominal Gadget"
        iItemID     = 2418
        oSearch = ItemFound( cTitle = sItemTitle2,
                             iItemNumb = iItemID, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan + 1 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        sItemTitle3 = "Awesome Thing a Ma Jig"
        iItemID     = 2607
        oSearch = ItemFound( cTitle = sItemTitle3,
                             iItemNumb = iItemID, iUser = self.user1 )
        oSearch.save()
        dDropDead = timezone.now() - timedelta( days = iWantOlderThan + 2 )
        oSearch.tCreate = dDropDead
        oSearch.save()
        #
        oWriteable = getItemFoundForWriting()
        #
        self.assertEqual( oWriteable.cTitle, sItemTitle3 )
        #
        self.assertTrue( timezone.now() >= oWriteable.tCreate )
        
        tFuture = oWriteable.tCreate + timedelta( seconds = 1 )
        self.assertTrue( timezone.now() < tFuture )
        #
        oWriteable = getItemFoundForWriting( iWantOlderThan = 140 )
        #
        self.assertEqual( oWriteable.cTitle, '' )


