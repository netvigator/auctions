from django.core.urlresolvers import reverse

from ..models           import UserItemFound

from .test_utils        import storeUserItemFoundButDontTestYet


class EditingUserItemFoundShouldRedoHitStars( storeUserItemFoundButDontTestYet ):
    #
    ''' test AnyReleventHitStarColsChangedMixin'''
    

    def test_remove_brand_zero_hitstars( self ):
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
        data['iModel'] = ''
        #
        # POST to the form
        r = self.client.post( update_url, data )
        #
        # retrieve again
        r = self.client.get( update_url )
        #
        self.assertIsNone( r.context['form'].initial['iModel'] )
        #
        form = self.app.get( update_url ).form
        #
        form['iModel'] = ''
        #
        response = form.submit()
        #
        oUserItemFound.refresh_from_db()
        #
        self.assertEquals( oUserItemFound.iHitStars, 0 )



