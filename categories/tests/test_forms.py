from django.core.urlresolvers   import reverse

from core.utils_test            import BaseUserWebTestCase, getUrlQueryStringOff

from ..models                   import Category
from ..forms                    import CreateCategoryForm, UpdateCategoryForm


class TestFormValidation( BaseUserWebTestCase ):

    ''' Category Form Tests '''
    # helpful:
    # https://stackoverflow.com/questions/2257958/django-unit-testing-for-form-edit

    def setUp(self):
        #
        super( TestFormValidation, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')
        #
        oCategory = Category(
            cTitle = "Gadget", cLookFor = "thingamajig", iUser = self.user1 )
        oCategory.save()
        #
        self.iCategoryID = oCategory.id

    def test_swap_title_and_lookfor( self ):
        #
        '''should swap title and look for without error'''
        #
        self.loginWebTest()
        #
        sUpdateURL  = reverse( 'categories:edit', args=(self.iCategoryID,) )
        #
        #oResponse   = self.client.get( sUpdateURL )
        ##
        #form        = oResponse.context['form'] # retrieve form data as dict
        ##
        #data = form.initial # form is unbound but contains data
        ##
        #print()
        #print( 'initial data:', data )
        ##
        #data['cTitle']   = 'thingamajig'
        #data['cLookFor'] = 'Gadget'
        ##
        #print()
        #print( 'updated data:', data )
        ##
        #oResponse = self.client.post( sUpdateURL, data )
        ##
        #print( 'form.is_valid():', form.is_valid() )
        ##
        #print( 'form.non_field_errors:', form.non_field_errors() )
        ## retrieve again
        #oResponse = self.client.get( sUpdateURL )
        ##
        #self.assertEqual(oResponse.context['form'].initial['cTitle'], 'thingamajig')
        #
        # webtest style
        oForm = self.app.get( sUpdateURL ).form
        #
        oForm['cTitle']   = 'thingamajig'
        oForm['cLookFor'] = 'Gadget'
        #
        oResponse = oForm.submit()
        #
        self.assertEqual( oForm['cTitle'  ].value, 'thingamajig' )
        self.assertEqual( oForm['cLookFor'].value, 'Gadget'      )


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
        form_data['cTitle'] = 'Widget'
        #
        form = CreateCategoryForm(data=form_data)
        form.request = self.request
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
        form.request = self.request
        self.assertTrue(form.is_valid())
        #
        form.instance.iUser = self.user1
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
        form.request = self.request
        form.user    = self.user1
        self.assertFalse(form.is_valid())
        #
        form_data = dict(
            cTitle      = 'ThingaMaJig',
            iStars      = 5,
            iUser       = self.user1.id )
        #
        form = CreateCategoryForm(data=form_data)
        form.request = self.request
        form.user    = self.user1
        isFormValid = form.is_valid()
        self.assertFalse( isFormValid )
        #
        '''
        print('')
        print( 'isFormValid:', isFormValid )
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors at bottom!' )
        '''

