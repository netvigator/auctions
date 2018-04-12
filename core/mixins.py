from django.core.exceptions import PermissionDenied
from django.db.models       import Q
from django.http            import HttpResponseRedirect

from Collect.Query          import get1stThatMeets
from Collect.Test           import ContainsAny


class DoesLoggedInUserOwnThisRowMixin(object):
    
    '''
    For some tables (Brands, Categories, Models, Searches, Items, and more),
    users should ONLY be able to their own records (rows).
    So we will overried get_object() and test there.
    This is tested in the Brands app!
    '''
    
    def get_object(self):
        '''only allow owner (or superuser) to access the table row'''
        obj = super(DoesLoggedInUserOwnThisRowMixin, self).get_object()
        if self.request.user.is_superuser:
            pass
        elif obj.iUser != self.request.user:
            raise PermissionDenied(
                "Permission Denied -- that's not your record!")
        return obj



class WereAnyReleventColsChangedBase(object):
    
    '''
    for testing whether any relevant fields have changed 
    '''
    def _getIsDataChangedTester( self, form ):
        
        def _isFormDataChanged( self, sCol ):
            #
            return sCol in form.changed_data
    
    def anyReleventColsChanged( self, form, tCols ):
        #
        isFormDataChanged = self._getIsDataChangedTester( form )
        #
        return get1stThatMeets( tCols, isFormDataChanged )


class WereAnyReleventRegExColsChangedMixin( WereAnyReleventColsChangedBase ):
    '''
    for testing whether any RegEx relevant fields have changed 
    '''
    setLook4TitleFields = frozenset( ( 'cTitle', 'cLookFor', 'bSubModelsOK' ) )
    #
    def redoRegEx( self, form ):
        #
        if ContainsAny( self.setLook4TitleFields, form.changed_data ):
            # Check whether sequence1 contains any of the items in sequence2.
            # 'cTitle' in form.changed_data or
            # 'cLookFor' in form.changed_data or
            # 'bSubModelsOK' in form.changed_data:
            form.instance.cRegExLook4Title  = None
        if 'cKeyWords' in form.changed_data :
            form.instance.cRegExKeyWords    = None
        if 'cExcludeIf' in form.changed_data :
            form.instance.cRegExExclude     = None
    
    def form_valid( self, form ):
        #
        if self.anyReleventColsChanged( form, self.tRegExRelevantCols ):
            #
            self.redoRegEx( form )
            #
        #
        return super(
                WereAnyReleventRegExColsChangedMixin, self ).form_valid( form )


class TitleSearchMixin(object):
    
    def get_queryset( self ):
        #
        # fetch the queryset from the parent's get_queryset
        #
        queryset = super( TitleSearchMixin, self ).get_queryset()
        #
        # get the Q parameter
        #
        q = self.request.GET.get( 'q' )
        #
        if q:
            # return a filtered queryset
            return queryset.filter(
                Q( cTitle__icontains = q ) | Q( cLookFor__icontains = q ) )
            #
        else: # no Q
            #
            return queryset


class FormValidMixin( object ):
    '''more DRY, move some copied and pasted code here'''

    def form_valid( self, form ):
        # model form does not accept user in kwargs
        obj = form.save( commit = False )
        obj.user = self.user = self.request.user
        form.instance.iUser  = self.request.user
        return super(FormValidMixin, self).form_valid(form)



class GetModelInContextMixin( object ):
    '''more DRY, move some copied and pasted code here'''
    
    def get_context_data(self, **kwargs):
        '''
        Adds the model to the context data.
        '''
        context = super(
                GetModelInContextMixin, self).get_context_data(**kwargs)
        context['model'] = self.model
        if hasattr( self, 'parent' ):
            context['parent'] = self.parent
        # context['model_fields'] = self.model._meta.get_fields()
        return context


class DoPostCanCancelMixin( object ):
    '''more DRY, move some copied and pasted code here'''

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.object.get_absolute_url()
            return HttpResponseRedirect(url)
        else:
            return ( super( DoPostCanCancelMixin, self )
                     .post( request, *args, **kwargs ) )


class GetFormMixin( object ):
    '''more DRY, move some copied and pasted code here'''

    def get_form( self, form_class = None ):
        '''
        can get form in view:
        form = self.get_form( self.form_class )
        see below for mixin that worked
        (but not used because there was a much easier way)
        '''
        if not hasattr( self, 'form' ) or self.form is None:
            form = super( GetFormMixin, self ).get_form(form_class)
            self.form = form
        #
        form.request = self.request
        #
        return form


"""
example of calling get_form()
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
