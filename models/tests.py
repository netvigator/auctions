from django.test import TestCase

from .models import Model

# Create your tests here.

'''
no views implemented yet
class ModelsViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/models/')
        self.assertEqual(resp.status_code, 200)
'''


class ModelModelTest(TestCase):

    def test_string_representation(self):
        sModel = "My model name/number"
        oModel = Model(cTitle= sModel )
        self.assertEqual(str(sModel), oModel.cTitle)
