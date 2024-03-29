from django.http        import HttpResponseRedirect
from django.shortcuts   import render
from django.urls        import reverse_lazy

from core.mixins        import ( WereAnyReleventRegExColsChangedMixin,
                                 GetPaginationExtraInfoInContext,
                                 TitleSearchMixin )

from core.views         import (
                            CreateViewCanCancel, DeleteViewGotModel,
                            ListViewGotModel, UpdateViewCanCancel,
                            DetailViewGotModelAlsoPost )

from .forms             import CreateModelForm, UpdateModelForm
from .models            import Model

from categories.models  import Category


# ### views assemble presentation info ###
# ###         keep views thin!         ###


class ModelIndexView( GetPaginationExtraInfoInContext, TitleSearchMixin,
                      ListViewGotModel ):
    template_name = 'models/index.html'
    # context_object_name = 'model_list' # default
    model = Model
    paginate_by = 100



class ModelDetailView( DetailViewGotModelAlsoPost ):

    model   = Model
    template_name = 'models/detail.html'



class CategoryContextMixin( object ):

    def get_context_data(self, **kwargs):
        #
        context = super().get_context_data( **kwargs )
        #
        context['form'].fields['iCategory'].queryset = \
                Category.objects.filter( iUser = self.request.user )
        #
        return context



class ModelCreateView( CategoryContextMixin, CreateViewCanCancel ):

    model           = Model
    form_class      = CreateModelForm
    template_name   = 'models/add.html'
    success_message = 'New Model record successfully saved!!!!'



class ModelUpdateView( CategoryContextMixin,
            WereAnyReleventRegExColsChangedMixin, UpdateViewCanCancel):

    form_class      = UpdateModelForm
    model           = Model
    template_name   = 'models/edit.html'
    success_message = 'Model record update successfully saved!!!!'

    tRegExRelevantCols = (
        'cTitle',
        'cKeyWords',
        'cLookFor',
        'bSubModelsOK',
        'cExcludeIf' )




class ModelDeleteView( DeleteViewGotModel ):

    model           = Model
    template_name   = 'models/confirm_delete.html'
    success_url     = reverse_lazy('models:index')
    success_message = 'Model record successfully deleted!!!!'


