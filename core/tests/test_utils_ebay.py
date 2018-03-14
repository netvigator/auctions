from django.test        import TestCase

from ..utils_testing    import setUpBrandsCategoriesModels
from ..utils_ebay       import (
        getRegExObjs, getModelRegExFinders, getCategoryRegExFinders, getBrandRegExFinders )


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
        t = getRegExObjs(
                self.oModel.cTitle,     # "Fleetwood"
                self.oModel.cLookFor,   # "Woodie"
                self.oModel.cExcludeIf, # 'golf'
                self.oModel.cKeyWords ) # 'Eldorado'
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle.search(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords.search( sAuctionTitle ) )
        #
        self.assertFalse( findExclude.search(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude.search(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle.search(    sAuctionTitle ) )

        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertFalse( findTitle.search(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude.search(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords.search( sAuctionTitle ) )
        #


    def test_brand_finders(self):
        
        ''' test brand finders '''
        #
        t = getRegExObjs(
                self.oBrand.cTitle,
                self.oBrand.cLookFor,
                self.oBrand.cExcludeIf )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle.search(    sAuctionTitle ) )
        #
        self.assertIsNone(findKeyWords )
        #
        self.assertFalse( findExclude.search(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude.search(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle.search(    sAuctionTitle ) )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertFalse( findTitle.search(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude.search(  sAuctionTitle ) )
        #


    
    def test_category_finders(self):
        
        ''' test category finders '''
        #
        t = getRegExObjs(
                self.oCategory.cTitle,
                self.oCategory.cLookFor,
                self.oCategory.cExcludeIf,
                self.oCategory.cKeyWords )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertTrue(  findTitle.search(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords.search( sAuctionTitle ) )
        #
        self.assertFalse( findExclude.search(  sAuctionTitle ) )
        #
        self.assertTrue(  findTitle.search(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Gemini Jets 1/200 Delta MD-80 Widget Livery N956DL'
        #
        self.assertTrue(  findExclude.search(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertFalse( findTitle.search(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude.search(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords.search( sAuctionTitle ) )
        #


    def test_getModelRegExFinders(self):
        #
        t = getModelRegExFinders( self.oModel )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords( sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )

        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertFalse( findTitle(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords( sAuctionTitle ) )
        #


    def test_getCategoryRegExFinders(self):
        #
        t = getCategoryRegExFinders( self.oCategory )
        #
        findTitle, findExclude, findKeyWords = t
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        self.assertTrue(  findKeyWords( sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Gemini Jets 1/200 Delta MD-80 Widget Livery N956DL'
        #
        self.assertTrue(  findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertFalse( findTitle(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        self.assertFalse( findKeyWords( sAuctionTitle ) )
        #




    def test_getBrandRegExFinders(self):
        #
        t = getBrandRegExFinders( self.oBrand )
        #
        findTitle, findExclude = t
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertTrue(  findExclude(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  findTitle(    sAuctionTitle ) )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertFalse( findTitle(    sAuctionTitle ) )
        #
        self.assertFalse( findExclude(  sAuctionTitle ) )
        #
