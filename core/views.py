from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.messages.views  import SuccessMessageMixin

from django.http                    import HttpResponseRedirect

from django.urls                    import reverse_lazy

from django.views.generic           import ListView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView


from .mixins                        import ( DoesLoggedInUserOwnThisRowMixin,
                                             FormValidMixin, GetFormMixin,
                                             GetUserSelectionsOnPost,
                                             GetModelInContextMixin,
                                             DoPostCanCancelMixin,
                                             LoggedInOrVisitorMixin,
                                             GetUserOrVisitingMixin,
                                             GetFormKeyWordArgsMixin )

from .utils                         import getSaySequence


# ### views assemble presentation info ###
# ###         keep views thin!         ###


class ListViewGotModel( GetUserOrVisitingMixin, GetFormKeyWordArgsMixin,
            LoggedInOrVisitorMixin, GetModelInContextMixin, ListView ):
    '''
    Enhanced ListView which also includes the model in the context data,
    so that the template has access to its model class.
    '''

    def get_queryset(self):
        #
        oUser, isVisiting = self.getUserOrVisiting()
        #
        queryset = self.model.objects.filter( iUser = oUser )
        #
        return queryset



class CreateViewCanCancel( GetFormKeyWordArgsMixin, LoginRequiredMixin,
            SuccessMessageMixin, FormValidMixin, GetFormMixin,
            CreateView ):
    '''
    Enhanced CreateView which includes crispy form Create and Cancel buttons.
    '''

    # value accessed in subclass
    success_message = 'New record successfully saved!!!!'
    # value accessed in subclass

    def get_object(self):
        '''work around obscure bug, sometimes CreateView requires a pk!'''
        # https://github.com/django-guardian/django-guardian/issues/279
        return None

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
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
            return super().post( request, *args, **kwargs )



class DeleteViewGotModel( LoginRequiredMixin, GetModelInContextMixin,
                DoesLoggedInUserOwnThisRowMixin, SuccessMessageMixin,
                DoPostCanCancelMixin, GetFormKeyWordArgsMixin,
                DeleteView ):
    '''
    Enhanced DeleteView which also includes the model in the context data,
    so that the template has access to its model class.
    '''

    success_message = 'Record successfully deleted!!!!'



class UpdateViewCanCancel(
            GetFormKeyWordArgsMixin, LoginRequiredMixin, SuccessMessageMixin,
            FormValidMixin, DoesLoggedInUserOwnThisRowMixin,
            GetModelInContextMixin, DoPostCanCancelMixin, GetFormMixin,
            UpdateView ):
    '''
    Enhanced UpdateView which includes crispy form Update and Cancel buttons.
    '''
    success_message = 'Record successfully saved!!!!'



class DetailViewGotModel(
                LoggedInOrVisitorMixin,
                GetUserOrVisitingMixin,
                GetModelInContextMixin,
                DetailView ):
    '''
    Enhanced DetailView which also includes the model in the context data,
    so that the template has access to its model class.
    '''

    pass



class DetailViewGotModelAlsoPost(
            GetFormKeyWordArgsMixin,
            SuccessMessageMixin,
            GetUserSelectionsOnPost,
            DetailViewGotModel ):

    '''detail view for Brands, Categories & Models, manages Keepers & Finders'''

    def get_context_data( self, **kwargs ):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the categories
        #
        oUser, isVisiting = self.getUserOrVisiting()
        #
        t = self.object.getKeeperContextForThis( self.object, oUser )
        #
        sHowManyKeepers, qsKeeperItems   = t
        #
        context['keepers_list']         = qsKeeperItems
        context['sHowManyKeepers']      = sHowManyKeepers
        #
        t = self.object.getFinderContextForThis( self.object, oUser )
        #
        sHowManyFinders, qsFinderItems   = t
        #
        context['finders_list']         = qsFinderItems
        context['sHowManyFinders']      = sHowManyFinders
        #
        context['isVisiting']           = isVisiting
        #
        return context



