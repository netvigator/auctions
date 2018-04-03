from core.views     import ( CreateViewCanCancel, DeleteViewGotModel,
                             DetailViewGotModel,  ListViewGotModel,
                             UpdateViewCanCancel )

from django.http    import HttpResponseRedirect
from django.urls    import reverse_lazy

from django.core.urlresolvers   import reverse

from .forms         import ( ItemFoundForm, UserItemFoundForm,
                             CreateSearchForm, UpdateSearchForm )

import searching.utils

from .mixins        import SearchViewSuccessPostFormValidMixin
from .models        import Search, ItemFound, UserItemFound
from .utils         import getHowManySearchDigitsNeeded


tModelFields = (
    'cTitle',
    'cKeyWords',
    'iDummyCategory',
    'cPriority', )


class SearchCreateView( SearchViewSuccessPostFormValidMixin, CreateViewCanCancel ):

    model           = Search
    template_name   = 'searching/add.html'
    success_message = 'New Search record successfully saved!!!!'
    form_class      = CreateSearchForm

    success_message = 'New Search record successfully saved!!!!'


class SearchIndexView( ListViewGotModel ):  
    
    template_name   = 'searching/index.html'
    model           = Search


class SearchDetailView( DetailViewGotModel ):
    
    model           = Search
    template_name   = 'searching/detail.html'


class SearchDeleteView( DeleteViewGotModel ):

    model           = Search
    template_name   = 'confirm_delete.html'
    success_message = 'Search record successfully deleted!!!!'
    success_url     = reverse_lazy('searching:index')



class SearchUpdateView( SearchViewSuccessPostFormValidMixin, UpdateViewCanCancel ):

    model           = Search
    template_name   = 'searching/edit.html'
    success_message = 'Search record update successfully saved!!!!'
    form_class      = UpdateSearchForm

    success_message = 'Search record successfully updated!!!!'




class ItemsFoundIndexView( ListViewGotModel ):

    template_name       = 'searching/items_found_index.html'
    model               = UserItemFound
    context_object_name = 'items_found_list'
    paginate_by         = 100

    def get_queryset(self):
        return self.model.objects.filter(
                        iUser = self.request.user,
                        iHitStars__isnull = False ).order_by('-iHitStars')



class ItemFoundDetailView( DetailViewGotModel ):
    
    model           = UserItemFound
    parent          = ItemFound
    template_name   = 'searching/item_found_detail.html'
    form_class      = UserItemFoundForm




class ItemFoundUpdateView( UpdateViewCanCancel ):

    model           = UserItemFound
    parent          = ItemFound
    template_name   = 'searching/item_found_edit.html'
    success_message = 'Item Found record update successfully saved!!!!'
    form_class      = UserItemFoundForm

    # want to set tlook4hits = None if any relevant fields changed
    # can be done with a mixin

