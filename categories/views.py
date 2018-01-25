from django.shortcuts import render
#from django.views.generic           import DetailView
#from django.views.generic.edit      import CreateView, UpdateView, DeleteView
#from django.views.generic.list      import ListView

from django.contrib.auth.mixins     import LoginRequiredMixin
from django.http                    import HttpResponseRedirect
from django.urls                    import reverse_lazy

from core.mixins                    import DoesLoggedInUserOwnThisRowMixin

from core.views                     import (
                    CreateViewGotCrispy, DeleteViewGotModel,
                    DetailViewGotModel,  ListViewGotModel, UpdateViewGotCrispy )

from .models                        import Category

# Create your views here but keep them thin.

tCategoryFields = (
    'cTitle',
    'cKeyWords',
    'bKeyWordRequired',
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

class IndexView( LoginRequiredMixin, ListViewGotModel ):  
    template_name = 'categories/index.html'
    # context_object_name = 'category_list' # default
    model = Category
    paginate_by = 100
    
    def get_queryset(self):
        return Category.objects.filter(iUser=self.request.user)

class CategoryDetail(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        DetailViewGotModel ):
    
    model   = Category
    template_name = 'categories/detail.html'


class CategoryCreate( LoginRequiredMixin, CreateViewGotCrispy ):

    model   = Category
    fields  = tCategoryFields
    template_name = 'categories/add.html'
    success_url = reverse_lazy('categories:index')

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
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        UpdateViewGotCrispy):

    fields          = tCategoryFields
    model           = Category
    template_name   = 'categories/edit.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('categories:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(CategoryUpdate, self).post(request, *args, **kwargs)



class CategoryDelete(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        DeleteViewGotModel ):
    model   = Category
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('categories:index')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('categories:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(CategoryDelete, self).post(request, *args, **kwargs)
