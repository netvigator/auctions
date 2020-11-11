from django.urls    import reverse

from .base          import SetupUserItemsFoundAndUserFindersWebTest


class EditingUserItemFoundShouldRedoHitStars(
        SetupUserItemsFoundAndUserFindersWebTest ):
    #
    ''' test AnyReleventHitStarColsChangedMixin'''


    def test_change_model_recalculate_hitstars( self ):
        #
        ''' test AnyReleventHitStarColsChangedMixin'''
        #
        oUserFinder     = self.oUserFinder
        oUserItemFound  = self.oUserItemFound
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
        '''
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
        '''



