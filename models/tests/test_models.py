from django.test                import TestCase

from ..models                   import Model

class ModelModelTest(TestCase):

    def test_string_representation(self):
        sModel = "My model name/number"
        oModel = Model(cTitle= sModel )
        self.assertEqual(str(sModel), oModel.cTitle)

