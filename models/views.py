from django.shortcuts import render

from django.views.generic           import DetailView, ListView
from django.contrib.auth.mixins     import LoginRequiredMixin

from .models                        import Model
from core.mixins                    import DoesLoggedInUserOwnThisRowMixin


# Create your views here but keep them thin.

tModelFields = (
    'cTitle',
    'iBrand',
    'iCategory',
    'cComment'
    )

class IndexView( LoginRequiredMixin, ListView ):  
    template_name = 'models/index.html'
    # context_object_name = 'model_list' # default
    model = Model
    paginate_by = 100
    
    def get_queryset(self):
        return Model.objects.filter(iUser=self.request.user)

class ModelDetail(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        DetailView ):
    
    model   = Model
    template_name = 'models/detail.html'


