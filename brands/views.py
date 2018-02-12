from django.urls            import reverse_lazy
from django.http            import HttpResponseRedirect

from crispy_forms.layout    import Field

from core.mixins            import ( WereAnyReleventColsChangedMixin,
                                     TitleSearchMixin )
from core.utils             import model_to_dict
from core.views             import (
                    CreateViewGotCrispy, DeleteViewGotModel,
                    DetailViewGotModel,  ListViewGotModel, UpdateViewGotCrispy )

from .models                import Brand
from .forms                 import BrandForm

from categories.models      import Category, BrandCategory
from models.models          import Model

# Create your views here but keep them thin.


class BrandActionMixin( object ):
    
    model = Brand
    
    @property
    def success_msg(self): return NotImplemented

    def form_valid( self ):
        messages.info( self.request, self.success_msg )
        return super( BrandActionMixin, self ).form_valid( form )

        
class BrandCreate( BrandActionMixin, CreateViewGotCrispy ):

    model           = Brand
    template_name   = 'brands/add.html'
    success_url     = reverse_lazy('brands:index')
    form_class      = BrandForm

    success_message = 'New Brand record successfully saved!!!!'

    def form_valid(self, form):
        form.instance.iUser = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('brands:index' )
            return HttpResponseRedirect(url)
        else:
            return super(BrandCreate, self).post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(BrandCreate, self).get_form(form_class)
        Field('cExcludeIf', rows='2')
        return form

class BrandDelete( DeleteViewGotModel ):
    model   = Brand
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('brands:index')

    success_message = 'Brand record successfully deleted!!!!'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('brands:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(BrandDelete, self).post(request, *args, **kwargs)

class BrandDetail( DetailViewGotModel ):
    
    model   = Brand
    template_name = 'brands/detail.html'


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BrandDetail, self).get_context_data(**kwargs)
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
        return context


class BrandUpdate( BrandActionMixin, WereAnyReleventColsChangedMixin,
                   UpdateViewGotCrispy ):
    model           = Brand
    template_name   = 'brands/edit.html'
    form_class      = BrandForm

    success_message = 'Brand record update successfully saved!!!!'
    
    tRegExRelevantCols = (
        'cTitle',
        'cLookFor',
        'bWantPair',
        'cExcludeIf' )

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('brands:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(BrandUpdate, self).post(request, *args, **kwargs)




class IndexView( TitleSearchMixin, ListViewGotModel ):  
    template_name = 'brands/index.html'
    # context_object_name = 'brand_list' # default
    model = Brand
    
