from django.urls            import reverse

from core.tests.base        import SetUpBrandsCategoriesModelsWebTest, \
                                   SetUpBrandsCategoriesModelsTestPlus, \
                                   getUrlQueryStringOff

from categories.models      import Category

from ..forms                import CreateModelForm, UpdateModelForm
from ..models               import Model

from pyPks.Dict.Maintain    import purgeNoneValueItems



class TestFormValidationMixin( object ):

    def test_Title_got_outside_parens(self):
        #
        '''text in parens is OK,
        but there must be some text outside the parens'''
        #
        dFormData = dict(
            cTitle      = '(LS3-5A)',
            iStars      = 5,
            iCategory   = self.CategoryID,
            iUser       = self.user1 )
        #
        form = CreateModelForm( data = dFormData )
        form.request = self.request
        self.assertFalse(form.is_valid())
        #
        '''
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors above!' )
        '''
        #
        dFormData['cTitle'] = 'LS3-5A'
        #
        form = CreateModelForm( data = dFormData )
        form.request = self.request
        self.assertTrue(form.is_valid())

        '''
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors at bottom!' )
        '''

    def test_save_redirect(self):
        #
        '''after saving the form, next page should be the detail'''
        #
        dFormData = dict(
            cTitle      = 'LS3-5A',
            iStars      = 5,
            iCategory   = self.CategoryID,
            iUser       = self.user1 )
        #
        form = CreateModelForm( data = dFormData )
        form.request = self.request
        self.assertTrue(form.is_valid())
        #
        form.instance.iUser = self.user1
        form.save()
        oModel = Model.objects.get( cTitle = 'LS3-5A' )
        #
        self.assertEqual(
            getUrlQueryStringOff( oModel.get_absolute_url() )[0],
            reverse('models:detail', kwargs={ 'pk': oModel.id } ) )


    def test_add_Title_already_there(self):
        #
        '''can add model name/# not in there yet,
        cannot add a name/# already there'''
        #
        dFormData = dict(
            cTitle      = 'Fleetwood',
            iStars      = 5,
            iCategory_id= self.CategoryID,
            iUser_id    = self.user1.id )
        #
        form = CreateModelForm( data = dFormData )
        form.request = self.request
        self.assertFalse(form.is_valid())
        #
        dFormData['cTitle'] = 'Woodie'
        #
        form = CreateModelForm( data = dFormData )
        form.request = self.request
        self.assertFalse(form.is_valid())


class WebTestFormValidation(
        TestFormValidationMixin, SetUpBrandsCategoriesModelsWebTest ):

    ''' Model Form Tests '''
    # helpful:
    # https://stackoverflow.com/questions/2257958/django-unit-testing-for-form-edit
    #
    def setUp(self):
        #
        super().setUp()
        #
        self.loginWebTest()

    def test_swap_title_and_lookfor( self ):
        #
        '''should swap title and look for without error'''
        #
        # webtest style
        sUpdateURL  = reverse( 'models:edit', args=(self.iModelID,) )
        #
        oForm = self.app.get( sUpdateURL ).form
        #
        self.assertEqual( oForm['cTitle'  ].value, 'Fleetwood')
        self.assertEqual( oForm['cLookFor'].value, 'Woodie'   )
        #
        oForm['cTitle']   = 'Woodie'
        oForm['cLookFor'] = 'Fleetwood'
        #
        oResponse = oForm.submit()
        #
        self.assertEqual( oForm['cTitle'  ].value, 'Woodie' )
        self.assertEqual( oForm['cLookFor'].value, 'Fleetwood'      )
        #
        oModel = Model.objects.get( id = self.iModelID )
        #
        self.assertEqual( oModel.cTitle,  'Woodie' )
        self.assertEqual( oModel.cLookFor,'Fleetwood'      )


    def test_change_Title_case_webtest_style( self ):
        #
        # webtest style
        sUpdateURL  = reverse( 'models:edit', args=(self.iModelID,) )
        #
        oForm = self.app.get( sUpdateURL ).form
        #
        self.assertEqual( oForm['cTitle'].value, 'Fleetwood' )
        #
        oForm['cTitle']   = 'fleetwood'
        #
        oResponse = oForm.submit()
        #
        self.assertEqual( oForm['cTitle'  ].value, 'fleetwood' )
        #
        oModel = Model.objects.get( id = self.iModelID )
        #
        self.assertEqual( oModel.cTitle, 'fleetwood' )
        #



class TestPlusFormValidation(
        TestFormValidationMixin, SetUpBrandsCategoriesModelsTestPlus ):
    #
    def test_swap_title_and_lookfor( self ):
        #
        '''should swap title and look for without error'''
        #
        # django style
        #
        sUpdateURL  = reverse( 'models:edit', args=(self.iModelID,) )
        #
        oResponse   = self.client.get( sUpdateURL )
        #
        form        = oResponse.context['form'] # retrieve form data as dict
        #
        data = form.initial # form is unbound but contains data
        #
        self.assertEqual( data['cTitle'  ], 'Fleetwood')
        self.assertEqual( data['cLookFor'], 'Woodie'   )
        #
        purgeNoneValueItems( data )
        #
        data['cTitle'  ] = 'Woodie'
        data['cLookFor'] = 'Fleetwood'
        #
        form = UpdateModelForm( data = data )
        #
        self.assertTrue( form.is_valid() )


    def test_change_Title_case_django_style( self ):
        #
        sUpdateURL  = reverse( 'models:edit', args=(self.iModelID,) )
        #
        oResponse   = self.client.get( sUpdateURL )
        #
        form        = oResponse.context['form'] # retrieve form data as dict
        #
        data = form.initial # form is unbound but contains data
        #
        self.assertEqual( data['cTitle'], 'Fleetwood' )
        #
        purgeNoneValueItems( data )
        #
        data['cTitle']   = 'fleetwood'
        #
        form = UpdateModelForm( data = data )
        #
        self.assertTrue( form.is_valid() )


