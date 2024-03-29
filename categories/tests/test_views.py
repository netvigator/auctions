import logging

from django.test        import Client
from django.urls        import reverse

from core.tests.base    import BaseUserWebTestCase, BaseUserTestPlusCase

from core.utils         import getExceptionMessageFromResponse

from ..models           import Category
from ..views            import CategoryCreateView


class CategoryViewsTests( BaseUserWebTestCase ):
    """Category views tests."""

    urls = '.urls'

    def test_no_categories_yet(self):
        #
        """
        If no categories exist, an appropriate message is displayed.
        """
        #
        response = self.client.get(reverse('categories:index'))
        #response = self.client.get('/categories/')

        #pprint( 'printing response:')
        #pprint( response )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['category_list'], [])
        self.assertContains(response, "No categories are available.")


    def test_got_categories(self):
        #
        """
        If categories exist, an appropriate message is displayed.
        """
        logging.disable(logging.CRITICAL)
        #
        oCategory = Category( cTitle = "Widgets", iUser = self.user1 )
        oCategory.save()

        oCategory = Category( cTitle = "Gadget", iUser = self.user1 )
        oCategory.save()
        iGadgetID = oCategory.id

        response = self.client.get(reverse('categories:index'))
        #response = self.client.get('/categories/')

        #pprint( 'printing response:')
        #pprint( response )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['category_list'],
                ['<Category: Widgets>', '<Category: Gadget>'],
                ordered=False )
        self.assertContains(response, "Gadget")

        #print( 'iGadgetID:', iGadgetID )

        response = self.client.get(
                reverse( 'categories:detail', kwargs={ 'pk': iGadgetID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gadget")

        self.client.logout()
        self.client.login(username='username2', password='mypassword')

        response = self.client.get(
                reverse( 'categories:edit', kwargs={ 'pk': iGadgetID } ) )

        self.assertEqual(response.status_code, 403) # forbidden
        self.assertEqual(
            getExceptionMessageFromResponse( response ),
            "Permission Denied -- that's not your record!" )

        self.client.logout()
        self.client.login(username='username3', password='mypassword')

        response = self.client.get(
                reverse( 'categories:detail', kwargs={ 'pk': iGadgetID } ) )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gadget")

        """
        Not logged in, cannot see form, direct to login page.
        """
        self.client.logout()
        response = self.client.get(reverse('categories:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/categories/')

        logging.disable(logging.NOTSET)



class CategoryViewsHitButtonsWebTest( BaseUserWebTestCase ):
    """
    Test Save and Cancel
    """


    def test_get(self):
        """
        Test GET requests
        """
        request = self.factory.get(reverse('categories:add'))
        request.user = self.user1
        #
        response = CategoryCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        #print( 'response.context_data has form and view, view keys:' )
        #for k in response.context_data['view'].__dict__:
            #print( k )
        #self.assertEqual(response.context_data['iUser'], self.user1)
        self.assertEqual(response.context_data['view'].__dict__['request'], request)


    # @patch('categories.models.Category.save', MagicMock(name="save"))
    def test_add_post(self):
        """
        Test post requests
        """
        data = dict(
            cTitle      = "Widgets",
            iUser       = self.user1 )
        # Create the request
        response = self.client.post( reverse('categories:add'), data )
        # import pdb; pdb.set_trace()
        self.assertEqual( response.status_code, 200 )
        #oCategory = Category.objects.get( cTitle = "Great Widget" )
        #self.assertEqual( oCategory, self.categories )

        #request = self.factory.get(reverse('categories:add'))
        #request.user = self.user1

        #response = self.client.post( request, data )

        #print( 'response.status_code:', response.status_code )


    def test_add_hit_cancel(self):
        #
        """
        Hit cancel when adding
        """
        data = dict(
            cTitle      = "Widgets",
            iUser       = self.user1,
            Cancel      = True )
        # Create the request
        response = self.client.post( reverse('categories:add'), data )
        #print( 'response.status_code:', response.status_code )
        #print( 'response.__dict__:' )
        #pprint( response.__dict__ )
        self.assertEqual( response.status_code, 200 )
        # self.assertRedirects( response, reverse( 'categories:index' ) )

    def test_search_create_view(self):
        #
        request = self.factory.get(reverse('categories:add'))
        request.user = self.user1
        #request.POST._mutable = True
        #request.POST['cancel'] = True
        #
        response = CategoryCreateView.as_view()(request)
        #
        # print( 'type( request.POST ):', type( request.POST ) )
        #
        self.assertEqual(response.status_code, 200 )
        #print( 'response.template_name:' )
        #print( response.template_name ) ['categories/add.html']
        #
    #

    # @patch('categories.models.Category.save', MagicMock(name="save"))
    def test_edit_post(self):
        """
        Test post requests
        """
        sCategory = "Widgets"
        oCategory = Category( cTitle= sCategory, iUser = self.user1 )
        oCategory.save()
        #
        data = dict(
            cTitle      = "Gadget",
            iUser       = self.user1 )
        # Create the request
        response = self.client.post(
                reverse('categories:edit', kwargs={'pk': oCategory.id} ), data )
        # import pdb; pdb.set_trace()
        self.assertEqual( response.status_code, 200 )
        #
        #response = self.client.post( request, data )




    def test_edit_hit_cancel(self):
        #
        """
        Hit cancel when adding
        """
        sCategory = "Widgets"
        oCategory = Category( cTitle= sCategory, iUser = self.user1 )
        oCategory.save()
        #
        data = dict(
            cTitle      = "Gadget",
            iUser       = self.user1,
            Cancel      = True )
        # Create the request
        response = self.client.post(
                reverse('categories:edit', kwargs={'pk': oCategory.id} ), data )
        #print( 'response.status_code:', response.status_code )
        #print( 'response.__dict__:' )
        #pprint( response.__dict__ )
        self.assertEqual( response.status_code, 200 )
        # self.assertRedirects( response, reverse( 'categories:index' ) )



class CategoryViewTestDjangoStyle( BaseUserTestPlusCase ):


    def test_edit_set_ModelsByYear(self):
        #
        """
        set a category to bModelsByYear
        """
        #
        #
        sCategory = "Widgets"
        oCategory = Category( cTitle = sCategory, iUser = self.user1 )
        oCategory.save()
        #
        data = dict(
            cTitle          = "Gadget",
            iUser           = self.user1,
            bModelsByYear   = True )
        # Create the request
        #sURL = reverse( 'categories:edit', kwargs={ 'pk': oCategory.id } )
        sURL = self.reverse('categories:edit', pk = oCategory.id )
        #print( 'sURL:', sURL )
        #c = Client()
        response = self.client.post( path = sURL, data = data )

        #print( 'response.status_code:', response.status_code )
        #print( 'response.__dict__:' )
        #pprint( response.__dict__ )
        self.assertEqual( response.status_code, 200 )
        # self.assertRedirects( response, reverse( 'categories:index' ) )
        # print( 'after post, oCategory.bModelsByYear =', oCategory.bModelsByYear )
        # self.assertTrue( 'needsModelYears' in self.request.session )
        #data = dict( bModelsByYear = True )
        #
        #response = self.client.post(
                #reverse('categories:edit', kwargs={'pk': oCategory.id} ), data )
        #
        # sURL = reverse('categories:edit', kwargs={'pk': oCategory.id} )
        #self.assertEqual(form["bModelsByYear"].value, False)
        # print( 'dir( response ):', dir( response ) )
        #print( 'response.request.session:', response.request.session )

