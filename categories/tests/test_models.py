from django.test                import TestCase


from ..models                   import Category


class CategoryModelTest(TestCase):

    def test_string_representation(self):
        sCategory = "This category"
        oCategory = Category( cTitle = sCategory )
        self.assertEqual(str(sCategory), oCategory.cTitle)
