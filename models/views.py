from django.http        import HttpResponseRedirect
from django.shortcuts   import render
from django.urls        import reverse_lazy

from core.mixins        import ( WereAnyReleventColsChangedMixin,
                                             TitleSearchMixin )

from core.views         import (
                    CreateViewGotCrispy, DeleteViewGotModel,
                    DetailViewGotModel, ListViewGotModel, UpdateViewGotCrispy )

from .forms             import ModelForm
from .models            import Model


# Create your views here but keep them thin.


class ModelIndexView( TitleSearchMixin, ListViewGotModel ):
    template_name = 'models/index.html'
    # context_object_name = 'model_list' # default
    model = Model
    paginate_by = 100
    

class ModelDetailView( DetailViewGotModel ):
    
    model   = Model
    template_name = 'models/detail.html'


class ModelCreateView( CreateViewGotCrispy ):

    model           = Model
    form_class      = ModelForm
    template_name   = 'models/add.html'
    success_message = 'New Model record successfully saved!!!!'



class ModelUpdateView( WereAnyReleventColsChangedMixin, UpdateViewGotCrispy):

    form_class      = ModelForm
    model           = Model
    template_name   = 'models/edit.html'
    success_message = 'Model record update successfully saved!!!!'

    tRegExRelevantCols = (
        'cTitle',
        'cKeyWords',
        #'bKeyWordRequired',
        #'bSplitDigitsOK',
        'cLookFor',
        'bSubModelsOK' )




class ModelDeleteView( DeleteViewGotModel ):

    model           = Model
    template_name   = 'confirm_delete.html'
    success_url     = reverse_lazy('models:index')
    success_message = 'Model record successfully deleted!!!!'


