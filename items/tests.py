from django.test import TestCase

# Create your tests here.

# from six          import next, print_ as print3

from .test_big_text import sExampleResponse
from .utils         import getSearchResultGenerator

from File.Del   import DeleteIfExists
from File.Write import WriteText2File

sExampleFile = '/tmp/search_results.json'

class getImportSearchResultsTest(TestCase):
    #
    def test_get_search_results(self):
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        WriteText2File( sExampleResponse, sExampleFile )
        #
        searchResult = getSearchResultGenerator( sExampleFile )
        dThisItem, iThisItem, iTotalItems = next( searchResult )
        #
        self.assertEqual( iThisItem, 1 )
        self.assertEqual( iTotalItems, 1 )
        # print3( 'dThisItem.keys():', list( dThisItem.keys() ) )
        self.assertEqual( dThisItem["itemId"],  "253295991282" )
        self.assertEqual( dThisItem["title" ],  "Simpson 360 Multimeter" )
        self.assertEqual( dThisItem["location"],"Piedmont,SC,USA" )
        self.assertEqual( dThisItem["country"], "US" )
        self.assertEqual( dThisItem["galleryURL"], 
            "http://thumbs3.ebaystatic.com/m/mDzuc_hBdbr66ce2oqz2yxA/140.jpg" )
        #
        dListingInfo    = dThisItem["listingInfo"]
        self.assertEqual( dListingInfo["startTime"], "2017-12-05T14:01:02.000Z" )
        self.assertEqual( dListingInfo[ "endTime" ], "2018-01-04T14:01:02.000Z" )
        self.assertEqual( dListingInfo["bestOfferEnabled" ], "false" )
        self.assertEqual( dListingInfo["buyItNowAvailable"], "false" )
        #
        dPrimaryCategory= dThisItem["primaryCategory"]
        self.assertEqual( dPrimaryCategory["categoryId"  ], "58277"       )
        self.assertEqual( dPrimaryCategory["categoryName"], "Multimeters" )
        #
        dCondition      = dThisItem["condition"]
        self.assertEqual( dCondition["conditionDisplayName"  ],
                                            "For parts or not working" )
        self.assertEqual( dCondition["conditionId"           ], "7000" )
        #
        dSellingStatus  = dThisItem["sellingStatus"]
        self.assertEqual( dSellingStatus["sellingState"], "Active" )
        
        dCurrentPrice   = dSellingStatus["currentPrice"]
        self.assertEqual( dCurrentPrice["@currencyId"], "USD" )
        self.assertEqual( dCurrentPrice["__value__"  ], "39.0")
        #
        dConvertPrice   = dSellingStatus["convertedCurrentPrice"]
        self.assertEqual( dConvertPrice["@currencyId"], "USD" )
        self.assertEqual( dConvertPrice["__value__"  ], "39.0")
        #
        DeleteIfExists( sExampleFile )





