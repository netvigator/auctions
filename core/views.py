from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.messages.views  import SuccessMessageMixin

from django.http                    import HttpResponseRedirect

from django.urls                    import reverse_lazy

from django.views.generic           import ListView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView


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

        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        
        oThisPage = context.get('page_obj')
        iPageNumb = oThisPage.number

        iMaxPage = len(paginator.page_range)
        #
        iStart = iPageNumb - 10 if iPageNumb >= 10 else 0
        iLast  = iPageNumb + 10 if iPageNumb <= iMaxPage else iMaxPage
        
        page_range = paginator.page_range[ iStart : iLast ]

        context.update({ 'page_range' : page_range,
                         'iStart'     : iStart,
                         'iLast'      : iLast,
                         'iMaxPage'   : iMaxPage })

        return context


    def get_queryset(self):
        return self.model.objects.filter( iUser = self.request.user )


class CreateViewGotCrispy( LoginRequiredMixin, SuccessMessageMixin, CreateView ):
    '''
    Enhanced CreateView which includes crispy form Create and Cancel buttons.
    '''

    success_message = 'New record successfully saved!!!!'

    def form_valid(self, form):
        # model form does not accept user in kwargs
        obj = form.save(commit=False)
        obj.user = self.user = self.request.user
        form.instance.iUser  = self.request.user
        # obj.save()
        return super(CreateViewGotCrispy, self).form_valid(form)


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
        form.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        form.which = 'Create'
        return form

    def get_object(self):
        '''work around obscure bug, sometimes CreateView wants a pk!'''
        # https://github.com/django-guardian/django-guardian/issues/279
        return None

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        return self.object.get_absolute_url()


    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy( '%s:index' % self.model._meta.db_table )
            return HttpResponseRedirect(url)
        else:
            return super(CreateViewGotCrispy, self).post(request, *args, **kwargs)


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

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.object.get_absolute_url()
            return HttpResponseRedirect(url)
        else:
            return super(DeleteViewGotModel, self).post(request, *args, **kwargs)


class UpdateViewGotCrispy( LoginRequiredMixin, SuccessMessageMixin,
                DoesLoggedInUserOwnThisRowMixin, UpdateView ):
    '''
    Enhanced UpdateView which includes crispy form Update and Cancel buttons.
    '''
    success_message = 'Record successfully saved!!!!'
    '''
    def __init__(self, *args, **kwargs):
        self.which = 'Update'
        super(UpdateViewGotCrispy, self).__init__(*args, **kwargs)
    '''
    def form_valid(self, form):
        # model form does not accept user in kwargs
        obj = form.save(commit=False)
        obj.user = self.user = self.request.user
        form.instance.iUser  = self.request.user
        # obj.save()
        return super(UpdateViewGotCrispy, self).form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        form.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-primary'))
        form.which = 'Update'
        return form

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.object.get_absolute_url()
            return HttpResponseRedirect(url)
        else:
            return super(UpdateViewGotCrispy, self).post(request, *args, **kwargs)


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
        if hasattr( self, 'parent' ): context['parent'] = self.parent
        # context['model_fields'] = self.model._meta.get_fields()
        return context
