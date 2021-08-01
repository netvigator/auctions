from django.conf    import settings

from core.views     import ( DetailViewGotModel,  ListViewGotModel,
                             UpdateViewCanCancel, CreateViewCanCancel )

from django.http    import HttpResponseRedirect

from .forms         import ItemFoundForm, UserItemFoundForm

from .mixins        import AnyReleventHitStarColsChangedMixin

from .models        import ItemFound, UserItemFound, UserFinder

from core.mixins    import ( GetPaginationExtraInfoInContext,
                             GetUserSelectionsOnPost,
                             TitleSearchMixin, GetUserOrVisiting )

from core.utils     import ( getDateTimeObjGotEbayStr, getEbayStrGotDateTimeObj,
                             sayMoreAboutHitsForThis )

from brands.models      import Brand
from categories.models  import Category

# ### views assemble presentation info ###
# ###         keep views thin!         ###

if settings.TESTING:
    #
    from pprint import pprint
    #
    maybePrint   = print
    maybePrettyP = pprint
    #
else:
    #
    def maybePrint(   *args ): pass
    def maybePrettyP( *args ): pass
    #

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
        oUser, isVisiting = self.getUserOrVisiting()
        #
        sSelect = self.kwargs.get( 'select', 'A' )
        #
        if not sSelect: sSelect = 'A'
        #
        if sSelect == 'A': # all
            qsGot = UserFinder.objects.filter(
                        iUser               = oUser,
                        bListExclude        = False,
                    ).order_by( '-iHitStars', 'iMaxModel', 'tTimeEnd' )
        #elif sSelect == 'P': # postive (non-zero hit stars)
        #    qsGot = UserFinder.objects.filter(
        #                iUser               = oUser,
        #                iHitStars__isnull   = False,
        #                bListExclude        = False,
        #            ).order_by( '-iHitStars', 'iMaxModel', 'tTimeEnd' )
        #
        elif sSelect == 'D': # "deleted" (excluded from list)
            qsGot = UserFinder.objects.filter(
                        iUser               = oUser,
                        iHitStars__isnull   = False,
                        bListExclude        = True
                    ).order_by( '-iHitStars', 'iMaxModel', 'tTimeEnd' )
        #elif sSelect == 'Z': # iHitStars = 0
        #    qsGot = UserFinder.objects.filter(
        #                iUser               = oUser,
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



class ItemFoundDetailView(
        GetUserOrVisiting, GetUserSelectionsOnPost, DetailViewGotModel ):

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
        oUser, isVisiting = self.getUserOrVisiting()
        #
        #
        qsThisItemAllHits = UserItemFound.objects.filter(
                iItemNumb_id    = context[ 'object' ].iItemNumb_id,
                iUser           = oUser,
                bListExclude    = False,
                ).order_by( '-iHitStars' )
        #
        if len( qsThisItemAllHits ) == 0:
            #
            qsThisItemAllHits = UserItemFound.objects.filter(
                iItemNumb_id    = context[ 'object' ].iItemNumb_id,
                iUser           = oUser,
                ).order_by( '-iHitStars' )
            #
        #
        sayMoreAboutHitsForThis( qsThisItemAllHits )
        #
        context['HitsForThis']  = qsThisItemAllHits
        #
        session = self.request.session
        #
        session['iItemNumb'  ]  = context[ 'object' ].iItemNumb_id
        #
        if len( qsThisItemAllHits ) == 0:
            session['iSearch']  = None
        else:
            session['iSearch']  = qsThisItemAllHits[0].iSearch_id
        #
        # cannot serialize datetime object, so covert to string
        #
        session['sTimeEnd'   ]  = getEbayStrGotDateTimeObj(
                                        context[ 'object' ].tTimeEnd )
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

    def get_initial( self ):
        #
        initial = super().get_initial()
        #
        # in testing, values might not be there
        #
        session  = self.request.session
        #
        if session and 'iItemNumb' in session:
            #
            initial['iItemNumb'] = session['iItemNumb']
            initial['iSearch'  ] = session['iSearch'  ]
            initial['tTimeEnd' ] = getDateTimeObjGotEbayStr( session['sTimeEnd' ] )
            initial['iUser'    ] = self.request.user
            #
        #
        return initial


    def troubleshoot_form_valid( self, form ):
        #
        instance = form.instance
        #session  = self.request.session
        ##
        #instance.iItemNumb_id = instance.iItemNumb_id or session['iItemNumb']
        #instance.iSearch_id   = instance.iSearch_id   or session['iSearch'  ]
        #instance.tTimeEnd     = instance.tTimeEnd     or session['tTimeEnd' ]
        #instance.iUser        = self.request.user
        #
        maybePrint( 'iItemNumb_id, iSearch_id, tTimeEnd, iUser:',
              instance.iItemNumb_id,
              instance.iSearch_id,
              instance.tTimeEnd,
              instance.iUser )
        #
        return super().form_valid( form )
