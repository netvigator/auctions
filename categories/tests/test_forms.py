from django.urls            import reverse

from core.utils             import maybePrint
from core.tests.base        import BaseUserWebTestCase, getUrlQueryStringOff

from .base                  import TestCategoryFormValidation

from ..models               import Category
from ..forms                import CreateCategoryForm, UpdateCategoryForm

from pyPks.Dict.Maintain    import purgeNoneValueItems


class TestFormValidation( TestCategoryFormValidation ):

    ''' Category Form Tests '''
    # helpful:
    # https://stackoverflow.com/questions/2257958/django-unit-testing-for-form-edit

    def test_swap_title_and_lookfor( self ):
        #
        '''should swap title and look for without error'''
        #
        # webtest style
        sUpdateURL  = reverse( 'categories:edit', args=(self.iCategoryID,) )
        #
        oForm = self.app.get( sUpdateURL ).form
        #
        self.assertEqual( oForm['cTitle'  ].value, 'Gadget'      )
        self.assertEqual( oForm['cLookFor'].value, 'thingamajig' )
        #
        oForm['cTitle']   = 'thingamajig'
        oForm['cLookFor'] = 'Gadget'
        #
        oResponse = oForm.submit()
        #
        self.assertEqual( oForm['cTitle'  ].value, 'thingamajig' )
        self.assertEqual( oForm['cLookFor'].value, 'Gadget'      )
        #
        oCategory = Category.objects.get( id = self.iCategoryID )
        #
        self.assertEqual( oCategory.cTitle,  'thingamajig' )
        self.assertEqual( oCategory.cLookFor,'Gadget'      )


    def test_Title_got_outside_parens(self):
        #
        '''text in parens is OK,
        but there must be some text outside the parens'''
        #
        form_data = dict(
            cTitle      = '(Widget)',
            iStars      = 5,
            iUser       = self.user1 )
        #
        form = CreateCategoryForm(data=form_data)
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
        form_data['cTitle'] = 'Widget'
        #
        form = CreateCategoryForm(data=form_data)
        #
        self.assertTrue(form.is_valid())


    def test_save_redirect(self):
        #
        '''after saving the form, next page should be the detail'''
        #
        form_data = dict(
            cTitle      = 'Widget',
            iStars      = 5,
            iUser       = self.user1 )
        #
        form = CreateCategoryForm(data=form_data)
        #
        self.assertTrue(form.is_valid())
        #
        form.instance.iUser = self.user1 # need this!
        form.save()
        oCategory = Category.objects.get( cTitle = 'Widget' )
        self.assertEqual(
            getUrlQueryStringOff( oCategory.get_absolute_url() )[0],
            reverse('categories:detail', kwargs={ 'pk': oCategory.id } ) )


    def test_add_Title_already_there(self):
        #
        '''can add category not in there yet,
        cannot add a category already there'''
        #
        form_data = dict(
            cTitle      = 'Gadget',
            iStars      = 5,
            iUser       = self.user1 )
        #
        form = CreateCategoryForm(data=form_data)
        #
        form.user    = self.user1 # need this!
        #
        self.assertFalse( form.is_valid() )
        #
        form_data = dict(
            cTitle      = 'ThingaMaJig',
            iStars      = 5,
            iUser       = self.user1.id )
        #
        form = CreateCategoryForm(data=form_data)
        #
        form.user    = self.user1 # need this!
        #
        self.assertFalse( form.is_valid() )
        #
        sErrMsg = (
                'Cannot put ThingaMaJig in category name, ThingaMaJig '
                'is already in Look_For for category name Gadget' )
        #
        self.assertIn( sErrMsg, form.errors['cLookFor'] )
        #
        '''
        maybePrint('')
        maybePrint( 'isFormValid:', isFormValid )
        if form.errors:
            for k, v in form.errors.items():
                maybePrint( k, ' -- ', v )
        else:
            maybePrint( 'no form errors at bottom!' )
        '''

    def test_change_Title_case_webtest_style( self ):
        #
        # webtest style
        sUpdateURL  = reverse( 'categories:edit', args=(self.iCategoryID,) )
        #
        oForm = self.app.get( sUpdateURL ).form
        #
        self.assertEqual( oForm['cTitle'].value, 'Gadget' )
        #
        oForm['cTitle']   = 'gadget'
        #
        oResponse = oForm.submit()
        #
        self.assertEqual( oForm['cTitle'  ].value, 'gadget' )
        #
        oCategory = Category.objects.get( id = self.iCategoryID )
        #
        self.assertEqual( oCategory.cTitle, 'gadget' )
        #


    def test_change_Title_case_django_style( self ):
        #
        sUpdateURL  = reverse( 'categories:edit', args=(self.iCategoryID,) )
        #
        oResponse   = self.client.get( sUpdateURL )
        #
        form        = oResponse.context['form'] # retrieve form data as dict
        #
        data = form.initial # form is unbound but contains data
        #
        self.assertEqual( data['cTitle'], 'Gadget' )
        #
        purgeNoneValueItems( data )
        #
        data['cTitle']   = 'gadget'
        #
        form = UpdateCategoryForm( data = data )
        #
        self.assertTrue( form.is_valid() )
        ## retrieve again
        #oResponse = self.client.get( sUpdateURL )
        ##
        #self.assertEqual(oResponse.context['form'].initial['cTitle'], 'thingamajig')
        '''
        print()
        print( 'initial data:', data )
        #
        #data['cLookFor'] = 'Gadget'
        ##
        print()
        print( 'updated data:', data )
        print( 'form.is_bound:', form.is_bound )
        print( 'form.is_valid():', form.is_valid() )
        #
        maybePrint('')
        if form.errors:
            for k, v in form.errors.items():
                maybePrint( k, ' -- ', v )
        else:
            maybePrint( 'no form errors at bottom!' )
        #print( 'form.non_field_errors:', form.non_field_errors() )
        oCategory = Category.objects.get( id = self.iCategoryID )
        #
        oForm = UpdateCategoryForm( instance = oCategory )
        #
        print( 'oForm.instance.cTitle:', oForm.instance.cTitle )
        oForm.instance.cTitle = 'gadget'
        oForm.user            = self.user1
        #
        '''
