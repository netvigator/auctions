from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.messages.views  import SuccessMessageMixin

from django.http                    import HttpResponseRedirect

from django.urls                    import reverse_lazy

from django.views.generic           import ListView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView


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


class CreateViewCanCancel( LoginRequiredMixin, SuccessMessageMixin, CreateView ):
    '''
    Enhanced CreateView which includes crispy form Create and Cancel buttons.
    '''

    success_message = 'New record successfully saved!!!!'

    def form_valid(self, form):
        # model form does not accept user in kwargs
        obj = form.save( commit = False )
        obj.user = self.user = self.request.user
        form.instance.iUser  = self.request.user
        return super(CreateViewCanCancel, self).form_valid(form)


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

    def get_form( self, form_class = None ):
        '''
        can get form in view:
        form = self.get_form( self.form_class )
        see below for mixin that worked
        (but not used because there was a much easier way)
        '''
        form = super( CreateViewCanCancel, self ).get_form(form_class)
        form.request = self.request
        self.form = form
        return form


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


class UpdateViewCanCancel( LoginRequiredMixin, SuccessMessageMixin,
                DoesLoggedInUserOwnThisRowMixin, UpdateView ):
    '''
    Enhanced UpdateView which includes crispy form Update and Cancel buttons.
    '''
    success_message = 'Record successfully saved!!!!'

    def form_valid(self, form):
        # model form does not accept user in kwargs
        obj = form.save( commit = False )
        obj.user = self.user = self.request.user
        form.instance.iUser  = self.request.user
        # obj.save()
        return super(UpdateViewCanCancel, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.object.get_absolute_url()
            return HttpResponseRedirect(url)
        else:
            return super(UpdateViewCanCancel, self).post(request, *args, **kwargs)

    def get_form( self, form_class = None ):
        '''
        can get form in view:
        form = self.get_form( self.form_class )
        see below for mixin that worked
        (but not used because there was a much easier way)
        '''
        form = super( UpdateViewCanCancel, self ).get_form(form_class)
        form.request = self.request
        self.form = form
        return form

    def get_context_data(self, **kwargs):
        '''
        Adds the model to the context data.
        '''
        context          = super( UpdateView, self).get_context_data(**kwargs)
        context['model'] = self.model
        if hasattr( self, 'parent' ):
            context['parent'] = self.parent
        # context['model_fields'] = self.model._meta.get_fields()
        return context


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
        if hasattr( self, 'parent' ):
            context['parent'] = self.parent
        # context['model_fields'] = self.model._meta.get_fields()
        return context


"""
this worked but this is not used cuz there was a much easier way

class SayCurrentPriceBetterMixin( object ):
    '''streamline saying the current price if in USD'''

    #
    def get_context_data( self, **kwargs ):
        '''
        Adds the the current price line to the context data.
        '''
        context = super(
            SayCurrentPriceBetterMixin, self ).get_context_data(**kwargs)
        #
        form = self.get_form( self.form_class )
        #
        sayCurrentPrice = form.instance.iItemNumb._meta.get_field(
                                'lCurrentPrice').verbose_name
        #
        sayCurrentPrice = sayCurrentPrice.replace(
                'local currency',
                form.instance.iItemNumb.lLocalCurrency )
        #
        context['sayCurrentPrice'] = sayCurrentPrice
        #
        self.form = form
        #
        return context
"""
