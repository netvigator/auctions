from django.test            import RequestFactory

from core.tests.base        import getDefaultMarket

from core.tests.base_class  import TestCasePlus

from ..views                import UserRedirectView, UserUpdateView


class BaseUserTestCasePlus( TestCasePlus ):

    def setUp(self):
        self.market = getDefaultMarket()
        self.user   = self.make_user()
        self.factory= RequestFactory()


class TestUserRedirectView( BaseUserTestCasePlus ):

    def test_get_redirect_url(self):
        # Instantiate the view directly. Never do this outside a test!
        view = UserRedirectView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        view.request = request
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            view.get_redirect_url(),
            '/users/testuser/'
        )


class TestUserUpdateView( BaseUserTestCasePlus ):

    def setUp(self):
        # call BaseUserTestCasePlus.setUp()
        super().setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = UserUpdateView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        self.view.request = request

    def test_get_success_url(self):
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            self.view.get_success_url(),
            '/users/testuser/'
        )

    def test_get_object(self):
        # Expect: self.user, as that is the request's user object
        self.assertEqual(
            self.view.get_object(),
            self.user
        )
