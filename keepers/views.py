from django.shortcuts   import render
from django.views       import generic

from core.mixins        import GetPaginationExtraInfoInContext

from core.views         import ( DeleteViewGotModel,
                                 DetailViewGotModel,  ListViewGotModel )

from .models            import Keeper, UserKeeper




class KeeperDetailView( DetailViewGotModel ):

    model   = Keeper
    template_name = 'keepers/detail.html'



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
