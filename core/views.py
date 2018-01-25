from django.shortcuts            import render
from django.views.generic        import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit   import CreateView, UpdateView, DeleteView

from crispy_forms.helper         import FormHelper
from crispy_forms.layout         import Submit

# Create your views here but keep them thin.

class ListViewGotModel( ListView ):
    '''
    Enhanced ListView which also includes the model in the context data,
    so that the template has access to its model class.
    '''
 
    def get_context_data(self, **kwargs):
        '''
        Adds the model to the context data.
        '''
        context          = super(ListView, self).get_context_data(**kwargs)
        context['model'] = self.model
        # context['model_fields'] = self.model._meta.get_fields()
        return context


class CreateViewGotCrispy( CreateView ):
    '''
    Enhanced CreateView which includes crispy form Create and Cancel buttons.
    '''
 
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        form.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        return form



class DeleteViewGotModel( DeleteView ):
    '''
    Enhanced DeleteView which also includes the model in the context data,
    so that the template has access to its model class.
    '''
 
    def get_context_data(self, **kwargs):
        '''
        Adds the model to the context data.
        '''
        context = super(DeleteView, self).get_context_data(**kwargs)
        context['model']        = self.model
        # context['model_fields'] = self.model._meta.get_fields()
        return context


class UpdateViewGotCrispy( UpdateView ):
    '''
    Enhanced UpdateView which includes crispy form Update and Cancel buttons.
    '''
 
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        form.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        return form


class DetailViewGotModel( DetailView ):
    '''
    Enhanced DetailView which also includes the model in the context data,
    so that the template has access to its model class.
    '''
 
    def get_context_data(self, **kwargs):
        '''
        Adds the model to the context data.
        '''
        context          = super(DetailView, self).get_context_data(**kwargs)
        context['model'] = self.model
        # context['model_fields'] = self.model._meta.get_fields()
        return context
