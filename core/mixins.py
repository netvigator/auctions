from django.core.exceptions import PermissionDenied
from django.db.models       import Q

from Collect.Query          import get1stThatMeets


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


class WereAnyReleventColsChangedMixin(object):
    
    '''
    for testing whether any RegEx relevant fields have changed 
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

    def redoRegEx( self, form ):
        #
        if 'cTitle' in form.changed_data or 'cLookFor' in form.changed_data :
            form.instance.oRegExLook4Title  = None
        if 'cKeyWords' in form.changed_data :
            form.instance.oRegExKeyWords    = None
        if 'cExcludeIf' in form.changed_data :
            form.instance.oRegExExclude     = None
    
    def form_valid(self, form):
        #
        if self.anyReleventColsChanged( form, self.tRegExRelevantCols ):
            #
            self.redoRegEx( form )
            #
        #
        return super().form_valid(form)


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

