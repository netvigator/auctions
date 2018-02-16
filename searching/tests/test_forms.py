from django.core.urlresolvers   import reverse, resolve
from django.http.request        import HttpRequest
from django.test.client         import Client

from core.tests                 import BaseUserTestCase

from .forms                     import SearchAddOrUpdateForm
from .models                    import Search, ItemFound

# from pprint import pprint

# Create your tests here.



class TestFormValidation(BaseUserTestCase):
    
    ''' Search Form Tests '''
    
    def setUp(self):
        #
        super( TestFormValidation, self ).setUp()
        #
        self.client = Client()
        self.client.login(username ='username1', password='mypassword')
        #
    '''
    def test_save_redirect(self):
        #
        form_data = dict(
            cTitle      = 'Great Widget',
            cPriority   = "A",
            cKeyWords   = "Blah bleh blih",
            iUser       = self.user1.id
            )
        #
        form = SearchAddOrUpdateForm(data=form_data)
        form.request = self.request
            #which           = 'Create',
        self.assertTrue( form.is_valid() )
        
        # test save
        form.instance.iUser = self.user1
        form.save()
        oSearch = Search.objects.get( cTitle = 'Great Widget' )
        self.assertEqual(
            reverse('searching:detail', kwargs={ 'pk': oSearch.id } ),
            '/searching/%s/' % oSearch.id )
    '''
    def test_stuff_in_there_already(self):
        #
        dData = dict(
                cTitle          = "My clever search",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        #
        form = SearchAddOrUpdateForm(data=dData)
        form.request            = self.request
        form.instance.iUser     = self.user1
        form.save()        
        #
        dData = dict(
                cTitle          = "Very clever search",
                cKeyWords       = "Blah bleh blih", # same as above
                which           = 'Create',
                cPriority       = "B",
                iUser           = self.user1 )
        #
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertFalse( form.is_valid() )
        #
        dData = dict(
                cTitle          = "Very clever search",
                cKeyWords       = "Blah blih bleh", # same but different order
                which           = 'Create',
                cPriority       = "B",
                iUser           = self.user1 )
        #
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertTrue( form.is_valid() ) # not comparing sets yet
        
        #
        '''
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors at bottom!' )
        '''
