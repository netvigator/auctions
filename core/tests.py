from django.test import TestCase

# Create your tests here.

from .utils     import oUserOne

class CoreUserTests(TestCase):
    """User tests."""

    def test_get_user(self):
        
        self.assertEquals( oUserOne.username, 'netvigator')


