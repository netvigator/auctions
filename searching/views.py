from django.contrib.auth    import get_user_model
from django.urls            import reverse_lazy
from django.http            import HttpResponseRedirect

from .forms                 import SearchAddOrUpdateForm
from .mixins                import EbayCategoryFormValidMixin
from .models                import Search

from core.views             import (
                                CreateViewGotCrispy, DeleteViewGotModel,
                                DetailViewGotModel,  ListViewGotModel,
                                UpdateViewGotCrispy )

# Create your views here.

User = get_user_model()

tModelFields = (
    'cTitle',
    'cKeyWords',
    'iDummyCategory',
    'cPriority', )


class SearchCreate( EbayCategoryFormValidMixin, CreateViewGotCrispy ):

    form_class      = SearchAddOrUpdateForm
    model           = Search
    template_name   = 'searching/add.html'
    success_url     = reverse_lazy('searching:index')
    #success_url = reverse_lazy('searching:detail', kwargs={'pk': self.object.id})

    success_message = 'New Search record successfully saved!!!!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        form.which = 'Create'
        return form

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('searching:index')
            return HttpResponseRedirect(url)
        else:
            return super(SearchCreate, self).post(request, *args, **kwargs)


class IndexView( ListViewGotModel ):  
    template_name   = 'searching/index.html'
    # context_object_name = 'searching_list' # default
    model           = Search
    


class SearchDetail( DetailViewGotModel ):
    
    model           = Search
    template_name   = 'searching/detail.html'



class SearchDelete( DeleteViewGotModel ):
    model           = Search
    template_name   = 'confirm_delete.html'
    success_url     = reverse_lazy('searching:index')

    success_message = 'Search record successfully deleted!!!!'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('searching:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(SearchDelete, self).post(request, *args, **kwargs)



class SearchUpdate(  EbayCategoryFormValidMixin, UpdateViewGotCrispy ):
    model           = Search
    form_class      = SearchAddOrUpdateForm
    template_name   = 'searching/edit.html'

    success_message = 'Search record update successfully saved!!!!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        form.which = 'Update'
        return form


    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('searching:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(SearchUpdate, self).post(request, *args, **kwargs)

