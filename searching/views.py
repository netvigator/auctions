from core.views         import ( CreateViewCanCancel, DeleteViewGotModel,
                                 DetailViewGotModel,  ListViewGotModel,
                                 UpdateViewCanCancel )

from django.urls        import reverse_lazy

from .forms             import CreateSearchForm, UpdateSearchForm

import searching.utils

from ebayinfo.models    import EbayCategory

from .mixins            import SearchViewSuccessPostFormValidMixin
from .models            import Search

# ### keep views thin! ###



class SearchCreateView(
        SearchViewSuccessPostFormValidMixin, CreateViewCanCancel ):

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
    parent          = EbayCategory


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


