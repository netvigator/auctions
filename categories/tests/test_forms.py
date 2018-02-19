from django.core.urlresolvers   import reverse

from core.utils_testing         import BaseUserTestCase

from ..models                   import Category
from ..forms                    import CategoryForm


class TestFormValidation(BaseUserTestCase):
    
    ''' Category Form Tests '''
    
    def setUp(self):
        #
        super( TestFormValidation, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')
        #
        oCategory = Category(
            cTitle = "Gadgets", cLookFor = "thingamajig", iUser = self.user1 )
        oCategory.save()

    def test_Title_got_outside_parens(self):
        #
        form_data = dict(
            cTitle      = '(Widgets)',
            iStars      = 5,
            iUser       = self.user1
            )
        #
        form = CategoryForm(data=form_data)
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
        form_data['cTitle'] = 'Widgets'
        #
        form = CategoryForm(data=form_data)
        form.request = self.request
        self.assertTrue(form.is_valid())

        ''' test save '''
        form.instance.iUser = self.user1
        form.save()
        oCategory = Category.objects.get( cTitle = 'Widgets' )
        self.assertEqual(
            reverse('categories:detail', kwargs={ 'pk': oCategory.id } ),
            '/categories/%s/' % oCategory.id )

    def test_Title_not_there_already(self):
        #
        form_data = dict(
            cTitle      = 'Gadgets',
            iStars      = 5,
            iUser       = self.user1
            )
        #
        form = CategoryForm(data=form_data)
        form.request = self.request
        self.assertFalse(form.is_valid())
        #
        form_data['cTitle'] = 'ThingaMaJig'
        #
        form = CategoryForm(data=form_data)
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

