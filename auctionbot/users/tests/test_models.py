
from core.tests.base        import getDefaultMarket

from core.tests.base_class  import TestCasePlus


class TestUser( TestCasePlus ):

    def setUp(self):

        self.market = getDefaultMarket()

        self.user   = self.make_user()

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
