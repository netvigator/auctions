from django.shortcuts   import render
from django.views       import generic

from core.mixins        import GetPaginationExtraInfoInContext, FindUserMixin

from core.views         import ( DeleteViewGotModel,
                                 DetailViewGotModel,  ListViewGotModel )

from searching.models   import UserItemFound

from .models            import Keeper




class KeeperDetailView( DetailViewGotModel ):

    model   = Keeper
    template_name = 'keepers/detail.html'



class KeeperIndexView( FindUserMixin,
            GetPaginationExtraInfoInContext, ListViewGotModel ):
    model               = Keeper
    template_name       = 'keepers/index.html'
    context_object_name = 'keeper_list'
    paginate_by         = 100

    def get_queryset(self):
        #
        oUser = self.findUser()
        #
        qsUserItemNumbs = ( UserItemFound.objects.filter(
                                iUser               = oUser )
                            .values_list( 'iItemNumb', flat = True )
                            .distinct() )
        #
        qsKeepers = Keeper.objects.filter(
                            iItemNumb__in = qsUserItemNumbs
                            ).order_by( '-tTimeEnd' )
        #
        return qsKeepers
