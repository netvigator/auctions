from django.test            import TestCase
from django.contrib.auth    import get_user_model

from .forms                 import AddOrUpdateForm
from .models                import Search

from core.tests             import getDefaultMarket
from markets.models         import Market
from ebaycategories.models  import EbayCategory

# Create your tests here.





class SearchModelTest(TestCase):

    def setUp(self):

        getDefaultMarket( self )

        oUser = get_user_model()

        self.user1 = oUser.objects.create_user( 'username1', 'email@ymail.com' )
        self.user1.set_password( 'mypassword')
        self.user1.first_name   = 'John'
        self.user1.last_name    = 'Citizen'
        self.user1.save()
        
        if (  ( not isinstance( self.market, Market ) ) or
              ( not Market.objects.get( pk = 1 ) ) ):
            self.market = Market(
                cMarket     = 'EBAY-US',
                cCountry    = 'US',
                iEbaySiteID = 0,
                cLanguage   = 'en-US',
                iCategoryVer= 1,
                cCurrencyDef= 'USD' )
            self.market.save()
        
        self.ebc = EbayCategory(
            iCategoryID = 10,
            name        = 'hot products',
            iLevel      = 1,
            iParentID   = 1,
            iTreeVersion= 1,
            iMarket     = self.market,
            bLeafCategory = False )
        self.ebc.save()
        
    def test_string_representation(self):
        sSearch = "My clever search"
        oSearch = Search( cTitle = sSearch )
        self.assertEqual( str(oSearch), oSearch.cTitle )


    
    def AddNewSearchTest( TescCase ):
        
        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A",
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertTrue(valid)        
        
        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                iDummyCategory  = 1,
                cPriority       = "A",
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertTrue(valid)
        
        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                cPriority       = "A",
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertFalse(valid)

        form = AddOrUpdateForm(
                cTitle          = "My clever search",
                iDummyCategory  = 'abc',
                cPriority       = "A",
                iUser           = self.user1 )
        valid = form.is_valid()
        self.assertFalse(valid)
