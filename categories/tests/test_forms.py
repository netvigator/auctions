from django.core.urlresolvers   import reverse

from core.utils_test            import BaseUserTestCase, getUrlQueryStringOff

from ..models                   import Category
from ..forms                    import CreateCategoryForm, UpdateCategoryForm


class TestFormValidation(BaseUserTestCase):
    
    ''' Category Form Tests '''
    
    def setUp(self):
        #
        super( TestFormValidation, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')
        #
        oCategory = Category(
            cTitle = "Gadget", cLookFor = "thingamajig", iUser = self.user1 )
        oCategory.save()

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
        self.assertFalse(form.is_valid())
        #
        form_data['cTitle'] = 'ThingaMaJig'
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
            print( 'no form errors at bottom!' )
        '''

