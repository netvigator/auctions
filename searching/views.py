from core.views     import ( CreateViewCanCancel, DeleteViewGotModel,
                             DetailViewGotModel,  ListViewGotModel,
                             UpdateViewCanCancel )

from django.contrib import messages
from django.http    import HttpResponseRedirect
from django.urls    import reverse_lazy

from django.core.urlresolvers   import reverse

from .forms         import ( ItemFoundForm, UserItemFoundForm,
                             CreateSearchForm, UpdateSearchForm )

import searching.utils

from .mixins        import ( SearchViewSuccessPostFormValidMixin,
                             AnyReleventHitStarColsChangedMixin )
from .models        import Search, ItemFound, UserItemFound
from .utils         import getHowManySearchDigitsNeeded

from core.mixins    import GetPaginationExtraInfoInContext

from models.models  import Model

# ### keep views thin! ###



class SearchCreateView( SearchViewSuccessPostFormValidMixin, CreateViewCanCancel ):

    model           = Search
    template_name   = 'searching/add.html'
    success_message = 'New Search record successfully saved!!!!'
    form_class      = CreateSearchForm

    success_message = 'New Search record successfully saved!!!!'


class SearchIndexView( ListViewGotModel ):

    template_name   = 'searching/index.html'
    model           = Search


class SearchDetailView( DetailViewGotModel ):

    model           = Search
    template_name   = 'searching/detail.html'


class SearchDeleteView( DeleteViewGotModel ):

    model           = Search
    template_name   = 'confirm_delete.html'
    success_message = 'Search record successfully deleted!!!!'
    success_url     = reverse_lazy('searching:index')



class SearchUpdateView( SearchViewSuccessPostFormValidMixin, UpdateViewCanCancel ):

    model           = Search
    template_name   = 'searching/edit.html'
    success_message = 'Search record update successfully saved!!!!'
    form_class      = UpdateSearchForm

    success_message = 'Search record successfully updated!!!!'




class ItemsFoundIndexView(
            GetPaginationExtraInfoInContext, ListViewGotModel ):

    template_name       = 'searching/items_found_index.html'
    model               = UserItemFound
    context_object_name = 'items_found_list'
    paginate_by         = 100
    #form_class          = ItemsFoundIndexForm

    def get_queryset(self):
        #
        # ADPZ
        # qs = super( ItemsFoundIndexView, self ).get_queryset()
        #sSelect = 'P'
        #
        sSelect = self.kwargs.get('select', 'p' )
        #
        if not sSelect: sSelect = 'p' # change to P after non auctions are flushed
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
                        iHitStars__eq       = 0,
                        tRetrieved__isnull  = True,
                        bListExclude        = False
                    ).order_by( '-iHitStars', 'iModel', 'tCreate' )
        if sSelect == 'a': # all auctions
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        bAuction            = True,
                        bListExclude        = False,
                        tRetrieved__isnull  = True,
                        iHitStars__isnull   = False
                    ).order_by( '-iHitStars', 'iModel', 'tCreate' )
        elif sSelect == 'p': # postive (non-zero hit stars) auctions
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        bAuction            = True,
                        iHitStars__isnull   = False,
                        bListExclude        = False,
                        tRetrieved__isnull  = True,
                        iHitStars__gt       = 0
                    ).order_by( '-iHitStars', 'iModel', 'tCreate' )
        elif sSelect == 'd': # "deleted" (excluded from list) auctions
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        bAuction            = True,
                        iHitStars__isnull   = False,
                        tRetrieved__isnull  = True,
                        bListExclude        = True
                    ).order_by( '-iHitStars', 'iModel', 'tCreate' )
        elif sSelect == 's': # iHitStars = 0 auctions
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        bAuction            = True,
                        iHitStars__eq       = 0,
                        tRetrieved__isnull  = True,
                        bListExclude        = False
                    ).order_by( '-iHitStars', 'iModel', 'tCreate' )
        #
        return qsGot



    def post(self, request, *args, **kwargs):

        url = request.build_absolute_uri()
        #
        if "selectall" in request.POST:
            #
            lPageItems = request.POST.getlist('AllItems')
            #
            qsChanged  = UserItemFound.objects.filter(
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
            setExclude = frozenset( request.POST.getlist('bListExclude') )
            # check box end user can change
            setGetPics = frozenset( request.POST.getlist('bGetPictures') )
            # check box end user can change
            setPicsSet = frozenset( request.POST.getlist('PicsSet'     ) )
            # hidden set if item has bGetPictures as True when page composed
            setExclSet = frozenset( request.POST.getlist('ExclSet'     ) )
            # hidden set if item has bListExclude as True when page composed
            #
            setCommon  = setGetPics.intersection( setExclude )
            #
            if setCommon:
                #
                messages.error( request,
                        'Error! On a row, it is invalid set both '
                        'get pics and delete! Careful!' )
                #
            else:
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
                qsChanged  = UserItemFound.objects.filter(
                                iItemNumb_id__in = setChanged,
                                iUser            = self.request.user )
                #
                for oItem in qsChanged:
                    #
                    sItemNumb = str( oItem.iItemNumb_id )
                    #
                    if sItemNumb in setGetPics:
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
            #
        return HttpResponseRedirect( url )



class ItemFoundDetailView( DetailViewGotModel ):

    model           = UserItemFound
    parent          = ItemFound
    template_name   = 'searching/item_found_detail.html'
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
         'view': <searching.views.ItemFoundDetailView object at 0x7f0669fa63c8>,
         'model': <class 'searching.models.UserItemFound'>,\
         'parent': <class 'searching.models.ItemFound'>}
        '''
        #
        qsThisItemAllHits = UserItemFound.objects.filter(
                iItemNumb_id = context[ 'object' ].iItemNumb_id,
                iUser        = context[ 'object' ].iUser )
        #
        qsThisItemOtherHits = qsThisItemAllHits.difference(
                UserItemFound.objects.filter( id = context[ 'object' ].id ) )
        #
        if qsThisItemOtherHits:
            #
            sTableTemplate = '<table RULES=ROWS>%s</table>'
            #
            sRowTemplate = (
                '<TR>'
                '<TD VALIGN=TOP>%s</TD>'
                '<TD VALIGN=TOP>%s</TD>'
                '<TD VALIGN=TOP>%s</TD>'
                '<TD VALIGN=TOP>%s%s</TD>'
                '</TR>' )
            #
            sHeader = ( sRowTemplate %
                        ( 'Model', 'Brand', 'Category', 'HitStars', '' ) )
            #
            lRows = [ sHeader ]
            #
            for o in qsThisItemOtherHits:
                #
                sayStarsModel   = o.iModel.iStars    or 'no model found'
                sayStarsBrand   = o.iBrand.iStars    or 'no brand found'
                sayStarsCategory= o.iCategory.iStars or 'no category found'
                #
                tStars = ( sayStarsModel, sayStarsBrand, sayStarsCategory )
                #
                sDetail = ' ( %s * %s * %s )' % tStars
                #
                lRows.append( sRowTemplate %
                        ( o.iModel, o.iBrand, o.iCategory, o.iHitStars, sDetail ) )
                #
            #
            sThisItemOtherHits = sTableTemplate % '\n'.join( lRows )
            #
        else:
            #
            sThisItemOtherHits = 'None'
            #
        #
        context['OtherHits'] = sThisItemOtherHits
        #
        return context


class ItemFoundUpdateView(
            AnyReleventHitStarColsChangedMixin, UpdateViewCanCancel ):

    model           = UserItemFound
    parent          = ItemFound
    template_name   = 'searching/item_found_edit.html'
    success_message = 'Item Found record update successfully saved!!!!'
    form_class      = UserItemFoundForm

    tHitStarRelevantCols = (
        'iModel',
        'iBrand',
        'iCategory' )

