import logging

from django.core.urlresolvers   import reverse

from core.utils_test            import BaseUserWebTestCase

from core.utils                 import getExceptionMessageFromResponse

from ..models                   import Keeper

from ..views                    import KeeperIndexView



class KeepersViewsTests( BaseUserWebTestCase ):
    """Item views tests."""

    def test_no_items_yet(self):
        #
        """
        If no itemss exist, an appropriate message is displayed.
        """
        self.client.login(username='username1', password='mypassword')
        #
        response = self.client.get(reverse('keepers:index'))
        #
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['keeper_list'], [])
        #
        # not working yet!?
        self.assertContains(response, "No keepers are available.")
        #
        # print( 'ran %s' % inspect.getframeinfo( inspect.currentframe() ).function )
