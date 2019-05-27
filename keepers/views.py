from django.shortcuts   import render
from django.views       import generic

from core.mixins        import ( GetPaginationExtraInfoInContext,
                                 GetUserItemsTableMixin )

from core.views         import ( DeleteViewGotModel,
                                 DetailViewGotModel,  ListViewGotModel )

from finders.models     import UserItemFound

from .models            import Keeper




class KeeperDetailView( GetUserItemsTableMixin, DetailViewGotModel ):

    model   = Keeper
    template_name = 'keepers/detail.html'

    def get_context_data(self, **kwargs):
        #
        context = super( KeeperDetailView, self).get_context_data(**kwargs )
        #
        qs = self.object.getUserItemsFoundForKeeper(
                    self.object, self.request )
        #
        context['UserItemsTable'] = self.getUserItemsTable( qs )
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
