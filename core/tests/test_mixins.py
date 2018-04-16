from django.core.urlresolvers import reverse

from core.utils_test        import setUpBrandsCategoriesModels

from searching.utils_stars  import getFoundItemTester


class EditingTitleShouldBlankFinder( setUpBrandsCategoriesModels ):
    #
    ''' test WereAnyReleventRegExColsChangedMixin'''
    
    #
    #oBrand      = Model.objects.get(    cTitle = "Cadillac"  )
    #oCategory   = Category.objects.get( cTitle = "Widgets"   )
    #oModel      = Model.objects.get(    cTitle = "Fleetwood" )
    #

    def test_change_cTitle_blank_finder( self ):
        #
        ''' test WereAnyReleventRegExColsChangedMixin'''
        #
        self.loginWebTest()
        #
        dFinders  = {}
        #
        foundItem = getFoundItemTester( self.oBrand, dFinders )
        #
        bInTitle, bExcludeThis = foundItem( self.oBrand.cTitle )
        #
        self.assertIn( self.oBrand.cRegExLook4Title,
                            ( r'Cadillac|\bCaddy\b', r'\bCaddy\b|Cadillac') )
        #
        update_url = reverse( 'brands:edit', args=(self.oBrand.id,) )
        #
        # GET the form
        r = self.client.get(update_url)
        #
        form = r.context['form']
        data = form.initial # form is unbound but contains data
        #
        self.assertEqual( data['cLookFor'], 'Caddy')
        #
        # manipulate some data
        data['cLookFor'] = ''
        #
        # POST to the form
        r = self.client.post(update_url, data)
        #
        # retrieve again
        r = self.client.get(update_url)
        #
        self.assertEqual(r.context['form'].initial['cLookFor'], '')
        #
        form = self.app.get( update_url ).form
        #
        form['cLookFor'] = ''
        #
        response = form.submit()
        #
        self.oBrand.refresh_from_db()
        #
        self.assertIsNone( self.oBrand.cRegExLook4Title )



