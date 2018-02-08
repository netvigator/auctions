from django.shortcuts import render
#from django.views.generic           import DetailView
#from django.views.generic.edit      import CreateView, UpdateView, DeleteView
#from django.views.generic.list      import ListView

from django.http                    import HttpResponseRedirect
from django.urls                    import reverse_lazy

from core.mixins                    import ( DoesLoggedInUserOwnThisRowMixin,
                                             WereAnyReleventColsChangedMixin )

from core.views                     import (
                    CreateViewGotCrispy, DeleteViewGotModel,
                    DetailViewGotModel,  ListViewGotModel, UpdateViewGotCrispy )

from .models                        import Category

# Create your views here but keep them thin.

tCategoryFields = (
    'cTitle',
    'cKeyWords',
    # 'bKeyWordRequired',
    'cLookFor',
    'iStars',
    'bAllOfInterest',
    'bWantPair',
    'bAccessory',
    'bComponent',
    'iFamily',
    'cExcludeIf',
    'bModelsShared',
    )

class IndexView( ListViewGotModel ):  
    template_name = 'categories/index.html'
    # context_object_name = 'category_list' # default
    model = Category
    paginate_by = 100
    

class CategoryDetail( DoesLoggedInUserOwnThisRowMixin, DetailViewGotModel ):
    
    model   = Category
    template_name = 'categories/detail.html'


class CategoryCreate( CreateViewGotCrispy ):

    model   = Category
    fields  = tCategoryFields
    template_name = 'categories/add.html'
    success_url = reverse_lazy('categories:index')

    # success_message = 'New Category record successfully saved!!!!'

    def form_valid(self, form):
        form.instance.iUser = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('categories:index' )
            return HttpResponseRedirect(url)
        else:
            return super(CategoryCreate, self).post(request, *args, **kwargs)


class CategoryUpdate(
        DoesLoggedInUserOwnThisRowMixin,
        WereAnyReleventColsChangedMixin, UpdateViewGotCrispy):

    fields          = tCategoryFields
    model           = Category
    template_name   = 'categories/edit.html'

    # success_message = 'Category record update successfully saved!!!!'

    tRegExRelevantCols = (
        'cTitle',
        'cKeyWords',
        # 'bKeyWordRequired',
        'cLookFor',
        'bWantPair',
        'cExcludeIf' )

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('categories:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(CategoryUpdate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        if 'cTitle' in form.changed_data or 'cLookFor' in form.changed_data :
            form.instance.oRegExLook4Title  = None
        if 'cKeyWords' in form.changed_data :
            form.instance.oRegExKeyWords    = None
        if 'cExcludeIf' in form.changed_data :
            form.instance.oRegExExclude     = None
        return super().form_valid(form)


class CategoryDelete( DoesLoggedInUserOwnThisRowMixin, DeleteViewGotModel ):
    model   = Category
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('categories:index')

    # success_message = 'Category record successfully deleted!!!!'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('categories:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(CategoryDelete, self).post(request, *args, **kwargs)
