from core.views     import ( DetailViewGotModel,  ListViewGotModel,
                             UpdateViewCanCancel, CreateViewCanCancel )

from django.http    import HttpResponseRedirect

from .forms         import ItemFoundForm, UserItemFoundForm

from .mixins        import AnyReleventHitStarColsChangedMixin

from .models        import ItemFound, UserItemFound, UserFinder

from core.mixins    import ( GetPaginationExtraInfoInContext,
                             GetUserSelectionsOnPost,
                             TitleSearchMixin )

from brands.models      import Brand
from categories.models  import Category

# ### views assemble presentation info ###
# ###         keep views thin!         ###


class FinderIndexView(
            GetUserSelectionsOnPost,
            GetPaginationExtraInfoInContext,
            TitleSearchMixin,
            ListViewGotModel ):

    template_name       = 'finders/index.html'
    model               = UserFinder
    context_object_name = 'finders_list'
    paginate_by         = 100

    def get_queryset( self ):
        #
        # ADS
        # qs = super().get_queryset()
        # sSelect = 'P'
        #
        sSelect = self.kwargs.get( 'select', 'A' )
        #
        if not sSelect: sSelect = 'A'
        #
        if sSelect == 'A': # all
            qsGot = UserFinder.objects.filter(
                        iUser               = self.request.user,
                        bListExclude        = False,
                    ).order_by( '-iHitStars', 'iMaxModel', 'tTimeEnd' )
        #elif sSelect == 'P': # postive (non-zero hit stars)
        #    qsGot = UserFinder.objects.filter(
        #                iUser               = self.request.user,
        #                iHitStars__isnull   = False,
        #                bListExclude        = False,
        #            ).order_by( '-iHitStars', 'iMaxModel', 'tTimeEnd' )
        #
        elif sSelect == 'D': # "deleted" (excluded from list)
            qsGot = UserFinder.objects.filter(
                        iUser               = self.request.user,
                        iHitStars__isnull   = False,
                        bListExclude        = True
                    ).order_by( '-iHitStars', 'iMaxModel', 'tTimeEnd' )
        #elif sSelect == 'Z': # iHitStars = 0
        #    qsGot = UserFinder.objects.filter(
        #                iUser               = self.request.user,
        #                iHitStars           = 0,
        #                bListExclude        = False
        #            ).order_by( '-iHitStars', 'iMaxModel', 'tTimeEnd' )
        #
        elif sSelect == 'S': # Search
            #
            qsGot = super().get_queryset( *args, **kwargs )
            #
            # want to find the get_queryset() method of TitleSearchMixin
            # not          the get_queryset() method of ListViewGotModel
            #
        #
        return qsGot



class ItemFoundDetailView( GetUserSelectionsOnPost, DetailViewGotModel ):

    # get this from the finders list (top menu item)

    model           = UserFinder
    parent          = ItemFound
    template_name   = 'finders/detail.html'
    form_class      = UserItemFoundForm

    def get_context_data( self, **kwargs ):
        '''
        want more info to the context data.
        '''
        context = super().get_context_data( **kwargs )

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
                iItemNumb_id    = context[ 'object' ].iItemNumb_id,
                iUser           = self.request.user,
                bListExclude    = False,
                ).order_by( '-iHitStars' )
        #
        context['HitsForThis']  = qsThisItemAllHits
        #
        session = self.request.session
        #
        session['iItemNumb'  ]  = context[ 'object' ].iItemNumb_id
        session['iSearch'    ]  = qsThisItemAllHits[0].iSearch_id
        #
        return context


"""
class ItemFoundHitView( GetUserSelectionsOnPost, DetailViewGotModel ):

    # get this from the list at bottom for a model, brand or category

    model           = UserItemFound
    parent          = ItemFound
    template_name   = 'finders/hit-detail.html'
    form_class      = UserItemFoundForm

    def get_context_data( self, **kwargs ):
        '''
        want more info to the context data.
        '''
        context = super().get_context_data( **kwargs )
        #
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
        qsThisItemOtherHits = UserItemFound.objects.filter(
                iItemNumb_id  = context[ 'object' ].iItemNumb_id,
                iUser         = context[ 'object' ].iUser,
                bListExclude  = False
                ).exclude( id = context[ 'object' ].id
                ).order_by( '-iHitStars' )
        #
        context['HitsForThis']  = qsThisItemOtherHits
        #
        session = self.request.session
        #
        session['iItemNumb']    = context[ 'object' ].iItemNumb_id
        #
        session['iSearch']      = \
                context['object'].iSearch_id or qsThisItemOtherHits[0].iSearch_id
        #
        return context
"""

class ItemFoundUpdateView(
            AnyReleventHitStarColsChangedMixin, UpdateViewCanCancel ):

    model           = UserItemFound
    parent          = ItemFound
    template_name   = 'finders/edit.html'
    success_message = 'Finder update successfully saved!!!!'
    form_class      = UserItemFoundForm

    tHitStarRelevantCols = (
        'iModel',
        'iBrand',
        'iCategory' )

    def get_context_data( self, **kwargs ):
        '''
        want more info to the context data.
        '''
        #
        context = super().get_context_data( **kwargs )

        context['form'].fields['iBrand'].queryset = \
                    Brand.objects.filter( iUser = self.request.user )
        context['form'].fields['iCategory'].queryset = \
                    Category.objects.filter( iUser = self.request.user )
        #
        instance = context['form'].instance
        # session  = self.request.session
        #
        # print( "instance.iItemNumb_id:", instance.iItemNumb_id )
        # print( "instance.iBrand:", instance.iBrand )
        # print( "session['iItemNumb'] :", session['iItemNumb'] )
        #
        return context


class ItemFoundCreateView( CreateViewCanCancel ):

    model           = UserItemFound
    parent          = ItemFound
    template_name   = 'finders/add.html'
    success_message = 'New finder successfully saved!!!!'
    form_class      = UserItemFoundForm

    def form_valid( self, form ):
        #
        instance = form.instance
        session  = self.request.session
        #
        instance.iItemNumb_id = instance.iItemNumb_id or session['iItemNumb']
        instance.iSearch_id   = instance.iSearch_id   or session['iSearch'  ]
        instance.iUser        = self.request.user
        #
        return super().form_valid( form )
