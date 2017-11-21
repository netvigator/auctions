from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory


# Create your tests here.

from .models        import Brand
from brands.views   import IndexView
from core.utils     import oUserOne


class ModelModelTest(TestCase):

    def test_string_representation(self):
        sBrand = "My brand name"
        oBrand = Brand(ctitle= sBrand )
        self.assertEqual(str(sBrand), oBrand.ctitle)


class BrandListViewTests(TestCase):
    """Brand list view tests."""

    def test_brands_in_the_context(self):

        client = Client()
        response = client.get('/')

        self.assertEquals(list(response.context['brand_list']), [])

        Brand.objects.create(ctitle='Chevrolet', iuser=oUserOne )
        response = client.get('/')
        self.assertEquals(response.context['brand_list'].count(), 1)

    def test_brands_in_the_context_request_factory(self):

        factory = RequestFactory()
        request = factory.get('/')

        response = IndexView.as_view()(request)

        self.assertEquals(list(response.context_data['brand_list']), [])

        Brand.objects.create(ctitle='Chevrolet', iuser=oUserOne )
        response = IndexView.as_view()(request)
        self.assertEquals(response.context_data['brand_list'].count(), 1)
