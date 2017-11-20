from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

# Create your views here but keep them thin.

from .models import Brand

class IndexView(generic.ListView):
    template_name = 'brands/index.html'
    context_object_name = 'brands_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Brand.objects.order_by('ctitle')


class DetailView(generic.DetailView):
    model = Brand
    template_name = 'brands/detail.html'

