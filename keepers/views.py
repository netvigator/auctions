from django.shortcuts   import render
from django.views       import generic

from core.mixins        import ( GetPaginationExtraInfoInContext,
                                 GetUserItemsTableMixin )

from core.views         import ( DeleteViewGotModel,
                                 DetailViewGotModel,  ListViewGotModel )

from .models            import Keeper, UserKeeper




class KeeperDetailView( GetUserItemsTableMixin, DetailViewGotModel ):

    model   = Keeper
    template_name = 'keepers/detail.html'

    def get_context_data(self, **kwargs):
        #
        context = super( KeeperDetailView, self).get_context_data(**kwargs )
        #
        #qs = self.object.getKeepersForThis( self.object, self.request )
        #
        #context['UserItemsTable'] = self.getUserItemsTable( qs )
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
        lUserKeeperNumbs = ( UserKeeper.objects.filter(
                                iUser = oUser )
                            .values_list( 'iItemNumb', flat = True )
                            .distinct() )
        #
        qsKeepers = Keeper.objects.filter(
                            iItemNumb__in = lUserKeeperNumbs
                            ).order_by( '-tTimeEnd' )
        #
        return qsKeepers
