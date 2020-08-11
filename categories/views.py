from django.shortcuts   import render

from django.http        import HttpResponseRedirect
from django.urls        import reverse_lazy

from core.mixins        import WereAnyReleventRegExColsChangedMixin

from core.views         import (
                            CreateViewCanCancel, DeleteViewGotModel,
                            ListViewGotModel, UpdateViewCanCancel,
                            DetailViewGotModelAlsoPost )

from .forms             import UpdateCategoryForm, CreateCategoryForm
from .models            import Category


# ### views assemble presentation info ###
# ###         keep views thin!         ###


class CategoryIndexView( ListViewGotModel ):
    template_name = 'categories/index.html'
    # context_object_name = 'category_list' # default
    model = Category
    paginate_by = 100


class CategoryDetailView( DetailViewGotModelAlsoPost ):

    model   = Category
    template_name = 'categories/detail.html'



class CategoryCreateView( CreateViewCanCancel ):

    model           = Category
    form_class      = CreateCategoryForm
    template_name   = 'categories/add.html'

    success_message = 'New Category record successfully saved!!!!'



class CategoryUpdateView(
        WereAnyReleventRegExColsChangedMixin, UpdateViewCanCancel):

    form_class      = UpdateCategoryForm
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
    template_name   = 'categories/confirm_delete.html'
    success_url     = reverse_lazy('categories:index')
    success_message = 'Category record successfully deleted!!!!'

