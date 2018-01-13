from test_plus.test import TestCase
from core.tests     import getDefaultMarket


class TestUser(TestCase):

    def setUp(self):

        getDefaultMarket( self )

        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            'testuser'  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            '/users/testuser/'
        )
