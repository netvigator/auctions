from django.core.exceptions import PermissionDenied
from django.db              import IntegrityError
from django.db.models       import Q
from django.http            import HttpResponseRedirect

from django.contrib         import messages

from core                   import sTableTemplateRowRules, sRowTemplate6ColsValignTop
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

        if iPageNumb > 1 and sPrevPage:
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


class GetUserSelectionsOnPost( object ):
    #
    def post( self, request, *args, **kwargs ):
        #
        url = request.build_absolute_uri()
        #
        # from finders.models import UserFinder # got circular import problem
        #
        if "selectall" in request.POST:
            #
            lPageItems = request.POST.getlist('AllItems')
            #
            # qsChanged  = UserItemFound.objects.filter(
            #                 iItemNumb_id__in = lPageItems,
            #                 iUser            = self.request.user )
            #
            qsChanged  = self.UserItem.objects.filter(
                            iItemNumb_id__in = lPageItems,
                            iUser            = self.request.user )
            #
            for oItem in qsChanged:
                #
                #
                oItem.bGetPictures = True
                oItem.bListExclude = False
                #
                oItem.save()
                #
            #
            return HttpResponseRedirect( url )
            #
        elif 'submit' in request.POST:
            #
            # handle items listed more than once on a page
            # user may not mark each one.
            # QUICK (and dirty): ignore items listed more than once on a page
            #
            lAllItems   = request.POST.getlist('AllItems')
            #
            setAllItems = frozenset( lAllItems )
            #
            if len( lAllItems ) == len( setAllItems ):
                #
                setMultiple = frozenset( [] )
                #
            else:
                #
                setGotItems = set( [] )
                setMultiple = set( [] )
                #
                for sI in lAllItems:
                    #
                    if sI in setGotItems:
                        #
                        setMultiple.add( sI )
                        #
                    else:
                        #
                        setGotItems.add( sI )
                        #
                #
            #
            setExclude = frozenset( request.POST.getlist('bListExclude') )
            # check box end user can change
            setGetPics =       set( request.POST.getlist('bGetPictures') )
            # check box end user can change
            setPicsSet = frozenset( request.POST.getlist('PicsSet'     ) )
            # hidden set if item has bGetPictures as True when page composed
            setExclSet = frozenset( request.POST.getlist('ExclSet'     ) )
            # hidden set if item has bListExclude as True when page composed
            #
            setCommon  = setGetPics.intersection( setExclude )
            #
            setUnExcl  = setExclSet.difference( setExclude )
            setUnPics  = setPicsSet.difference( setGetPics )
            #
            setNewExcl = setExclude.difference( setExclSet )
            setNewPics = setGetPics.difference( setPicsSet )
            #
            setChanged = setUnExcl.union(
                        setUnPics, setNewExcl, setNewPics )
            #
            # qsChanged  = UserItemFound.objects.filter(
            #                 iItemNumb_id__in = setChanged,
            #                 iUser            = self.request.user )
            #
            qsChanged  = self.UserItem.objects.filter(
                            iItemNumb_id__in = setChanged,
                            iUser            = self.request.user )
            #
            setCommon.difference_update( setMultiple )
            #
            for oItem in qsChanged:
                #
                if str( oItem.iItemNumb_id ) in setCommon: continue
                #
                sItemNumb = str( oItem.iItemNumb_id )
                #
                if sItemNumb in setGetPics and sItemNumb not in setNewExcl:
                    oItem.bGetPictures = True
                elif sItemNumb in setUnPics:
                    oItem.bGetPictures = False
                #
                if sItemNumb in setNewExcl:
                    oItem.bListExclude = True
                elif sItemNumb in setUnExcl:
                    oItem.bListExclude = False
                #
                oItem.save()
                #
            #
            if setCommon:
                #
                sMessage = (
                        'Error! On a row, it is invalid set both '
                        'get pics and delete! Careful!' )
                #
                messages.error( request, sMessage )
                #
                for sItemNumb in setCommon:
                    oItem = ItemFound.objects.get( iItemNumb = int( sItemNumb ) )
                    messages.error( request, '%s -- %s' % ( sItemNumb, oItem.cTitle ) )
            #
        return HttpResponseRedirect( url )


class GetFindersSelectionsOnPost( GetUserSelectionsOnPost ):
    #
    def post( self, request, *args, **kwargs ):
        #
        # this import must be burried here to avoid a circular import problem
        #
        from finders.models import UserFinder
        #
        self.UserItem = UserFinder
        #
        return super(
                GetFindersSelectionsOnPost, self
                ).post( request, *args, **kwargs )


class GetUserItemsSelectionsOnPost( GetUserSelectionsOnPost ):
    #
    def post( self, request, *args, **kwargs ):
        #
        # this import must be burried here to avoid a circular import problem
        #
        from finders.models import UserItemFound
        #
        self.UserItem = UserItemFound
        #
        return super(
                GetFindersSelectionsOnPost, self
                ).post( request, *args, **kwargs )




class GetItemsForSomething( object ):
    '''get finders & keepers for Brand, Category or Model, DRY'''

    def getKeeperContextForThis( self, oThis, oUser ):
        #
        # actual keepers, not userkeepers
        #
        from keepers.models import Keeper # got circular import problem
        #
        lUserItems = self.getKeeperQsetForThis(
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
        return sHowMany, oItems



    def getFinderContextForThis( self, oThis, oUser ):
        #
        # actually userfinders not finders
        #
        qsUserItems = self.getFinderQsetForThis(
                        oThis, oUser ).order_by( '-tTimeEnd' )
        #
        iUserItems = len( qsUserItems )
        #
        if iUserItems > 50:
            #
            sHowMany = 'Recent'
            #
            oItems = qsUserItems[ : 20 ]
            #
        else:
            #
            sHowMany = 'All'
            #
            oItems = qsUserItems
            #
        #
        return sHowMany, oItems




def _sayStars( o, sName ):
    #
    if o is None:
        sSayStars = 'no %s found' % sName
    else:
        sSayStars = str( o.iStars )
    #
    return sSayStars


_sTrashCheckBox = ( '<input class="checkbox" name="bListExclude" '
                    'type="checkbox" value={{ item.iItemNumb_id }}' )


class GetUserItemsTableMixin( object ):
    '''get table of user items, DRY'''

    def getUserItemsTable( self, qs ):
        #
        if qs:
            #
            sHeader = ( sRowTemplate6ColsValignTop %
                        ( 'Edit', 'Trash', 'Model', 'Brand', 'Category', 'HitStars', '' ) )
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
                sUserItemLink = '<a href="%s">Edit</a>' % o.get_edit_url()
                #
                lRows.append( sRowTemplate6ColsValignTop %
                        ( sUserItemLink, _sTrashCheckBox, sModel, sBrand, sCategory, o.iHitStars, sDetail ) )
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
