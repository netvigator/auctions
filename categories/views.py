from django.shortcuts   import render

from django.http        import HttpResponseRedirect
from django.urls        import reverse_lazy

from core.mixins        import WereAnyReleventRegExColsChangedMixin

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

    success_message = 'New Category record successfully saved!!!!'



class CategoryUpdateView( WereAnyReleventRegExColsChangedMixin, UpdateViewGotCrispy):

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




class CategoryDeleteView( DeleteViewGotModel ):

    model           = Category
    template_name   = 'confirm_delete.html'
    success_url     = reverse_lazy('categories:index')
    success_message = 'Category record successfully deleted!!!!'

