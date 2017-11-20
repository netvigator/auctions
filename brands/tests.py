from django.test import TestCase

# Create your tests here.

from .models import Brand

class ModelModelTest(TestCase):

    def test_string_representation(self):
        sBrand = "My brand name"
        oBrand = Brand(ctitle= sBrand )
        self.assertEqual(str(sBrand), oBrand.ctitle)
