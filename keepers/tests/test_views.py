import logging

from django.core.urlresolvers   import reverse

from core.utils_test            import BaseUserTestCase

from core.utils                 import getExceptionMessageFromResponse

from ..models                   import Keeper

from ..views                    import KeeperIndexView



class KeepersViewsTests(BaseUserTestCase):
    """Item views tests."""

    def test_no_items_yet(self):
        #
        """
        If no itemss exist, an appropriate message is displayed.
        """
        self.client.login(username='username1', password='mypassword')
        #
        response = self.client.get(reverse('keepers:index'))

        print('')
        print( response )
        print('')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['keeper_list'], [])
        #
        # not working yet!? self.assertContains(response, "No keepers are available.")
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
