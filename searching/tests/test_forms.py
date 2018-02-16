from django.core.urlresolvers   import reverse, resolve
from django.http.request        import HttpRequest
from django.test.client         import Client

from core.tests                 import BaseUserTestCase

from ..forms                     import SearchAddOrUpdateForm
from ..models                    import Search, ItemFound

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

    def test_save_redirect(self):
        #
        form_data = dict(
            cTitle          = 'Great Widget 1',
            cPriority       = "A",
            cKeyWords       = "Blah bleh blih",
            which           = 'Create',
            iUser           = self.user1.id
            )
        #
        form = SearchAddOrUpdateForm(data=form_data)
        form.request        = self.request
        form.instance.iUser = self.user1
        self.assertTrue( form.is_valid() )
        
        # test save
        form.save()
        oSearch = Search.objects.get( cTitle = 'Great Widget 1' )
        self.assertEqual(
            reverse('searching:detail', kwargs={ 'pk': oSearch.id } ),
            '/searching/%s/' % oSearch.id )

    def test_form_valid(self):

        # has key words
        dData = dict(
                cTitle          = "My clever search 3",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertTrue( form.is_valid() )

        # has a category
        dData = dict(
                cTitle          = "My clever search 4",
                iDummyCategory  = 10, # see core.tests
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertTrue( form.is_valid() )

        # no key words, no category
        dData = dict(
                cTitle          = "My clever search 5",
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData ) 
        form.request = self.request
        self.assertFalse( form.is_valid() )

        # has an invalid category
        dData = dict(
                cTitle          = "My clever search 6",
                iDummyCategory  = 'abc',
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = SearchAddOrUpdateForm( data = dData )
        form.request = self.request
        self.assertFalse( form.is_valid() )



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
                cTitle          = "Very clever search 1",
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
                cTitle          = "Very clever search 2",
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
