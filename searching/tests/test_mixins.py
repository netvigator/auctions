from django.core.urlresolvers import reverse

from ..models           import UserItemFound

from .test_utils        import storeUserItemFoundButDontTestYet

from models.models      import Model



class EditingUserItemFoundShouldRedoHitStars( storeUserItemFoundButDontTestYet ):
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


    def test_change_brand_recalculate_hitstars( self ):
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
        iExpectStars = (
                oUserItemFound.iModel.iStars *
                oUserItemFound.iBrand.iStars *
                oUserItemFound.iCategory.iStars )
        #
        self.assertEquals( oUserItemFound.iHitStars, iExpectStars )
        #
        update_url = reverse(
                'searching:item_found_edit', args=(oUserItemFound.id,) )
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
        #print('')
        #print( 'form.is_valid():', form.is_valid() )
        #print('searching data:')
        #pprint( data )
        #
        # POST to the form
        r = self.client.post( update_url, data )
        #
        # retrieve again
        r = self.client.get( update_url )
        #
        #pprint( r.context['form'] )
        self.assertEquals(
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
        self.assertEquals( oUserItemFound.iHitStars, iExpectStars )



