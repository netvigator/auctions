from django.shortcuts   import render
from django.views       import generic

from core.mixins        import GetPaginationExtraInfoInContext

from core.views         import ( DeleteViewGotModel,
                                 DetailViewGotModel,  ListViewGotModel )

from finders.models     import UserItemFound

from .models            import Keeper




class KeeperDetailView( DetailViewGotModel ):

    model   = Keeper
    template_name = 'keepers/detail.html'

    def get_context_data(self, **kwargs):
        #
        context = super( KeeperDetailView, self).get_context_data(**kwargs )
        #
        context['user_items_list'] = \
            self.object.getUserItemsFoundForKeeper(
                    self.object, self.request )
        #
        return context


class KeeperIndexView( GetPaginationExtraInfoInContext, ListViewGotModel ):
    model               = Keeper
    template_name       = 'keepers/index.html'
    context_object_name = 'keeper_list'
    paginate_by         = 100

    def get_queryset(self):
        #
        oUser = self.request.user
        #
        qsUserItemNumbs = ( UserItemFound.objects.filter(
                                iUser = oUser )
                            .values_list( 'iItemNumb', flat = True )
                            .distinct() )
        #
        qsKeepers = Keeper.objects.filter(
                            iItemNumb__in = qsUserItemNumbs
                            ).order_by( '-tTimeEnd' )
        #
        return qsKeepers
