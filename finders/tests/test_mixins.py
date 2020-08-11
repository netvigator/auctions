from django.urls            import reverse

from ..models               import UserItemFound, UserFinder

from searching.tests.base   import StoreUserItemFoundWebTestBase

from models.models          import Model


class EditingUserItemFoundShouldRedoHitStars( StoreUserItemFoundWebTestBase ):
    #
    ''' test AnyReleventHitStarColsChangedMixin'''

    def setUp( self ):
        #
        '''set up to test _storeUserItemFound() with actual record'''
        #
        super( EditingUserItemFoundShouldRedoHitStars, self ).setUp()
        #
        self.oModel2 = Model(
            cTitle      = "Calais",
            cExcludeIf  = 'golf',
            iStars      = 1,
            iBrand      = self.oBrand,
            iCategory   = self.oCategory,
            iUser       = self.user1 )
        self.oModel2.save()


    def test_change_model_recalculate_hitstars( self ):
        #
        ''' test AnyReleventHitStarColsChangedMixin'''
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
        iExpectStars = (
                oUserItemFound.iModel.iStars *
                oUserItemFound.iBrand.iStars *
                oUserItemFound.iCategory.iStars )
        #
        self.assertEqual( oUserItemFound.iHitStars, iExpectStars )
        #
        update_url = reverse(
                'finders:edit', args=(oUserItemFound.id,) )
        #
        #print('')
        #print('update_url:', update_url )
        # update_url: /finders/1/edit/
        #
        # GET the form
        r = self.client.get( update_url )
        #
        form = r.context['form']
        data = form.initial # form is unbound but contains data
        #
        self.assertEqual( data['iModel'], self.oModel.id )
        #
        # manipulate some data
        data['iModel'] = self.oModel2.id
        #
        # ### testing no longer works, maybe cuz the extra field gModel ###
        # print('')
        # print( 'form.is_valid():', form.is_valid() )
        # print('searching data:')
        # pprint( data )
        #
        # POST to the form
        r = self.client.post( update_url, data )
        #
        # retrieve again
        r = self.client.get( update_url )
        #
        #pprint( r.context['form'] )
        self.assertEqual(
                r.context['form'].initial['iModel'], self.oModel2.id )
        #
        form = self.app.get( update_url ).form
        #
        form['iModel'] = self.oModel2.id
        #
        response = form.submit()
        #
        oUserItemFound.refresh_from_db()
        #
        iExpectStars = (
                oUserItemFound.iBrand.iStars *
                oUserItemFound.iCategory.iStars )
        #
        self.assertEqual( oUserItemFound.iHitStars, iExpectStars )



