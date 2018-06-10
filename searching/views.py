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
        if not sSelect: sSelect = 'p'
        #
        if sSelect == 'A': # all
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        bListExclude        = False,
                        tRetrieved__isnull  = True,
                        iHitStars__isnull   = False ).order_by('-iHitStars')
        elif sSelect == 'P': # postive (non-zero hit stars)
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        iHitStars__isnull   = False,
                        bListExclude        = False,
                        tRetrieved__isnull  = True,
                        iHitStars__gt       = 0 ).order_by('-iHitStars')
        elif sSelect == 'D': # "deleted" (excluded from list)
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        iHitStars__isnull   = False,
                        tRetrieved__isnull  = True,
                        bListExclude        = True ).order_by('-iHitStars')
        elif sSelect == 'Z': # iHitStars = 0
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        iHitStars__eq       = 0,
                        tRetrieved__isnull  = True,
                        bListExclude        = False ).order_by('-iHitStars')
        if sSelect == 'a': # all auctions
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        bAuction            = True,
                        bListExclude        = False,
                        tRetrieved__isnull  = True,
                        iHitStars__isnull   = False ).order_by('-iHitStars')
        elif sSelect == 'p': # postive (non-zero hit stars) auctions
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        bAuction            = True,
                        iHitStars__isnull   = False,
                        bListExclude        = False,
                        tRetrieved__isnull  = True,
                        iHitStars__gt       = 0 ).order_by('-iHitStars')
        elif sSelect == 'd': # "deleted" (excluded from list) auctions
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        bAuction            = True,
                        iHitStars__isnull   = False,
                        tRetrieved__isnull  = True,
                        bListExclude        = True ).order_by('-iHitStars')
        elif sSelect == 's': # iHitStars = 0 auctions
            qsGot = UserItemFound.objects.select_related().filter(
                        iUser               = self.request.user,
                        bAuction            = True,
                        iHitStars__eq       = 0,
                        tRetrieved__isnull  = True,
                        bListExclude        = False ).order_by('-iHitStars')
        #
        return qsGot



    def post(self, request, *args, **kwargs):

        url = request.build_absolute_uri()
        #
        if "cancel" in request.POST:
            pass
        elif 'submit' in request.POST:
            #
            setDelete  = frozenset( request.POST.getlist('bListExclude') )
            setGetPics = frozenset( request.POST.getlist('bGetPictures') )
            setPicsSet = frozenset( request.POST.getlist('PicsSet'     ) )
            setExclSet = frozenset( request.POST.getlist('ExclSet'     ) )
            #
            setCommon  = setGetPics.intersection( setDelete )
            #
            if setCommon:
                #
                messages.error( request,
                        'Error! On a row, it is invalid set both '
                        'get pics and delete! Careful!' )
                #
            else:

                setNewDel  = setDelete.union( setExclSet )
                setNewPics = setGetPics.union( setPicsSet )
                #
                qsNewDel = UserItemFound.objects.filter(
                                iItemNumb_id__in = setNewDel,
                                iUser            = self.request.user )
                #
                for oItem in qsNewDel:
                    #
                    if str( oItem.iItemNumb_id ) in setDelete:
                        oItem.bListExclude = True
                    else:
                        oItem.bListExclude = False
                    oItem.save()
                    #
                #
                qsNewPics = UserItemFound.objects.filter(
                                iItemNumb_id__in = setNewPics,
                                iUser            = self.request.user )
                #
                for oItem in qsNewPics:
                    #
                    if str( oItem.iItemNumb_id ) in setGetPics:
                        oItem.bGetPictures = True
                    else:
                        oItem.bGetPictures = False
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

