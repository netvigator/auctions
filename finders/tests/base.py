from django.utils           import timezone

from ..models               import UserItemFound, UserFinder

from searching.tests.base   import ( StoreUserItemFoundWebTestBase,
                                     SetUpForHitStarsWebTests )

from brands.models          import Brand
from categories.models      import Category
from models.models          import Model

from searching.models       import Search


class SetupUserItemsFoundAndUserFindersWebTest( StoreUserItemFoundWebTestBase ):

    def setUp( self ):
        #
        '''set up to test _storeUserItemFound() with actual record'''
        #
        super().setUp()
        #
        self.loginWebTest()
        #
        self.oModel2 = Model(
            cTitle      = "Calais",
            cExcludeIf  = 'golf',
            iStars      = 1,
            iBrand      = self.oBrand,
            iCategory   = self.oCategory,
            iUser       = self.user1 )
        self.oModel2.save()
        #
        oUserItemFound = UserItemFound.objects.get(
                iItemNumb   = self.iItemNumb,
                iUser       = self.user1 )
        #
        oUserItemFound.iBrand   = self.oBrand
        oUserItemFound.iCategory= self.oCategory
        oUserItemFound.iModel   = self.oModel
        #
        oUserItemFound.iHitStars= (  self.oBrand.iStars *
                                     self.oModel.iStars *
                                     self.oCategory.iStars )
        #
        oUserItemFound.save()
        #
        oUserFinder = UserFinder(
                iItemNumb   = oUserItemFound.iItemNumb,
                iUser       = oUserItemFound.iUser,
                cTitle      = oUserItemFound.iItemNumb.cTitle )
        #
        oUserFinder.save() # need cuz UserItemFound.get_absolute_url()
        #
        self.oUserItemFound = oUserItemFound
        self.oUserFinder    = oUserFinder


class SetUpUserItemFoundWebTests( SetUpForHitStarsWebTests ):
    #
    def setUp( self ):
        #
        super().setUp()
        #
        oSample = UserFinder.objects.get(
            cTitle = 'Altec Lansing 288-8K High Frequency Drive MRII 542 Horn',
            iUser = self.user1 )
        #
        self.oSample   = oSample
        #
        oBrand = Brand.objects.get(
                cTitle = 'Altec-Lansing',
                iUser  = self.user1 )
        oModel = Model.objects.get(
                cTitle = '511A',
                iBrand = oBrand,
                iUser  = self.user1 )
        oCategory = Category.objects.get(
                cTitle = 'Horn',
                iUser  = self.user1 )
        #
        oSearch = Search.objects.all()[1]
        #
        oUserItemFound = UserItemFound(
                iItemNumb   = self.oSample.iItemNumb,
                iBrand      = oBrand,
                iModel      = oModel,
                iCategory   = oCategory,
                iUser       = self.user1,
                iSearch     = oSearch,
                tCreate     = timezone.now() )
        #
        oUserItemFound.save()
        #
        self.oUserItemFound = oUserItemFound
        self.oBrand         = oBrand
        self.oCategory      = oCategory
        #
