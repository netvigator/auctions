from django.shortcuts   import render
from django.views       import generic

from core.mixins        import GetPaginationExtraInfoInContext

from core.views         import ( DeleteViewGotModel,
                                 DetailViewGotModel,  ListViewGotModel )

from .models            import Keeper



class KeeperListView(
            GetPaginationExtraInfoInContext, ListViewGotModel ):
    model               = Keeper
    template_name       = 'archive/items_index.html'
    context_object_name = 'items_list'
    paginate_by         = 100


