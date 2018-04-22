from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.messages.views  import SuccessMessageMixin

from django.http                    import HttpResponseRedirect

from django.urls                    import reverse_lazy

from django.views.generic           import ListView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView


from .mixins                        import ( DoesLoggedInUserOwnThisRowMixin,
                                             FormValidMixin, GetFormMixin,
                                             GetModelInContextMixin,
                                             DoPostCanCancelMixin )

# ### keep views thin! ###


class ListViewGotModel(
            LoginRequiredMixin, GetModelInContextMixin, ListView ):
    '''
    Enhanced ListView which also includes the model in the context data,
    so that the template has access to its model class.
    '''

    def get_queryset(self):
        #
        queryset = self.model.objects.filter( iUser = self.request.user )
        #
        return queryset



class CreateViewCanCancel( LoginRequiredMixin, 
            SuccessMessageMixin, FormValidMixin, GetFormMixin,
            CreateView ):
    '''
    Enhanced CreateView which includes crispy form Create and Cancel buttons.
    '''

    success_message = 'New record successfully saved!!!!'

    def get_object(self):
        '''work around obscure bug, sometimes CreateView requires a pk!'''
        # https://github.com/django-guardian/django-guardian/issues/279
        return None

    def get_form(self, form_class=None):
        form = super(CreateViewCanCancel, self).get_form(form_class)
        return form

    def post(self, request, *args, **kwargs):
        # this one is different, cannot use mixin
        if "cancel" in request.POST:
            # different URL in this one
            url = reverse_lazy( '%s:index' % self.model._meta.db_table )
            return HttpResponseRedirect(url)
        else:
            # self.object = self.get_object() # assign the object to the view
            # cannot work, see above
            return ( super( CreateViewCanCancel, self )
                     .post( request, *args, **kwargs ) )



class DeleteViewGotModel( LoginRequiredMixin, GetModelInContextMixin,
                DoesLoggedInUserOwnThisRowMixin, SuccessMessageMixin,
                DoPostCanCancelMixin,
                DeleteView ):
    '''
    Enhanced DeleteView which also includes the model in the context data,
    so that the template has access to its model class.
    '''
 
    success_message = 'Record successfully deleted!!!!'




class UpdateViewCanCancel(
            LoginRequiredMixin, SuccessMessageMixin, FormValidMixin,
            DoesLoggedInUserOwnThisRowMixin, GetModelInContextMixin,
            GetFormMixin, DoPostCanCancelMixin,
            UpdateView ):
    '''
    Enhanced UpdateView which includes crispy form Update and Cancel buttons.
    '''
    success_message = 'Record successfully saved!!!!'

    def get_form_kwargs(self):
        kwargs = super( UpdateViewCanCancel, self ).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs




class DetailViewGotModel( LoginRequiredMixin,
                DoesLoggedInUserOwnThisRowMixin, GetModelInContextMixin,
                DetailView ):
    '''
    Enhanced DetailView which also includes the model in the context data,
    so that the template has access to its model class.
    '''
 
    pass

