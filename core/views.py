from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.messages.views  import SuccessMessageMixin

from django.http                    import HttpResponseRedirect

from django.urls                    import reverse_lazy

from django.views.generic           import ListView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView


from .mixins                        import ( DoesLoggedInUserOwnThisRowMixin,
                                             FormValidMixin, GetFormMixin,
                                             GetModelInContextMixin )

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

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy( '%s:index' % self.model._meta.db_table )
            return HttpResponseRedirect(url)
        else:
            # self.object = self.get_object() # assign the object to the view
            # cannot work, see above
            return ( super( CreateViewCanCancel, self )
                     .post( request, *args, **kwargs ) )



class DeleteViewGotModel( LoginRequiredMixin, GetModelInContextMixin,
                DoesLoggedInUserOwnThisRowMixin, SuccessMessageMixin, DeleteView ):
    '''
    Enhanced DeleteView which also includes the model in the context data,
    so that the template has access to its model class.
    '''
 
    success_message = 'Record successfully deleted!!!!'


    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.object.get_absolute_url()
            return HttpResponseRedirect(url)
        else:
            return super(DeleteViewGotModel, self).post(request, *args, **kwargs)


class UpdateViewCanCancel(
            LoginRequiredMixin, SuccessMessageMixin, FormValidMixin,
            DoesLoggedInUserOwnThisRowMixin, GetFormMixin, GetModelInContextMixin,

            UpdateView ):
    '''
    Enhanced UpdateView which includes crispy form Update and Cancel buttons.
    '''
    success_message = 'Record successfully saved!!!!'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.object.get_absolute_url()
            return HttpResponseRedirect(url)
        else:
            return super(UpdateViewCanCancel, self).post(request, *args, **kwargs)



class DetailViewGotModel( LoginRequiredMixin,
                DoesLoggedInUserOwnThisRowMixin, GetModelInContextMixin,
                DetailView ):
    '''
    Enhanced DetailView which also includes the model in the context data,
    so that the template has access to its model class.
    '''
 
    pass

