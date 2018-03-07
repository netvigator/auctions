from django.test        import TestCase

from ..utils_testing    import setUpBrandsCategoriesModels
from ..utils_ebay       import (
        getFinders, getModelFinders, getCategoryFinders, getBrandFinders )


from brands.models      import Brand
from categories.models  import Category
from models.models      import Model



class getFindersTest( setUpBrandsCategoriesModels ):
    
    #
    ''' test getFinders for Brands, Categories & Models '''
    
    #
    #oBrand      = Model.objects.get(    cTitle = "Cadillac"  )
    #oCategory   = Category.objects.get( cTitle = "Widgets"   )
    #oModel      = Model.objects.get(    cTitle = "Fleetwood" )
    #
    
    def test_model_finders(self):
        
        ''' test model finders '''
        #
        t = getFinders(
                self.oModel.cTitle,
                self.oModel.cLookFor,
                self.oModel.cExcludeIf,
                self.oModel.cKeyWords )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle.findall(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords.findall( sAuctionTitle ) )
        #
        self.assertFalse( findExclude.findall(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude.findall(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle.findall(    sAuctionTitle ) )

        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertFalse( findTitle.findall(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude.findall(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords.findall( sAuctionTitle ) )
        #


    def test_brand_finders(self):
        
        ''' test brand finders '''
        #
        t = getFinders(
                self.oBrand.cTitle,
                self.oBrand.cLookFor,
                self.oBrand.cExcludeIf )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle.findall(    sAuctionTitle ) )
        #
        self.assertIsNone(findKeyWords )
        #
        self.assertFalse( findExclude.findall(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude.findall(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle.findall(    sAuctionTitle ) )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertFalse( findTitle.findall(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude.findall(  sAuctionTitle ) )
        #


    
    def test_category_finders(self):
        
        ''' test category finders '''
        #
        t = getFinders(
                self.oCategory.cTitle,
                self.oCategory.cLookFor,
                self.oCategory.cExcludeIf,
                self.oCategory.cKeyWords )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertTrue(  findTitle.findall(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords.findall( sAuctionTitle ) )
        #
        self.assertFalse( findExclude.findall(  sAuctionTitle ) )
        #
        self.assertTrue(  findTitle.findall(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Gemini Jets 1/200 Delta MD-80 Widget Livery N956DL'
        #
        self.assertTrue(  findExclude.findall(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertFalse( findTitle.findall(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude.findall(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords.findall( sAuctionTitle ) )
        #


    def test_getModelFinders(self):
        #
        t = getModelFinders( self.oModel.id )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle.findall(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords.findall( sAuctionTitle ) )
        #
        self.assertFalse( findExclude.findall(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude.findall(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle.findall(    sAuctionTitle ) )

        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertFalse( findTitle.findall(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude.findall(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords.findall( sAuctionTitle ) )
        #
        