from django.views.generic.edit  import CreateView, UpdateView, DeleteView
from django.views.generic       import DetailView, ListView
from django.urls                import reverse_lazy
from django.views               import generic

from .models                    import Brand
from categories.models          import Category, BrandCategory
from models.models              import Model


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

class BrandCreate(CreateView):
    model   = Brand
    fields  = tModelFields
    template_name = 'brands/brand_add_form.html'

class BrandDelete(DeleteView):
    model   = Brand
    template_name = 'brands/brand_confirm_delete.html'
    success_url = reverse_lazy('brand-list')

class BrandDetail(DetailView):
    model   = Brand
    fields  = tModelFields
    template_name = 'brands/brand_detail_form.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BrandDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the categories
        #context['fields_list'] = Brand.getFieldsForView(
                                        #Brand, tMoreModelFields )
        #
        user = self.request.user
        context['categories_list'] = Category.objects.filter(iUser=user)
        # Add in a QuerySet of all the models
        context['models_list'    ] = Model.objects.filter(iUser=user)
        return context

class BrandUpdate(UpdateView):
    model   = Brand
    fields  = tModelFields
    template_name = 'brands/brand_edit_form.html'

class IndexView(ListView):  
    template_name = 'brands/brand_index.html'
    # context_object_name = 'brand_list' # default
    model = Brand
    
    def get_queryset(self):
        return Brand.objects.filter(iUser=self.request.user)
