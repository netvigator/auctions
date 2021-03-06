from django.urls        import reverse, resolve

from core.dj_import     import HttpRequest
from django.test.client import Client

from core.tests.base    import ( SetUpBrandsCategoriesModelsMixin,
                                 getSingleEbayCategoryMixin,
                                 getUrlQueryStringOff,
                                 BaseUserWebTestCase )

from ..forms            import CreateSearchForm, UpdateSearchForm
from ..models           import Search

from categories.models  import Category
from finders.models     import ItemFound

# from pprint import pprint

# Create your tests here.



class TestFormValidation(
        getSingleEbayCategoryMixin,
        SetUpBrandsCategoriesModelsMixin,
        BaseUserWebTestCase ):

    ''' Search Form Tests '''
    # helpful:
    # https://stackoverflow.com/questions/2257958/django-unit-testing-for-form-edit '''

    def test_save_redirect(self):
        #
        '''after saving the form, next page should be the detail'''
        #
        dFormData = dict(
            cTitle          = 'Great Widget 1',
            cPriority       = "A1",
            cKeyWords       = "Blah bleh blih",
            iUser           = self.user1.id )
        #
        form = CreateSearchForm( data = dFormData )
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
        dFormData = dict(
                cTitle          = "My clever search 3",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A2",
                iUser           = self.user1 )
        form = CreateSearchForm( data = dFormData )
        form.request = self.request
        if form.errors:
            print()
            print('form has at least one error:')
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        self.assertTrue( form.is_valid() )

        # has a category
        dFormData = dict(
                cTitle          = "My clever search 4",
                iDummyCategory  = 10, # see core.tests
                cPriority       = "A3",
                iUser           = self.user1 )
        form = CreateSearchForm( data = dFormData )
        form.request = self.request
        form.user    = self.user1
        self.assertTrue( form.is_valid() )

        # cPriority not good
        dFormData = dict(
                cTitle          = "My clever search 4",
                iDummyCategory  = 10, # see core.tests
                cPriority       = "A",
                iUser           = self.user1 )
        form = CreateSearchForm( data = dFormData )
        form.request = self.request
        self.assertFalse( form.is_valid() )

        # no key words, no category
        dFormData = dict(
                cTitle          = "My clever search 5",
                cPriority       = "A4",
                iUser           = self.user1 )
        form = CreateSearchForm( data = dFormData )
        form.request = self.request
        self.assertFalse( form.is_valid() )

        # has an invalid category
        dFormData = dict(
                cTitle          = "My clever search 6",
                iDummyCategory  = 'abc',
                cPriority       = "A5",
                iUser           = self.user1 )
        form = CreateSearchForm( data = dFormData )
        form.request = self.request
        self.assertFalse( form.is_valid() )

        # has an set My Category without an ebay category
        #
        oCategory = Category.objects.filter( cTitle = "Capacitor Checker" )[0]
        #
        dFormData = dict(
                cTitle          = "My clever search 7",
                cPriority       = "A6",
                iMyCategory     = oCategory.id,
                iUser           = self.user1 )
        form = CreateSearchForm( data = dFormData )
        form.request = self.request
        self.assertFalse( form.is_valid() )

        dFormData = dict(
                cTitle          = "My clever search 8",
                iDummyCategory  = 10, # see core.tests
                cPriority       = "A7",
                iMyCategory     = oCategory.id,
                iUser           = self.user1 )
        form = CreateSearchForm( data = dFormData )
        form.request = self.request
        self.assertTrue( form.is_valid() )


    def test_add_stuff_already_there(self):
        #
        dFormData = dict(
                cTitle          = "My clever search",
                cKeyWords       = "Blah bleh blih",
                cPriority       = "A8",
                iUser           = self.user1 )
        #
        form = CreateSearchForm(data=dFormData)
        form.request            = self.request
        form.instance.iUser     = self.user1
        self.assertTrue( form.is_valid() )
        form.save()
        #
        dFormData = dict(
                cTitle          = "Very clever search 1",
                cKeyWords       = "Blah bleh blih", # same as above
                cPriority       = "B1",
                iUser           = self.user1 )
        #
        form = CreateSearchForm( data = dFormData )
        form.request = self.request
        # self.assertFalse( form.is_valid() ) # cannot test for now
        #
        dFormData = dict(
                cTitle          = "Very clever search 2",
                cKeyWords       = "Blah blih bleh", # same but different order
                cPriority       = "B2",
                iUser           = self.user1 )
        #
        form = CreateSearchForm( data = dFormData )
        form.request = self.request
        self.assertTrue( form.is_valid() ) # not comparing sets yet
        #
        '''
        print( 'cTitle:', dFormData['cTitle'] )
        if form.errors:
            print('form has at least one error:')
            for k, v in form.errors.items():
                print( k, ' -- ', v )
        else:
            print( 'no form errors at bottom!' )
        '''
