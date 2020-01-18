import logging

from django.urls        import reverse

from core.tests.base    import BaseUserWebTestCase

from core.utils         import getExceptionMessageFromResponse

from ..models           import Keeper

from ..views            import KeeperIndexView



class KeepersViewsTests( BaseUserWebTestCase ):
    """Item views tests."""

    def test_no_items_yet(self):
        #
        """
        If no itemss exist, an appropriate message is displayed.
        """
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
