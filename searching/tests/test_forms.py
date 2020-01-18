from django.urls        import reverse, resolve

from core.dj_import     import HttpRequest
from django.test.client import Client

from core.tests.base    import ( BaseUserWebTestCase,
                                 getSingleEbayCategoryMixin,
                                 getUrlQueryStringOff )

from ..forms            import CreateSearchForm, UpdateSearchForm
from ..models           import Search

from finders.models     import ItemFound

# from pprint import pprint

# Create your tests here.



class TestFormValidation( getSingleEbayCategoryMixin, BaseUserWebTestCase ):

    ''' Search Form Tests '''
    # helpful:
    # https://stackoverflow.com/questions/2257958/django-unit-testing-for-form-edit '''

    def test_save_redirect(self):
        #
        '''after saving the form, next page should be the detail'''
        #
        form_data = dict(
            cTitle          = 'Great Widget 1',
            cPriority       = "A1",
            cKeyWords       = "Blah bleh blih",
            which           = 'Create',
            iUser           = self.user1.id )
        #
        form = CreateSearchForm(data=form_data)
        form.request        = self.request
        form.instance.iUser = self.user1
        self.assertTrue( form.is_valid() )

        # test save
        form.save()
        oSearch = Search.objects.get( cTitle = 'Great Widget 1' )
        self.assertEqual(
            getUrlQueryStringOff( oSearch.get_absolute_url() )[0],
            reverse('searching:detail', kwargs={ 'pk': oSearch.id } ) )

    def test_form_valid(self):

        # has key words
        dData = dict(
                cTitle          = "My clever search 3",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A1",
                which           = 'Create',
                iUser           = self.user1 )
        form = CreateSearchForm( data = dData )
        form.request = self.request
        self.assertTrue( form.is_valid() )

        # has a category
        dData = dict(
                cTitle          = "My clever search 4",
                iDummyCategory  = 10, # see core.tests
                cPriority       = "A1",
                which           = 'Create',
                iUser           = self.user1 )
        form = CreateSearchForm( data = dData )
        form.request = self.request
        form.user    = self.user1
        self.assertTrue( form.is_valid() )

        # cPriority not good
        dData = dict(
                cTitle          = "My clever search 4",
                iDummyCategory  = 10, # see core.tests
                cPriority       = "A",
                which           = 'Create',
                iUser           = self.user1 )
        form = CreateSearchForm( data = dData )
        form.request = self.request
        self.assertFalse( form.is_valid() )

        # no key words, no category
        dData = dict(
                cTitle          = "My clever search 5",
                cPriority       = "A1",
                which           = 'Create',
                iUser           = self.user1 )
        form = CreateSearchForm( data = dData )
        form.request = self.request
        self.assertFalse( form.is_valid() )

        # has an invalid category
        dData = dict(
                cTitle          = "My clever search 6",
                iDummyCategory  = 'abc',
                cPriority       = "A2",
                which           = 'Create',
                iUser           = self.user1 )
        form = CreateSearchForm( data = dData )
        form.request = self.request
        self.assertFalse( form.is_valid() )



    def test_add_stuff_already_there(self):
        #
        dData = dict(
                cTitle          = "My clever search",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A2",
                which           = 'Create',
                iUser           = self.user1 )
        #
        form = CreateSearchForm(data=dData)
        form.request            = self.request
        form.instance.iUser     = self.user1
        form.save()
        #
        dData = dict(
                cTitle          = "Very clever search 1",
                cKeyWords       = "Blah bleh blih", # same as above
                which           = 'Create',
                cPriority       = "B1",
                iUser           = self.user1 )
        #
        form = CreateSearchForm( data = dData )
        form.request = self.request
        # self.assertFalse( form.is_valid() ) # cannot test for now
        #
        dData = dict(
                cTitle          = "Very clever search 2",
                cKeyWords       = "Blah blih bleh", # same but different order
                which           = 'Create',
                cPriority       = "B2",
                iUser           = self.user1 )
        #
        form = CreateSearchForm( data = dData )
        form.request = self.request
        self.assertTrue( form.is_valid() ) # not comparing sets yet

        #
        '''
        if form.errors:
            print('')
            print('form has at least one error:')
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors at bottom!' )
        '''
