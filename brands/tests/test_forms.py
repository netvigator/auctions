# import inspect

from django.urls            import reverse

from core.utils             import maybePrint
from core.tests.base        import BaseUserWebTestCase, getUrlQueryStringOff

# Create your tests here.

from ..forms                import CreateBrandForm, UpdateBrandForm
from ..models               import Brand

from pyPks.Dict.Maintain    import purgeNoneValueItems



class TestFormValidation( BaseUserWebTestCase ):

    ''' Brand Form Tests '''
    # helpful:
    # https://stackoverflow.com/questions/2257958/django-unit-testing-for-form-edit

    def setUp(self):
        #
        super().setUp()
        #
        oBrand = Brand(
            cTitle = "Cadillac",
            cLookFor = "Caddy",
            iUser = self.user1 )
        oBrand.save()
        #
        self.iBrandID = oBrand.id
        #
        oBrand = Brand(
            cTitle = "IPC",
            cLookFor = "International Projector",
            iUser = self.user1 )
        oBrand.save()
        #


        self.loginWebTest()


    def test_swap_title_and_lookfor( self ):
        #
        '''should swap title and look for without error'''
        #
        # webtest style
        sUpdateURL  = reverse( 'brands:edit', args=(self.iBrandID,) )
        #
        oForm = self.app.get( sUpdateURL ).form
        #
        self.assertEqual( oForm['cTitle'  ].value, 'Cadillac')
        self.assertEqual( oForm['cLookFor'].value, 'Caddy'   )
        #
        oForm['cTitle']   = 'Caddy'
        oForm['cLookFor'] = 'Cadillac'
        #
        oResponse = oForm.submit()
        #
        self.assertEqual( oForm['cTitle'  ].value, 'Caddy'   )
        self.assertEqual( oForm['cLookFor'].value, 'Cadillac')
        #
        oBrand = Brand.objects.get( id = self.iBrandID )
        #
        self.assertEqual( oBrand.cTitle,  'Caddy'   )
        self.assertEqual( oBrand.cLookFor,'Cadillac')


    def test_Title_got_outside_parens(self):
        #
        '''text in parens is OK,
        but there must be some text outside the parens'''
        #
        dFormData = dict(
            cTitle      = '(Chevrolet)',
            iStars      = 5,
            iUser       = self.user1.id )
        #
        form = CreateBrandForm( data = dFormData )
        #
        self.assertFalse(form.is_valid())
        #
        '''
        if form.errors:
            for k, v in form.errors.items():
                maybePrint( k, ' -- ', v )
        else:
            maybePrint( 'no form errors above!' )
        '''
        #
        dFormData['cTitle'] = 'Chevrolet'
        #
        form = CreateBrandForm( data = dFormData )
        #
        self.assertTrue(form.is_valid())
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_save_redirect(self):
        #
        '''after saving the form, next page should be the detail'''
        #
        dFormData = dict(
            cTitle      = 'Chevrolet',
            iStars      = 5,
            iUser       = self.user1.id )
        #
        form = CreateBrandForm( data = dFormData )
        #
        self.assertTrue(form.is_valid())
        #
        form.instance.iUser = self.user1 # need this!
        form.save()
        oBrand = Brand.objects.get( cTitle = 'Chevrolet' )
        self.assertEqual(
            getUrlQueryStringOff( oBrand.get_absolute_url() )[0],
            reverse('brands:detail', kwargs={ 'pk': oBrand.id } ) )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

    def test_add_Title_already_there(self):
        #
        '''can add brand name not in there yet,
        cannot add a brand name already there'''
        #
        dFormData = dict(
            cTitle      = 'Cadillac',
            iStars      = 5,
            iUser       = self.user1.id )
        #
        form = CreateBrandForm( data = dFormData )
        ##
        form.user    = self.user1 # need this!
        #
        self.assertFalse( form.is_valid() )
        #
        dFormData['cTitle'] = 'Caddy'
        #
        form = CreateBrandForm( data = dFormData )
        ##
        form.user    = self.user1 # need this!
        #
        self.assertFalse( form.is_valid() )
        #
        dFormData = dict(
            cTitle      = 'International',
            cLookFor    = "International Servicemaster",
            iStars      = 5,
            iUser       = self.user1.id )
        #
        form = CreateBrandForm( data = dFormData )
        ##
        form.user    = self.user1 # need this!
        #
        ''' yes the errors are there
        maybePrint('')
        maybePrint( 'form.is_valid() returns', form.is_valid() )
        if form.errors:
            for k, v in form.errors.items():
                maybePrint( k, ' -- ', v )
        else:
            maybePrint( 'no form errors at bottom!' )
        #
        '''
        #
        self.assertTrue( form.is_valid() )
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )



    def test_change_Title_case_webtest_style( self ):
        #
        # webtest style
        sUpdateURL  = reverse( 'brands:edit', args=(self.iBrandID,) )
        #
        oForm = self.app.get( sUpdateURL ).form
        #
        self.assertEqual( oForm['cTitle'].value, 'Cadillac' )
        #
        oForm['cTitle']   = 'cadillac'
        #
        oResponse = oForm.submit()
        #
        self.assertEqual( oForm['cTitle'].value, 'cadillac' )
        #
        oBrand = Brand.objects.get( id = self.iBrandID )
        #
        self.assertEqual( oBrand.cTitle, 'cadillac' )
        #


    def test_change_Title_case_django_style( self ):
        #
        sUpdateURL  = reverse( 'brands:edit', args=(self.iBrandID,) )
        #
        oResponse   = self.client.get( sUpdateURL )
        #
        form        = oResponse.context['form'] # retrieve form data as dict
        #
        data = form.initial # form is unbound but contains data
        #
        self.assertEqual( data['cTitle'], 'Cadillac' )
        #
        purgeNoneValueItems( data )
        #
        data['cTitle']   = 'cadillac'
        #
        form = UpdateBrandForm( data = data )
        #
        self.assertTrue( form.is_valid() )
