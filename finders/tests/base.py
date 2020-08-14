from ..models               import UserItemFound, UserFinder

from searching.tests.base   import StoreUserItemFoundWebTestBase

from models.models          import Model


class SetupUserItemsFoundAndUserFinders( StoreUserItemFoundWebTestBase ):

    def setUp( self ):
        #
        '''set up to test _storeUserItemFound() with actual record'''
        #
        super().setUp()
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
        self.loginWebTest()
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
                iUser       = oUserItemFound.iUser )
        #
        oUserFinder.save() # need cuz UserItemFound.get_absolute_url()
        #
        self.oUserItemFound = oUserItemFound
        self.oUserFinder    = oUserFinder
