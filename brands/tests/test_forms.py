# import inspect

from django.urls        import reverse

from core.utils_test    import ( BaseUserWebTestCase, getUrlQueryStringOff,
                                 maybePrint )

# Create your tests here.

from ..forms            import CreateBrandForm, UpdateBrandForm
from ..models           import Brand




class TestFormValidation( BaseUserWebTestCase ):

    ''' Brand Form Tests '''
    # helpful:
    # https://stackoverflow.com/questions/2257958/django-unit-testing-for-form-edit

    def setUp(self):
        #
        super( TestFormValidation, self ).setUp()
        #
        oBrand = Brand(
            cTitle = "Cadillac", cLookFor = "Caddy", iUser = self.user1 )
        oBrand.save()

    def test_Title_got_outside_parens(self):
        #
        '''text in parens is OK,
        but there must be some text outside the parens'''
        #
        form_data = dict(
            cTitle      = '(Chevrolet)',
            iStars      = 5,
            iUser       = self.user1.id )
        #
        form = CreateBrandForm(data=form_data)
        form.request = self.request
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
        form_data['cTitle'] = 'Chevrolet'
        #
        form = CreateBrandForm(data=form_data)
        form.request = self.request
        self.assertTrue(form.is_valid())
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )


    def test_save_redirect(self):
        #
        '''after saving the form, next page should be the detail'''
        #
        form_data = dict(
            cTitle      = 'Chevrolet',
            iStars      = 5,
            iUser       = self.user1.id )
        #
        form = CreateBrandForm(data=form_data)
        form.request = self.request
        self.assertTrue(form.is_valid())
        #
        form.instance.iUser = self.user1
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
        form_data = dict(
            cTitle      = 'Cadillac',
            iStars      = 5,
            iUser       = self.user1.id )
        #
        # maybePrint( 'test_add_Title_already_there' )
        form = CreateBrandForm(data=form_data)
        form.request = self.request
        form.user    = self.user1
        #isFormValid = form.is_valid()
        #self.assertFalse( isFormValid )
        self.assertFalse( form.is_valid() )
        #
        form_data['cTitle'] = 'Caddy'
        #
        form = CreateBrandForm(data=form_data)
        form.request = self.request
        form.user    = self.user1
        #isFormValid = form.is_valid()
        #self.assertFalse( isFormValid )
        self.assertFalse( form.is_valid() )
        #
        ''' yes the errors are there
        maybePrint('')
        maybePrint( 'form.is_valid() returns', form.is_valid() )
        if form.errors:
            for k, v in form.errors.items():
                maybePrint( k, ' -- ', v )
        else:
            maybePrint( 'no form errors at bottom!' )
        '''
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )

