from django.urls                    import reverse_lazy
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.http                    import HttpResponseRedirect
from django.shortcuts               import render

from crispy_forms.helper            import FormHelper
from crispy_forms.layout            import Submit
# from crispy_forms.layout          import Layout, Field

from .models                        import Search
from core.mixins                    import DoesLoggedInUserOwnThisRowMixin
from core.utils                     import model_to_dict
from core.views                     import (
                    CreateViewGotModel, DeleteViewGotModel,
                    DetailViewGotModel, ListViewGotModel, UpdateViewGotModel )

# Create your views here.

from .models        import Search

tModelFields = (
    'cTitle',
    'cKeyWords',
    'iEbayCategory',
    'cPriority', )

class SearchCreate( LoginRequiredMixin, CreateViewGotModel ):

    model   = Search
    fields  = tModelFields
    template_name = 'searching/add.html'
    success_url = reverse_lazy('searching:index')

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


class IndexView( LoginRequiredMixin, ListViewGotModel ):  
    template_name = 'searching/index.html'
    # context_object_name = 'brand_list' # default
    model = Search
    
    def get_queryset(self):
        return Search.objects.filter(iUser=self.request.user)


class SearchDetail(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        DetailViewGotModel ):
    
    model   = Search
    template_name = 'searching/detail.html'



class SearchDelete(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        DeleteViewGotModel ):
    model   = Search
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('searching:index')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('searching:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(SearchDelete, self).post(request, *args, **kwargs)



class SearchUpdate(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        UpdateViewGotModel ):
    model   = Search
    fields  = tModelFields
    template_name = 'searching/edit.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('searching:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(SearchUpdate, self).post(request, *args, **kwargs)

