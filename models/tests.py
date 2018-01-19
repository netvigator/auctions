from django.core.urlresolvers   import reverse, resolve
from django.test                import TestCase

from core.tests                 import getDefaultMarket, BaseUserTestCase
from categories.models          import Category

from .models                    import Model

# Create your tests here.

'''
no views implemented yet
class ModelsViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/models/')
        self.assertEqual(resp.status_code, 200)
'''


class TestURLs(BaseUserTestCase):

    def test_get_absolute_url(self):
        
        oCategory           = Category.objects.get( pk = 1 )
        
        oModel = Model(
            cTitle          = "My stellar model",
            iUser           = self.user1,
            iCategory       = oCategory,
            id              = 1 )
        oModel.save()
            
        self.assertEqual(
            oModel.get_absolute_url(),
            '/models/1/'
        )

    def test_list_reverse(self):
        """searches:index should reverse to /models/."""
        self.assertEqual(reverse('models:index'), '/models/')


    def test_list_resolve(self):
        """/models/ should resolve to models:index."""
        self.assertEqual(resolve('/models/').view_name, 'models:index')

    def test_detail_reverse(self):
        """models:detail should reverse to /models/<pk>/."""
        self.assertEqual(
            reverse('models:detail', kwargs={ 'pk': 1 }),
            '/models/1/'
        )

    def test_edit_reverse(self):
        """models:edit should reverse to /models/edit/."""
        self.assertEqual(reverse('models:edit', kwargs={ 'pk': 1 }),
                         '/models/1/edit/')

    def test_update_resolve(self):
        """/models/~update/ should resolve to models:update."""
        self.assertEqual(
            resolve('/models/1/edit/').view_name,
            'models:edit'
        )


class ModelModelTest(TestCase):

    def test_string_representation(self):
        sModel = "My model name/number"
        oModel = Model(cTitle= sModel )
        self.assertEqual(str(sModel), oModel.cTitle)
