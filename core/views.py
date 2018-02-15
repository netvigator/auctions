from django.contrib.auth.mixins     import LoginRequiredMixin
from django.views.generic           import ListView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView

from django.contrib.messages.views  import SuccessMessageMixin

from crispy_forms.helper            import FormHelper
from crispy_forms.layout            import Submit

from .mixins                        import DoesLoggedInUserOwnThisRowMixin

# Create your views here but keep them thin.

class ListViewGotModel( LoginRequiredMixin, ListView ):
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

    def get_queryset(self):
        return self.model.objects.filter( iUser = self.request.user )


class CreateViewGotCrispy( LoginRequiredMixin, SuccessMessageMixin, CreateView ):
    '''
    Enhanced CreateView which includes crispy form Create and Cancel buttons.
    '''

    '''
    def __init__(self, *args, **kwargs):
        self.which = 'Create'
        super(UpdateViewGotCrispy, self).__init__(*args, **kwargs)
    '''

    success_message = 'New record successfully saved!!!!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        form.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        form.which = 'Create'
        return form

    def form_valid(self, form):
        form.instance.iUser = self.request.user
        return super().form_valid(form)



class DeleteViewGotModel( LoginRequiredMixin,
                DoesLoggedInUserOwnThisRowMixin, SuccessMessageMixin, DeleteView ):
    '''
    Enhanced DeleteView which also includes the model in the context data,
    so that the template has access to its model class.
    '''
 
    success_message = 'Record successfully deleted!!!!'

    def get_context_data(self, **kwargs):
        '''
        Adds the model to the context data.
        '''
        context = super(DeleteView, self).get_context_data(**kwargs)
        context['model']        = self.model
        # context['model_fields'] = self.model._meta.get_fields()
        return context


class UpdateViewGotCrispy( LoginRequiredMixin,
                DoesLoggedInUserOwnThisRowMixin, SuccessMessageMixin, UpdateView ):
    '''
    Enhanced UpdateView which includes crispy form Update and Cancel buttons.
    '''
    success_message = 'Record successfully saved!!!!'
    '''
    def __init__(self, *args, **kwargs):
        self.which = 'Update'
        super(UpdateViewGotCrispy, self).__init__(*args, **kwargs)
    '''
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        form.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        form.which = 'Update'
        return form


class DetailViewGotModel( LoginRequiredMixin,
                DoesLoggedInUserOwnThisRowMixin, DetailView ):
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
