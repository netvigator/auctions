from django.core.exceptions import PermissionDenied
from django.db              import IntegrityError
from django.db.models       import Q
from django.http            import HttpResponseRedirect

from core                   import ( sTableTemplateRowRules,
                                     sRowTemplate6ColsValignTop )
from core.utils             import getLink, getSaySequence

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
        qsUserItems = self.getFinderQsetForThis( oThis, oUser )
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



class GetUserSelectionsOnPost( object ):
    #
    # this started in core.mixins, but
    # importing deleteKeeperUserItem there caused a circular import problem
    #
    def post( self, request, *args, **kwargs ):
        #
        url = request.build_absolute_uri()
        #
        # imports must be here, if above causes circular import block
        #
        tTrash = tuple( request.POST.getlist('bTrashThis') )
        #
        print( tTrash )
        #
        from finders.models import UserFinder, UserItemFound
        #
        if "selectall" in request.POST:
            #
            # next: queryset update method
            # next: queryset update method
            # next: queryset update method
            #
            tPageItems = tuple( map( int, request.POST.getlist('AllItems') ) )
            #
            UserFinder.objects.filter(
                    iItemNumb_id__in = tPageItems,
                    iUser            = self.request.user ).update(
                        bGetPictures = True,
                        bListExclude = False )
            #
            UserItemFound.objects.filter(
                    iItemNumb_id__in = tPageItems,
                    iUser            = self.request.user ).update(
                        bGetPictures = True,
                        bListExclude = False )
            #
            return HttpResponseRedirect( url )
            #
        elif 'GetOrTrashAll' in request.POST or 'GetOrTrashThis' in request.POST:
            #
            lAllItems   = request.POST.getlist('AllItems')
            #
            setAllItems = frozenset( lAllItems )
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
            lPicsGet    = []
            lPicsCancel = []
            lExcludeYes = []
            lExcludeNo  = []
            #
            for sItemNumb in setChanged:
                #
                if sItemNumb in setCommon: continue
                #
                if sItemNumb in setGetPics and sItemNumb not in setNewExcl:
                    lPicsGet.append( sItemNumb )
                elif sItemNumb in setUnPics:
                    lPicsCancel.append( sItemNumb )
                #
                if sItemNumb in setNewExcl:
                    lExcludeYes.append( sItemNumb )
                elif sItemNumb in setUnExcl:
                    lExcludeNo.append( sItemNumb )
                #
            #
            # next: queryset update method
            # next: queryset update method
            # next: queryset update method
            #
            if lPicsGet:
                #
                tPicsGet    = tuple( map( int, lPicsGet   ) )
                #
                UserFinder.objects.filter(
                        iItemNumb_id__in = tPicsGet,
                        iUser            = self.request.user ).update(
                            bGetPictures = True )
                #
                UserItemFound.objects.filter(
                        iItemNumb_id__in = tPicsGet,
                        iUser            = self.request.user ).update(
                            bGetPictures = True )
                #
            if lPicsCancel:
                #
                tPicsCancel = tuple( map( int, lPicsCancel) )
                #
                UserFinder.objects.filter(
                        iItemNumb_id__in = tPicsCancel,
                        iUser            = self.request.user ).update(
                            bGetPictures = False )
                #
                UserItemFound.objects.filter(
                        iItemNumb_id__in = tPicsCancel,
                        iUser            = self.request.user ).update(
                            bGetPictures = False )
                #
            if lExcludeYes:
                #
                tExcludeYes = tuple( map( int, lExcludeYes) )
                #
                UserFinder.objects.filter(
                        iItemNumb_id__in = tExcludeYes,
                        iUser            = self.request.user ).update(
                            bListExclude = True )
                #
                UserItemFound.objects.filter(
                        iItemNumb_id__in = tExcludeYes,
                        iUser            = self.request.user ).update(
                            bListExclude = True )
                #
            if lExcludeNo:
                #
                tExcludeNo  = tuple( map( int, lExcludeNo ) )
                #
                UserFinder.objects.filter(
                        iItemNumb_id__in = tExcludeNo,
                        iUser            = self.request.user ).update(
                            bListExclude = False )
                #
                UserItemFound.objects.filter(
                        iItemNumb_id__in = tExcludeNo,
                        iUser            = self.request.user ).update(
                            bListExclude = False )
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
        if 'trash' in request.POST:
            #
            # circular import problem if this import is at top
            #
            from keepers.utils import deleteKeeperUserItem
            #
            tTrash = tuple( request.POST.getlist('bTrashThis') )
            #
            for sItemNumb in tTrash:
                #
                deleteKeeperUserItem( sItemNumb, self.request.user )
                # print( 'would delete keeper %s' % sItemNumb )
                #
            #
            if tTrash:
                #
                if len( tTrash ) == 1:
                    #
                    sPart = ' %s' % tTrash[0]
                    #
                else:
                    #
                    sPart = 's %s' % getSaySequence( tTrash )
                    #
                #
                sMessage = 'Keeper item%s successfully trashed!!!!' % sPart
                #
                success_message = sMessage
                #
                # print( sMessage )
                # message display not working 2019-10-27
            #
        #
        return HttpResponseRedirect( url )

