from django.shortcuts import render

from django.contrib.auth.mixins     import LoginRequiredMixin
from django.http                    import HttpResponseRedirect
from django.urls                    import reverse_lazy

from core.mixins                    import DoesLoggedInUserOwnThisRowMixin

from .models                        import Model

from core.views                     import (
                    CreateViewGotModel, DeleteViewGotModel,
                    DetailViewGotModel, ListViewGotModel, UpdateViewGotModel )

# Create your views here but keep them thin.

tModelFields = (
    'cTitle',
    'iBrand',
    'bGenericModel',
    'iCategory',
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
    'cExcludeIf',
    'cFileSpec1',
    'cFileSpec2',
    'cFileSpec3',
    'cFileSpec4',
    'cFileSpec5',
    )

class IndexView( LoginRequiredMixin, ListViewGotModel ):  
    template_name = 'models/index.html'
    # context_object_name = 'model_list' # default
    model = Model
    paginate_by = 100
    
    def get_queryset(self):
        return Model.objects.filter(iUser=self.request.user)

class ModelDetail(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        DetailViewGotModel ):
    
    model   = Model
    template_name = 'models/detail.html'


class ModelCreate( LoginRequiredMixin, CreateViewGotModel ):

    model   = Model
    fields  = tModelFields
    template_name = 'models/add.html'
    success_url = reverse_lazy('models:index')

    def form_valid(self, form):
        form.instance.iUser = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('models:index' )
            return HttpResponseRedirect(url)
        else:
            return super(ModelCreate, self).post(request, *args, **kwargs)


class ModelUpdate(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        UpdateViewGotModel):

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
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        DeleteViewGotModel ):
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
