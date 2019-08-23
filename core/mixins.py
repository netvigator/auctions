from django.core.exceptions import PermissionDenied
from django.db              import IntegrityError
from django.db.models       import Q
from django.http            import HttpResponseRedirect

from core                   import sTableTemplateRowRules, sRowTemplate4ColsValignTop

from core.utils             import getLink

from pyPks.Collect.Query    import get1stThatMeets
from pyPks.Collect.Test     import ContainsAny


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
            queryset = queryset.filter(
                Q( cTitle__icontains = q ) | Q( cLookFor__icontains = q ) )
            #
        #
        return queryset


class FormValidMixin( object ):
    '''more DRY, move some copied and pasted code here'''

    def form_valid( self, form ):
        # model form does not accept user in kwargs
        obj = form.save( commit = False )
        obj.user = self.user = self.request.user
        form.instance.iUser  = self.request.user
        #try:
            #return super(FormValidMixin, self).form_valid(form)
        #except IntegrityError:
            #return self
        return super(FormValidMixin, self).form_valid(form)


class GetModelInContextMixin( object ):
    '''more DRY, move some copied and pasted code here'''

    def get_context_data(self, **kwargs):
        '''
        Adds the model to the context data.
        '''
        context = super(
                GetModelInContextMixin, self).get_context_data(**kwargs)
        #
        context['model'] = self.model
        #
        if hasattr( self, 'parent' ):
            context['parent'] = self.parent
        #
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



class GetPaginationExtraInfoInContext( object ):
    ''' get info into context for bisect style page choices'''

    def get_context_data( self, **kwargs ):
        '''
        Adds pagination info to the context data.
        '''
        sPrevPage = self.request.GET.get( 'previous', None )

        if sPrevPage is None and 'sPrevPage' in kwargs:
            #
            sPrevPage = kwargs.pop( 'sPrevPage' )

        context = super(
                GetPaginationExtraInfoInContext, self
                ).get_context_data( **kwargs )

        if not context.get( 'is_paginated' ):
            return context

        paginator = context.get('paginator')

        oThisPage = context.get('page_obj')
        iPageNumb = oThisPage.number

        iMaxPage = len(paginator.page_range)
        #
        iBeg = iPageNumb - 1 if iPageNumb > 3 else 0
        iEnd = iMaxPage if iPageNumb + 2 == iMaxPage else iPageNumb + 1

        iMidLeft = iMidRight = 0

        if iPageNumb > 1 and sPrevPage is not None:
            #
            iPrevPage = int( sPrevPage )

            # want choice midway between previous page and this page
            iNeedPage = ( iPageNumb + iPrevPage ) // 2

        else:
            #
            iNeedPage = 0

        iBegAvg = 1
        iEndAvg = iMaxPage
        #
        #
        iMidLeft    = ( ( iBegAvg   + iPageNumb ) // 2
                            if iPageNumb - 1 > 2 else 0 )
        iMidRight   = ( ( iPageNumb + iEndAvg   ) // 2
                            if iEndAvg - iPageNumb > 2 else 0 )

        iStart = iBeg - 1 if iBeg > 0 else 0

        show_range = paginator.page_range[ iStart : iEnd ]

        #print('iMidRight:', iMidRight )
        #print('sPrevPage:', sPrevPage )
        #print('iNeedPage:', iNeedPage )

        # want choice midway between previous page and this page
        if iNeedPage > 0 and iNeedPage not in show_range:
            if iNeedPage > iPageNumb:
                iMidRight = iNeedPage
            elif iNeedPage < iPageNumb:
                iMidLeft  = iNeedPage
        #print('iMidRight:', iMidRight )

        if iMidLeft  in show_range:
            if iPageNumb > iMaxPage // 2:
                iMidLeft  = iPageNumb // 2
            else:
                iMidLeft  = 0

        if iMidRight in show_range:
            if iPageNumb < iMaxPage // 2:
                iMidRight = ( iPageNumb + iMaxPage ) // 2
            else:
                iMidRight = 0

        #print( 'show_range:', show_range )
        #print( 'iPageNumb :', iPageNumb  )
        #print( 'iBegAvg   :', iBegAvg    )
        #print( 'iEndAvg   :', iEndAvg    )
        #print( 'iBeg      :', iBeg       )
        #print( 'iEnd      :', iEnd       )
        #print( 'iMidLeft  :', iMidLeft   )
        #print( 'iMidRight :', iMidRight  )

        context.update({ 'show_range' : show_range,
                         'iBeg'       : iBeg,
                         'iEnd'       : iEnd,
                         'iMidLeft'   : iMidLeft,
                         'iMidRight'  : iMidRight,
                         'iMaxPage'   : iMaxPage })
        #
        return context


class GetItemsForSomething( object ):
    '''get keepers for Brand, Category or Model, DRY'''

    def getKeepersForThis( self, oThis, request ):
        #
        from keepers.models   import Keeper
        #
        oUser = request.user
        #
        lUserItems = self.getUserKeepersForThis(
                oThis, oUser
                ).values_list( 'iItemNumb', flat=True ).distinct()
        #
        iUserItems = len( lUserItems )
        #
        print( 'len( iUserItems ):', iUserItems )
        #
        if iUserItems > 50:
            #
            sHowMany = 'Recent'
            #
            oItems = Keeper.objects.filter(
                iItemNumb__in = lUserItems ).order_by(
                    '-tTimeEnd' )[ : 20 ]
            #
        else:
            #
            sHowMany = 'All'
            #
            oItems = Keeper.objects.filter(
                iItemNumb__in = lUserItems ).order_by(
                    '-tTimeEnd' )
            #
        #
        # print( 'len( oItems ):', len( oItems ) )
        #
        return sHowMany, len( lUserItems ), oItems



    def getFindersForThis( self, oThis, request ):
        #
        from finders.models   import UserItemFound
        #
        oUser = request.user
        #
        lUserItems = self.getUserFindersForThis(
                oThis, oUser
                ).values_list( 'iItemNumb', flat=True ).distinct()
        #
        iUserItems = len( lUserItems )
        #
        # print( 'len( iUserItems ):', iUserItems )
        #
        if iUserItems > 50:
            #
            sHowMany = 'Recent'
            #
            oItems = UserItemFound.objects.filter(
                iItemNumb__in = lUserItems ).order_by(
                    '-tTimeEnd' )[ : 20 ]
            #
        else:
            #
            sHowMany = 'All'
            #
            oItems = UserItemFound.objects.filter(
                iItemNumb__in = lUserItems ).order_by(
                    '-tTimeEnd' )
            #
        #
        # print( 'len( oItems ):', len( oItems ) )
        #
        return sHowMany, len( lUserItems ), oItems




def _sayStars( o, sName ):
    #
    if o is None:
        sSayStars = 'no %s found' % sName
    else:
        sSayStars = str( o.iStars )
    #
    return sSayStars


class GetUserItemsTableMixin( object ):
    '''get table of user items, DRY'''

    def getUserItemsTable( self, qs ):
        #
        if qs:
            #
            sHeader = ( sRowTemplate4ColsValignTop %
                        ( 'Model', 'Brand', 'Category', 'HitStars', '' ) )
            #
            lRows = [ sHeader ]
            #
            for o in qs:
                #
                sayStarsModel   = _sayStars( o.iModel,    'model'    )
                sayStarsBrand   = _sayStars( o.iBrand,    'brand'    )
                sayStarsCategory= _sayStars( o.iCategory, 'category' )
                #
                tStars = ( sayStarsModel, sayStarsBrand, sayStarsCategory )
                #
                sDetail = ' ( %s * %s * %s )' % tStars
                #
                sModel    = getLink( o.iModel    )
                sBrand    = getLink( o.iBrand    )
                sCategory = getLink( o.iCategory )
                #
                lRows.append( sRowTemplate4ColsValignTop %
                        ( sModel, sBrand, sCategory, o.iHitStars, sDetail ) )
                #
            #
            sThisItemHitsTable = sTableTemplateRowRules % '\n'.join( lRows )
            #
        else:
            #
            sThisItemHitsTable = 'None'
            #
        #
        return sThisItemHitsTable
