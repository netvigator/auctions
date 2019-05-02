from django.contrib         import messages
from django.http            import HttpResponseRedirect
from django.urls            import reverse_lazy

from core.mixins            import ( WereAnyReleventRegExColsChangedMixin,
                                     TitleSearchMixin )
from core.utils             import model_to_dict
from core.views             import (
                                CreateViewCanCancel, DeleteViewGotModel,
                                ListViewGotModel, UpdateViewCanCancel,
                                DetailViewGotModelAlsoPost )

from .forms             import CreateBrandForm, UpdateBrandForm
from .mixins            import ( GetContextForBrandCategoryList,
                                 PostUpdateBrandCategoryList )
from .models            import Brand

from categories.models  import Category, BrandCategory
from models.models      import Model
from keepers.utils      import deleteKeeperUserItem

# ### keep views thin! ###



class BrandCreateView( GetContextForBrandCategoryList,
                       PostUpdateBrandCategoryList, CreateViewCanCancel ):

    model           = Brand
    template_name   = 'brands/add.html'
    form_class      = CreateBrandForm

    success_message = 'New Brand record successfully saved!!!!'






class BrandDeleteView( DeleteViewGotModel ):

    model           = Brand
    template_name   = 'brands/confirm_delete.html'
    success_message = 'Brand record successfully deleted!!!!'
    success_url     = reverse_lazy('brands:index')




class BrandDetailView( DetailViewGotModelAlsoPost ):

    model   = Brand
    template_name = 'brands/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BrandDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the categories
        #context['fields_list'] = Brand.getFieldsForView(
        #
        #context['model_fields' ] = tModelFields
        #context['dFieldsValues'] = model_to_dict( context['model'] )
        #
        context['categories_list'] = \
            self.object.getCategoriesForBrand(self.object)
        # Add in a QuerySet of all the models
        context['models_list'    ] = \
            self.object.getModelsForBrand(    self.object )
        #
        # in DetailViewGotModelAlsoPost: context['keepers_list'] = oItems
        #
        return context



class BrandUpdateView( WereAnyReleventRegExColsChangedMixin,
                   GetContextForBrandCategoryList,
                   PostUpdateBrandCategoryList, UpdateViewCanCancel ):

    model           = Brand
    template_name   = 'brands/edit.html'
    form_class      = UpdateBrandForm

    success_message = 'Brand record update successfully saved!!!!'
    # success_url   = reverse_lazy('brands:detail')

    tRegExRelevantCols = (
        'cTitle',
        'cLookFor',
        'bWantPair',
        'cExcludeIf' )




class BrandIndexView( TitleSearchMixin, ListViewGotModel ):
    template_name = 'brands/index.html'
    # context_object_name = 'brand_list' # default
    model = Brand

