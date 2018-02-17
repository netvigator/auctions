from django.shortcuts   import render

from django.http        import HttpResponseRedirect
from django.urls        import reverse_lazy

from core.mixins        import WereAnyReleventColsChangedMixin

from core.views         import (
                    CreateViewGotCrispy, DeleteViewGotModel,
                    DetailViewGotModel,  ListViewGotModel, UpdateViewGotCrispy )

from .forms             import CategoryForm
from .models            import Category

# Create your views here but keep them thin.


class CategoryIndexView( ListViewGotModel ):  
    template_name = 'categories/index.html'
    # context_object_name = 'category_list' # default
    model = Category
    paginate_by = 100
    

class CategoryDetailView( DetailViewGotModel ):
    
    model   = Category
    template_name = 'categories/detail.html'


class CategoryCreateView( CreateViewGotCrispy ):

    model           = Category
    form_class      = CategoryForm
    template_name   = 'categories/add.html'
    success_url     = reverse_lazy('categories:index')

    success_message = 'New Category record successfully saved!!!!'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('categories:index' )
            return HttpResponseRedirect(url)
        else:
            return super(CategoryCreateView, self).post(request, *args, **kwargs)


class CategoryUpdateView( WereAnyReleventColsChangedMixin, UpdateViewGotCrispy):

    form_class      = CategoryForm
    model           = Category
    template_name   = 'categories/edit.html'

    success_message = 'Category record update successfully saved!!!!'

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
            return super(CategoryUpdateView, self).post(request, *args, **kwargs)



class CategoryDeleteView( DeleteViewGotModel ):
    model   = Category
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('categories:index')

    success_message = 'Category record successfully deleted!!!!'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('categories:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(CategoryDeleteView, self).post(request, *args, **kwargs)
