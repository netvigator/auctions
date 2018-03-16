from django.test        import TestCase

from core.utils_testing import BaseUserTestCase

from ..utils_testing    import setUpBrandsCategoriesModels
from ..utils_ebay       import (
            _getModelRegExFinders4Test, _getCategoryRegExFinders4Test,
            _getBrandRegExFinders4Test, getFoundItemTester )


from brands.models      import Brand
from categories.models  import Category
from models.models      import Model



class findersStorageTest( setUpBrandsCategoriesModels ):
    
    #
    ''' test Finder Storage for Brands, Categories & Models '''
    
    #
    #oBrand      = Model.objects.get(    cTitle = "Cadillac"  )
    #oCategory   = Category.objects.get( cTitle = "Widgets"   )
    #oModel      = Model.objects.get(    cTitle = "Fleetwood" )
    #
    def test_BrandRegExFinderStorage(self):
        #
        t = _getBrandRegExFinders4Test( self.oBrand )
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
        
    

    def test_CategoryRegExFinderStorage(self):
        #
        t = _getCategoryRegExFinders4Test( self.oCategory )
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



    def test_ModelRegExFinderStorage(self):
        #
        t = _getModelRegExFinders4Test( self.oModel )
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

    def testBrandGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oBrand, dFinders )
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  foundItem(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertFalse(  foundItem(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertTrue(  foundItem(    sAuctionTitle ) )
        #
        foundItem = dFinders[ self.oBrand.pk ]
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  foundItem(    sAuctionTitle ) )
        #
        self.assertIn( self.oBrand.sRegExLook4Title,
                                    ( 'Cadillac|Caddy', 'Caddy|Cadillac') )
        self.assertEquals( 'golf',           self.oBrand.sRegExExclude )



    def testCategoryGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oCategory, dFinders )
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertTrue(  foundItem(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Gemini Jets 1/200 Delta MD-80 Widget Livery N956DL'
        #
        self.assertFalse(  foundItem(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertFalse(  foundItem(  sAuctionTitle ) )
        #
        foundItem = dFinders[ self.oCategory.pk ]
        #
        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertTrue(  foundItem(    sAuctionTitle ) )
        #
        self.assertIn( self.oCategory.sRegExLook4Title,
                                        ( 'Gizmo|Widget', 'Widget|Gizmo' ) )
        self.assertEquals( 'Delta',         self.oCategory.sRegExExclude )
        self.assertEquals( 'Gadget',        self.oCategory.sRegExKeyWords )


    def testModelGetFoundItemTester(self):
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oModel, dFinders )
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  foundItem(    sAuctionTitle ) )
        #
        sAuctionTitle = 'Easy Trek, Remote Controlled Caddy by Spin It Golf (Black)'
        #
        self.assertFalse(  foundItem(  sAuctionTitle ) )
        #
        sAuctionTitle = 'Elvis Presley 1955 Pink Caddy Fleetwood Series 60, Greenlight 12950 1/18 Diecast'
        #
        self.assertFalse(  foundItem(    sAuctionTitle ) )

        sAuctionTitle = 'WEATHER WIDGET GADGET FOR YOUR DESKTOP PC WINDOWS XP/VISTA/7/8'
        #
        self.assertFalse( foundItem(    sAuctionTitle ) )
        #
        foundItem = dFinders[ self.oModel.pk ]
        #
        sAuctionTitle = '1976 Cadillac Eldorado Fleetwood Bicentennial'
        #
        self.assertTrue(  foundItem(    sAuctionTitle ) )
        #
        self.assertIn( self.oModel.sRegExLook4Title,
                                ( 'Woodie|Fleetwood', 'Fleetwood|Woodie' ) )
        self.assertEquals( 'golf',              self.oModel.sRegExExclude )
        self.assertEquals( 'Eldorado',          self.oModel.sRegExKeyWords )

