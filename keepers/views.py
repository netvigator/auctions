from django.shortcuts   import render
from django.views       import generic

from core.mixins        import GetPaginationExtraInfoInContext

from core.views         import ( DeleteViewGotModel,
                                 DetailViewGotModel,  ListViewGotModel )

from .models            import Keeper



class KeeperIndexView(
            GetPaginationExtraInfoInContext, ListViewGotModel ):
    model               = Keeper
    template_name       = 'keeper/keepers_index.html'
    context_object_name = 'keepers_list'
    paginate_by         = 100


