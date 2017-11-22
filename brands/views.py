from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView

# Create your views here but keep them thin.

from .models import Brand

class IndexView(generic.ListView):  
    template_name = 'brands/index.html'
    context_object_name = 'index'
    model = Brand
    
'''
    def get_queryset(self):
        """Return the last five published questions."""
        return Brand.objects.order_by('ctitle')
'''

class DetailView(generic.DetailView):
    model = Brand
    template_name = 'brands/detail.html'


class CreateBrandView(CreateView):

    model = Brand
    fields = ('ctitle','bwanted','ballofinterest','istars','ccomment',
              'cnationality','cexcludeif',)
    template_name = 'brands/edit_brand.html'

    def get_success_url(self):
        return reverse('brands-list')