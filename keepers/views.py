from django.shortcuts   import render
from django.views       import generic

from core.mixins        import ( GetPaginationExtraInfoInContext,
                                 GetUserSelectionsOnPost,
                                 TitleSearchMixin )

from core.views         import ( DeleteViewGotModel, CreateViewCanCancel,
                                 DetailViewGotModel,  ListViewGotModel )

from .forms             import KeeperForm

from .models            import Keeper, UserKeeper


# ### views assemble presentation info ###
# ###         keep views thin!         ###


class KeeperDetailView( GetUserSelectionsOnPost, DetailViewGotModel ):

    model   = Keeper
    template_name = 'keepers/detail.html'

    def get_context_data( self, **kwargs ):
        '''
        want more info to the context data.
        '''
        context = super(
                KeeperDetailView, self
                ).get_context_data( **kwargs )

        # qsThisItem = UserItemFound.objects.filter(
        #
        qsThisItemAllHits = UserKeeper.objects.filter(
                iItemNumb_id    = context[ 'object' ].iItemNumb,
                iUser           = self.request.user,
                ).order_by( '-iHitStars' )
        #
        context['HitsForThis']  = qsThisItemAllHits
        #
        return context



class KeeperIndexView(
            GetUserSelectionsOnPost,
            GetPaginationExtraInfoInContext,
            TitleSearchMixin,
            ListViewGotModel ):
    model               = Keeper
    template_name       = 'keepers/index.html'
    context_object_name = 'keeper_list'
    paginate_by         = 100

    def get_queryset(self):
        #
        oUser = self.request.user
        #
        lUserKeeperNumbs = ( UserKeeper.objects.filter(
                                iUser = oUser )
                            .values_list( 'iItemNumb', flat = True )
                            .distinct() )
        #
        qsKeepers = Keeper.objects.filter(
                            iItemNumb__in = lUserKeeperNumbs
                            ).order_by( '-tTimeEnd' )
        #
        return qsKeepers



class KeeperCreateView( CreateViewCanCancel ):

    model           = UserKeeper
    parent          = Keeper
    template_name   = 'keepers/add.html'
    success_message = 'New keeper hit successfully saved!!!!'
    form_class      = KeeperForm

    def form_valid( self, form ):
        #
        instance = form.instance
        session  = self.request.session
        #
        instance.iItemNumb_id = instance.iItemNumb_id or session['iItemNumb']
        instance.iSearch_id   = instance.iSearch_id   or session['iSearch'  ]
        instance.iUser        = self.request.user
        #
        return super( ItemFoundCreateView, self ).form_valid( form )
