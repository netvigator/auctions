from django.shortcuts import render

from django.views.generic           import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView
from django.views.generic.list      import ListView

from django.contrib.auth.mixins     import LoginRequiredMixin
from django.http                    import HttpResponseRedirect
from django.urls                    import reverse_lazy

from core.mixins                    import DoesLoggedInUserOwnThisRowMixin

from crispy_forms.helper            import FormHelper
from crispy_forms.layout            import Submit

from .models                        import Model

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


class ModelCreate( LoginRequiredMixin, CreateView ):

    model   = Model
    fields  = tModelFields
    template_name = 'models/add.html'
    success_url = reverse_lazy('models:index')

    def form_valid(self, form):
        form.instance.iUser = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        #form.helper.layout = Layout()
        #Field( 'cLookFor', rows = 3 )
        form.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        return form


class ModelUpdate(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        UpdateView):

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
        DeleteView ):
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
