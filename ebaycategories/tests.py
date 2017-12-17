from django.test import TestCase

# Create your tests here.

from .utils  import cCategoryVersionFile, getCategoryVersion

from File.Del   import DeleteIfExists
from File.Write import WriteText2File


from core.ebay_wrapper import oEbayConfig


class EbayWrapperTests(TestCase):
    '''ebay wrapper tests'''
    
    def test_get_ini_values(self):
        
        self.assertEquals( oEbayConfig['call']['global_id'], 'EBAY-US' )
        
        self.assertEquals( oEbayConfig['research']['Token'], 'ENTER_HERE' )


# actually for 'EBAY-US' as of 2017-12
sExampleCategoryVersion = (
  '''<?xml version="1.0" encoding="UTF-8"?>
    <GetCategoriesResponse xmlns="urn:ebay:apis:eBLBaseComponents">
        <Timestamp>2017-12-12T04:45:28.766Z</Timestamp>
        <Ack>Success</Ack>
        <Version>1041</Version>
        <Build>E1041_CORE_APICATALOG_18587827_R1</Build>
        <UpdateTime>2017-06-13T02:06:57.000Z</UpdateTime>
        <CategoryVersion>117</CategoryVersion>
        <ReservePriceAllowed>true</ReservePriceAllowed>
        <MinimumReservePrice>0.0</MinimumReservePrice>
    </GetCategoriesResponse>''' )




class getCategoryVersionTest(TestCase):
    #
    def test_get_category_version(self):
        # create/destroy test file needs to be in here
        # test is run AFTER the last line in this file is executed
        WriteText2File(
            sExampleCategoryVersion, cCategoryVersionFile % 'EBAY-US' )
        self.assertEqual( getCategoryVersion(), '117' )
        DeleteIfExists( cCategoryVersionFile % 'EBAY-US' )

