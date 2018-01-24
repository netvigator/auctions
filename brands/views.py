#from django.views.generic          import DetailView
#from django.views.generic.edit     import CreateView, UpdateView, DeleteView
#from django.views.generic.list     import ListView
from django.urls                    import reverse_lazy
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.http                    import HttpResponseRedirect

from crispy_forms.helper            import FormHelper
from crispy_forms.layout            import Submit
# from crispy_forms.layout          import Layout, Field

from .models                        import Brand
from categories.models              import Category, BrandCategory
from models.models                  import Model
from core.mixins                    import DoesLoggedInUserOwnThisRowMixin
from core.utils                     import model_to_dict
from core.views                     import (
                    CreateViewGotModel, DeleteViewGotModel,
                    DetailViewGotModel, ListViewGotModel, UpdateViewGotModel )


# Create your views here but keep them thin.



tModelFields = (
    'cTitle',
    'bWanted',
    'bAllOfInterest',
    'cLookFor',
    'iStars',
    'cComment',
    'cNationality',
    'cExcludeIf' )

'''
    'iUser',
    'tCreate',
    'tModify'
'''

#lMoreModelFields = list( tModelFields )
#lMoreModelFields.extend( [ 'iUser_id', 'tCreate', 'tModify' ] )
#tMoreModelFields = tuple( lMoreModelFields )

class BrandCreate( LoginRequiredMixin, CreateViewGotModel ):

    model   = Brand
    fields  = tModelFields
    template_name = 'brands/add.html'
    success_url = reverse_lazy('brands:index')

    def form_valid(self, form):
        form.instance.iUser = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        form.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        return form


class BrandDelete(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        DeleteViewGotModel ):
    model   = Brand
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('brands:index')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('brands:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(BrandDelete, self).post(request, *args, **kwargs)

class BrandDetail(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        DetailViewGotModel ):
    
    model   = Brand
    template_name = 'brands/detail.html'


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BrandDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the categories
        #context['fields_list'] = Brand.getFieldsForView(
        #
        #context['model_fields' ] = tModelFields
        #context['dFieldsValues'] = model_to_dict( context['model'] )
        #
        context['categories_list'] = \
            self.object.getCategoriesForBrand(self.object)
        # Add in a QuerySet of all the models
        context['models_list'    ] = \
            self.object.getModelsForBrand(    self.object )
        #
        return context


class BrandUpdate(
        LoginRequiredMixin, DoesLoggedInUserOwnThisRowMixin,
        UpdateViewGotModel ):
    model   = Brand
    fields  = tModelFields
    template_name = 'brands/edit.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        form.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        return form

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = reverse_lazy('brands:detail', kwargs={'pk': self.object.id})
            return HttpResponseRedirect(url)
        else:
            return super(BrandUpdate, self).post(request, *args, **kwargs)

class IndexView( LoginRequiredMixin, ListViewGotModel ):  
    template_name = 'brands/index.html'
    # context_object_name = 'brand_list' # default
    model = Brand
    
    def get_queryset(self):
        return Brand.objects.filter(iUser=self.request.user)

    #def get_context_data(self, **kwargs):
        ## Call the base implementation first to get a context
        #context = super(IndexView, self).get_context_data(**kwargs)
