from core.views     import ( DetailViewGotModel,  ListViewGotModel,
                             UpdateViewCanCancel )

from django.http    import HttpResponseRedirect

from .forms         import ItemFoundForm, UserItemFoundForm

from .mixins        import AnyReleventHitStarColsChangedMixin

from .models        import ItemFound, UserItemFound, UserFinder

from core.mixins    import ( GetPaginationExtraInfoInContext,
                             GetFindersSelectionsOnPost,
                             GetUserItemsTableMixin )

# ### keep views thin! ###


class FindersIndexView(
            GetFindersSelectionsOnPost, GetPaginationExtraInfoInContext,
            ListViewGotModel ):

    template_name       = 'finders/fIndex.html'
    model               = UserFinder
    context_object_name = 'finders_list'
    paginate_by         = 100

    def get_queryset( self ):
        #
        # ADPZ
        # qs = super( ItemsFoundIndexView, self ).get_queryset()
        # sSelect = 'P'
        #
        sSelect = self.kwargs.get('select', 'P' )
        #
        if not sSelect: sSelect = 'P'
        #
        if sSelect == 'A': # all
            qsGot = UserFinder.objects.filter(
                        iUser               = self.request.user,
                        bListExclude        = False,
                    ).order_by( '-iMaxStars', 'iMaxModel', 'tTimeEnd' )
        elif sSelect == 'P': # postive (non-zero hit stars)
            qsGot = UserFinder.objects.filter(
                        iUser               = self.request.user,
                        iMaxStars__isnull   = False,
                        bListExclude        = False,
                    ).order_by( '-iMaxStars', 'iMaxModel', 'tTimeEnd' )
        elif sSelect == 'D': # "deleted" (excluded from list)
            qsGot = UserFinder.objects.filter(
                        iUser               = self.request.user,
                        iMaxStars__isnull   = False,
                        bListExclude        = True
                    ).order_by( '-iMaxStars', 'iMaxModel', 'tTimeEnd' )
        elif sSelect == 'Z': # iMaxStars = 0
            qsGot = UserFinder.objects.filter(
                        iUser               = self.request.user,
                        iMaxStars           = 0,
                        bListExclude        = False
                    ).order_by( '-iMaxStars', 'iMaxModel', 'tTimeEnd' )
        #
        return qsGot



class ItemsFoundIndexView(
            GetFindersSelectionsOnPost, GetPaginationExtraInfoInContext,
            ListViewGotModel ):

    template_name       = 'finders/index.html'
    model               = UserItemFound
    context_object_name = 'finders_list'
    paginate_by         = 100

    def get_queryset( self ):
        #
        # ADPZ
        # qs = super( ItemsFoundIndexView, self ).get_queryset()
        # sSelect = 'P'
        #
        sSelect = self.kwargs.get('select', 'P' )
        #
        if not sSelect: sSelect = 'P' # was p now P after non auctions flushed
        #
        if sSelect == 'A': # all
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        bListExclude        = False,
                        tRetrieved__isnull  = True,
                        iHitStars__isnull   = False
                    ).order_by( '-iHitStars', 'iModel', 'tCreate' )
        elif sSelect == 'P': # postive (non-zero hit stars)
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        iHitStars__isnull   = False,
                        bListExclude        = False,
                        tRetrieved__isnull  = True,
                        iHitStars__gt       = 0
                    ).order_by( '-iHitStars', 'iModel', 'tCreate' )
        elif sSelect == 'D': # "deleted" (excluded from list)
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        iHitStars__isnull   = False,
                        tRetrieved__isnull  = True,
                        bListExclude        = True
                    ).order_by( '-iHitStars', 'iModel', 'tCreate' )
        elif sSelect == 'Z': # iHitStars = 0
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        iHitStars           = 0,
                        tRetrieved__isnull  = True,
                        bListExclude        = False
                    ).order_by( '-iHitStars', 'iModel', 'tCreate' )
        #if sSelect == 'a': # all auctions
            #qsGot = UserItemFound.objects.select_related().filter(
                        #iUser               = self.request.user,
                        #bAuction            = True,
                        #bListExclude        = False,
                        #tRetrieved__isnull  = True,
                        #iHitStars__isnull   = False
                    #).order_by( '-iHitStars', 'iModel', 'tCreate' )
        #elif sSelect == 'p': # postive (non-zero hit stars) auctions
            #qsGot = UserItemFound.objects.select_related().filter(
                        #iUser               = self.request.user,
                        #bAuction            = True,
                        #iHitStars__isnull   = False,
                        #bListExclude        = False,
                        #tRetrieved__isnull  = True,
                        #iHitStars__gt       = 0
                    #).order_by( '-iHitStars', 'iModel', 'tCreate' )
        #elif sSelect == 'd': # "deleted" (excluded from list) auctions
            #qsGot = UserItemFound.objects.select_related().filter(
                        #iUser               = self.request.user,
                        #bAuction            = True,
                        #iHitStars__isnull   = False,
                        #tRetrieved__isnull  = True,
                        #bListExclude        = True
                    #).order_by( '-iHitStars', 'iModel', 'tCreate' )
        #elif sSelect == 's': # iHitStars = 0 auctions
            #qsGot = UserItemFound.objects.select_related().filter(
                        #iUser               = self.request.user,
                        #bAuction            = True,
                        #iHitStars           = 0,
                        #tRetrieved__isnull  = True,
                        #bListExclude        = False
                    #).order_by( '-iHitStars', 'iModel', 'tCreate' )
        #
        return qsGot








class ItemFoundDetailView( GetUserItemsTableMixin, DetailViewGotModel ):

    model           = UserFinder
    parent          = ItemFound
    template_name   = 'finders/fDetail.html'
    form_class      = UserItemFoundForm

    def get_context_data( self, **kwargs ):
        '''
        want more info to the context data.
        '''
        context = super(
                ItemFoundDetailView, self
                ).get_context_data( **kwargs )

        # qsThisItem = UserItemFound.objects.filter(
        #
        '''
        {'object': <UserItemFound: FISHER FM 200 B FM STEREO TUBE TUNER 200B>,
         'useritemfound': <UserItemFound: FISHER FM 200 B FM STEREO TUBE TUNER 200B>,
         'view': <finders.views.ItemFoundDetailView object at 0x7f0669fa63c8>,
         'model': <class 'finders.models.UserItemFound'>,\
         'parent': <class 'finders.models.ItemFound'>}
        '''
        #
        qsThisItemAllHits = UserItemFound.objects.filter(
                iItemNumb_id        = context[ 'object' ].iItemNumb,
                tRetrieved__isnull  = True,
                iUser               = self.request.user )
        #
        sThisItemAllHits = self.getUserItemsTable( qsThisItemAllHits )
        #
        context['AllHits']          = sThisItemAllHits
        context['qsAllHits']        = qsThisItemAllHits
        #
        return context


class ItemFoundHitView( GetUserItemsTableMixin, DetailViewGotModel ):

    model           = UserItemFound
    parent          = ItemFound
    template_name   = 'finders/detail.html'
    form_class      = UserItemFoundForm

    def get_context_data( self, **kwargs ):
        '''
        want more info to the context data.
        '''
        context = super(
                ItemFoundHitView, self
                ).get_context_data( **kwargs )

        # qsThisItem = UserItemFound.objects.filter(
        #
        '''
        {'object': <UserItemFound: FISHER FM 200 B FM STEREO TUBE TUNER 200B>,
         'useritemfound': <UserItemFound: FISHER FM 200 B FM STEREO TUBE TUNER 200B>,
         'view': <finders.views.ItemFoundDetailView object at 0x7f0669fa63c8>,
         'model': <class 'finders.models.UserItemFound'>,\
         'parent': <class 'finders.models.ItemFound'>}
        '''
        #
        qsThisItemAllHits = UserItemFound.objects.filter(
                iItemNumb_id = context[ 'object' ].iItemNumb_id,
                iUser        = context[ 'object' ].iUser )
        #
        qsThisItemOtherHits = qsThisItemAllHits.difference(
                UserItemFound.objects.filter( id = context[ 'object' ].id ) )
        #
        sThisItemOtherHits = self.getUserItemsTable( qsThisItemOtherHits )
        #
        context['OtherHits'] = sThisItemOtherHits
        #
        return context


class ItemFoundUpdateView(
            AnyReleventHitStarColsChangedMixin, UpdateViewCanCancel ):

    model           = UserItemFound
    parent          = ItemFound
    template_name   = 'finders/edit.html'
    success_message = 'Item Found record update successfully saved!!!!'
    form_class      = UserItemFoundForm

    tHitStarRelevantCols = (
        'iModel',
        'iBrand',
        'iCategory' )


