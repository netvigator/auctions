from django.urls        import reverse

from core.test_utils    import BaseUserTestCase


# Create your tests here.

from ..forms            import BrandForm
from ..models           import Brand




class TestFormValidation(BaseUserTestCase):
    
    ''' Brand Form Tests '''
    
    def setUp(self):
        #
        super( TestFormValidation, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')
        #
        oBrand = Brand(
            cTitle = "Cadillac", cLookFor = "Caddy", iUser = self.user1 )
        oBrand.save()

    def test_Title_got_outside_parens(self):
        #
        form_data = dict(
            cTitle      = '(Chevrolet)',
            iStars      = 5,
            iUser       = self.user1.id
            )
        #
        form = BrandForm(data=form_data)
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
        form_data['cTitle'] = 'Chevrolet'
        #
        form = BrandForm(data=form_data)
        form.request = self.request
        self.assertTrue(form.is_valid())
        
        ''' test save '''
        form.instance.iUser = self.user1
        form.save()
        oBrand = Brand.objects.get( cTitle = 'Chevrolet' )
        self.assertEqual(
            reverse('brands:detail', kwargs={ 'pk': oBrand.id } ),
            '/brands/%s/' % oBrand.id )
        

    def test_Title_not_there_already(self):
        #
        form_data = dict(
            cTitle      = 'Cadillac',
            iStars      = 5,
            iUser       = self.user1.id
            )
        #
        form = BrandForm(data=form_data)
        form.request = self.request
        self.assertFalse(form.is_valid())
        #
        form_data['cTitle'] = 'Caddy'
        #
        form = BrandForm(data=form_data)
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

