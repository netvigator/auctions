import logging

from django.core.urlresolvers   import reverse

from core.utils_test            import BaseUserTestCase

from core.utils                 import getExceptionMessageFromResponse

from ..models                   import Keeper

from ..views                    import KeeperListView



class KeepersViewsTests(BaseUserTestCase):
    """Item views tests."""

    def not_yet_test_no_items_yet(self):
        #
        """
        If no itemss exist, an appropriate message is displayed.
        """
        self.client.login(username='username1', password='mypassword')
        #
        response = self.client.get(reverse('items:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['item_list'], [])
        self.assertContains(response, "No items are available.")
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
