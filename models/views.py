from django.shortcuts import render

from django.views.generic           import (
                                DetailView, ListView, UpdateView, DeleteView )
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.http                    import HttpResponseRedirect
from django.urls                    import reverse_lazy

from .models                        import Model
from core.mixins                    import DoesLoggedInUserOwnThisRowMixin


# Create your views here but keep them thin.
tModelFields = (
    'cTitle',
    'cKeyWords',
    'bKeyWordRequired',
    'bsplitdigitsok',
    'cLookFor',
    'iStars',
    'bSubModelsOK',
    'bMustHaveBrand',
    'bWanted',
    'bGetPictures',
    'bGetDescription',
    'cComment',
    'iBrand',
    'bGenericModel',
    'iCategory',
    'cExcludeIf',
    'cFileSpec1',
    'cFileSpec2',
    'cFileSpec3',
    'cFileSpec4',
    'cFileSpec5',
    )

class IndexView( LoginRequiredMixin, ListView ):  
    template_name = 'models/index.html'
    # context_object_name = 'model_list' # default
    model = Model
    paginate_by = 100
    
    def get_queryset(self):
        return Model.objects.filter(iUser=self.request.user)

class ModelDetail(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin, DetailView ):
    
    model   = Model
    template_name = 'models/detail.html'



class ModelUpdate(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin, UpdateView):

    fields = tModelFields

    model = Model

    template_name = 'models/edit.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('models:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(ModelUpdate, self).post(request, *args, **kwargs)



class ModelDelete(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin, DeleteView ):
    model   = Model
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('models:index')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('models:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(ModelDelete, self).post(request, *args, **kwargs)
