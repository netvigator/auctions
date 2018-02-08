from django.shortcuts import render

from django.http                    import HttpResponseRedirect
from django.urls                    import reverse_lazy

from core.mixins                    import ( WereAnyReleventColsChangedMixin,
                                             TitleSearchMixin )

from core.views                     import (
                    CreateViewGotCrispy, DeleteViewGotModel,
                    DetailViewGotModel, ListViewGotModel, UpdateViewGotCrispy )

from .models                        import Model


# Create your views here but keep them thin.

tModelFields = (
    'cTitle',
    'iBrand',
    'bGenericModel',
    'iCategory',
    'cKeyWords',
    #'bKeyWordRequired',
    #'bSplitDigitsOK',
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

class IndexView( TitleSearchMixin, ListViewGotModel ):
    template_name = 'models/index.html'
    # context_object_name = 'model_list' # default
    model = Model
    paginate_by = 100
    

class ModelDetail( DetailViewGotModel ):
    
    model   = Model
    template_name = 'models/detail.html'


class ModelCreate( CreateViewGotCrispy ):

    model   = Model
    fields  = tModelFields
    template_name = 'models/add.html'
    success_url = reverse_lazy('models:index')

    success_message = 'New Model record successfully saved!!!!'

    def form_valid(self, form):
        form.instance.iUser = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('models:index' )
            return HttpResponseRedirect(url)
        else:
            return super(ModelCreate, self).post(request, *args, **kwargs)


class ModelUpdate( WereAnyReleventColsChangedMixin, UpdateViewGotCrispy):

    fields = tModelFields
    model = Model
    template_name = 'models/edit.html'

    success_message = 'Model record update successfully saved!!!!'

    tRegExRelevantCols = (
        'cTitle',
        'cKeyWords',
        #'bKeyWordRequired',
        #'bSplitDigitsOK',
        'cLookFor',
        'bSubModelsOK' )

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('models:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(ModelUpdate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        if 'cTitle' in form.changed_data or 'cLookFor' in form.changed_data :
            form.instance.oRegExLook4Title  = None
        if 'cKeyWords' in form.changed_data :
            form.instance.oRegExKeyWords    = None
        if 'cExcludeIf' in form.changed_data :
            form.instance.oRegExExclude     = None
        return super().form_valid(form)


class ModelDelete( DeleteViewGotModel ):
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
