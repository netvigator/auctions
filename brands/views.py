from django.views.generic.edit      import CreateView, UpdateView, DeleteView
from django.views.generic           import DetailView, ListView
from django.urls                    import reverse_lazy
from django.views                   import generic
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.http                    import HttpResponseForbidden

from .models                        import Brand
from categories.models              import Category, BrandCategory
from models.models                  import Model
from core.mixins                    import DoesLoggedInUserOwnThisRowMixin

from Utils.Output                   import getSayYesOrNo

# Create your views here but keep them thin.


'''
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView




    def get_queryset(self):
        """Return the last five published questions."""
        return Brand.objects.order_by('cTitle')


class DetailView(generic.DetailView):
    model = Brand
    template_name = 'brands/detail.html'


class CreateBrandView(CreateView):

    model = Brand
    fields = ('cTitle','bWanted','bAllOfInterest','iStars','cComment',
              'cNationality','cExcludeIf',)
    template_name = 'brands/edit_brand.html'

    def get_success_url(self):
        return reverse('brands-list')
'''


    
tModelFields = (
    'cTitle',
    'bWanted',
    'bAllOfInterest',
    'cLookFor',
    'iStars',
    'cComment',
    'cNationality',
    'cExcludeIf' )
'''
    'iUser',
    'tCreate',
    'tModify'
'''

#lMoreModelFields = list( tModelFields )
#lMoreModelFields.extend( [ 'iUser_id', 'tCreate', 'tModify' ] )
#tMoreModelFields = tuple( lMoreModelFields )


class BrandCreate( LoginRequiredMixin, CreateView ):
    model   = Brand
    fields  = tModelFields
    template_name = 'brands/add_form.html'
    success_url = reverse_lazy('brands:index')

    def form_valid(self, form):
        form.instance.iUser = self.request.user
        return super().form_valid(form)


class BrandDelete( LoginRequiredMixin, DeleteView ):
    model   = Brand
    template_name = 'brands/confirm_delete.html'
    success_url = reverse_lazy('brands:index')


class BrandDetail(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        DetailView ):
    
    model   = Brand
    template_name = 'brands/detail_form.html'


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BrandDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the categories
        #context['fields_list'] = Brand.getFieldsForView(
        #                               Brand, tMoreModelFields )
        #
        context['categories_list'] = \
            self.object.getCategoriesForBrand(self.object)
        # Add in a QuerySet of all the models
        context['models_list'    ] = \
            self.object.getModelsForBrand(    self.object )
        #
        return context


class BrandUpdate( LoginRequiredMixin, UpdateView ):
    model   = Brand
    fields  = tModelFields
    template_name = 'brands/edit_form.html'


class IndexView( LoginRequiredMixin, ListView ):  
    template_name = 'brands/index.html'
    # context_object_name = 'brand_list' # default
    model = Brand
    
    def get_queryset(self):
        return Brand.objects.filter(iUser=self.request.user)

    #def get_context_data(self, **kwargs):
        ## Call the base implementation first to get a context
        #context = super(IndexView, self).get_context_data(**kwargs)
