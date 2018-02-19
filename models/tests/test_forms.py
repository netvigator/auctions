from django.core.urlresolvers   import reverse

from core.utils_testing         import BaseUserTestCase

from categories.models          import Category

from ..forms                    import ModelForm
from ..models                   import Model

# Create your tests here.


class TestFormValidation(BaseUserTestCase):
    
    ''' Model Form Tests '''
    
    def setUp(self):
        #
        super( TestFormValidation, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')
        #
        self.oCategory = Category(
            cTitle = "Widgets",
            iStars  = 5,
            iUser = self.user1 )
        self.oCategory.save()
        self.CategoryID = self.oCategory.id
        #
        oModel = Model(
            cTitle      = "Fleetwood",
            cLookFor    = "Woodie",
            iCategory   = self.oCategory,
            iUser       = self.user1 )
        oModel.save()
        
        # print( 'category ID:', self.CategoryID )

    def test_Title_got_outside_parens(self):
        #
        form_data = dict(
            cTitle      = '(LS3-5A)',
            iStars      = 5,
            iCategory   = self.CategoryID,
            iUser       = self.user1
            )
        #
        form = ModelForm(data=form_data)
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
        form = ModelForm(data=form_data)
        form.request = self.request
        self.assertTrue(form.is_valid())

        ''' test save '''
        form.instance.iUser = self.user1
        form.save()
        oModel = Model.objects.get( cTitle = 'LS3-5A' )
        self.assertEqual(
            reverse('models:detail', kwargs={ 'pk': oModel.id } ),
            '/models/%s/' % oModel.id )

        '''
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors at bottom!' )
        '''

    def test_Title_not_there_already(self):
        #
        form_data = dict(
            cTitle      = 'Fleetwood',
            iStars      = 5,
            iCategory   = self.CategoryID,
            iUser       = self.user1
            )
        #
        form = ModelForm(data=form_data)
        form.request = self.request
        self.assertFalse(form.is_valid())
        #
        form_data['cTitle'] = 'Woodie'
        #
        form = ModelForm(data=form_data)
        form.request = self.request
        self.assertFalse(form.is_valid())

