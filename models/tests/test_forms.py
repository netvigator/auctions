from django.core.urlresolvers   import reverse

from core.utils_test            import ( SetUpBrandsCategoriesModelsWebTest,
                                         SetUpBrandsCategoriesModelsTestPlus,
                                         getUrlQueryStringOff )

from categories.models          import Category

from ..forms                    import CreateModelForm, UpdateModelForm
from ..models                   import Model



class TestFormValidationMixin( object ):

    def test_Title_got_outside_parens(self):
        #
        '''text in parens is OK,
        but there must be some text outside the parens'''
        #
        form_data = dict(
            cTitle      = '(LS3-5A)',
            iStars      = 5,
            iCategory   = self.CategoryID,
            iUser       = self.user1 )
        #
        form = CreateModelForm(data=form_data)
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
        form_data['cTitle'] = 'LS3-5A'
        #
        form = CreateModelForm(data=form_data)
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
        form_data = dict(
            cTitle      = 'LS3-5A',
            iStars      = 5,
            iCategory   = self.CategoryID,
            iUser       = self.user1 )
        #
        form = CreateModelForm(data=form_data)
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
        form_data = dict(
            cTitle      = 'Fleetwood',
            iStars      = 5,
            iCategory_id= self.CategoryID,
            iUser_id    = self.user1.id )
        #
        form = CreateModelForm(data=form_data)
        form.request = self.request
        self.assertFalse(form.is_valid())
        #
        form_data['cTitle'] = 'Woodie'
        #
        form = CreateModelForm(data=form_data)
        form.request = self.request
        self.assertFalse(form.is_valid())


class WebTestFormValidation(
        TestFormValidationMixin, SetUpBrandsCategoriesModelsWebTest ):

    ''' Model Form Tests '''
    # helpful:
    # https://stackoverflow.com/questions/2257958/django-unit-testing-for-form-edit
    pass



class TestPlusFormValidation(
        TestFormValidationMixin, SetUpBrandsCategoriesModelsTestPlus ):
    pass


