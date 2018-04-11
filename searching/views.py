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

from pprint import pprint

# ### keep views thin! ###

tModelFields = (
    'cTitle',
    'cKeyWords',
    'iDummyCategory',
    'cPriority', )


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



def _getTableBoolSetTrue( sChangeBoolField, sIdField, lIDsToChange ):
    #
    for iID in lIDsToChange:
        pass
    

class ItemsFoundIndexView( ListViewGotModel ):

    template_name       = 'searching/items_found_index.html'
    model               = UserItemFound
    context_object_name = 'items_found_list'
    paginate_by         = 100
    #form_class          = ItemsFoundIndexForm

    def get_queryset(self):
        # ADPZ
        qs = super( ItemsFoundIndexView, self ).get_queryset()
        #
        sSelect = self.kwargs['select']
        #
        if sSelect == 'A': # all
            qsGot = qs.filter(
                        bListExclude = False,
                        iHitStars__isnull = False ).order_by('-iHitStars')
        elif sSelect == 'P': # postive (non-zero hit stars)
            qsGot = qs.filter(
                        iHitStars__isnull = False,
                        bListExclude = False,
                        iHitStars__gt = 0 ).order_by('-iHitStars')
        elif sSelect == 'D': # "deleted" (excluded from list)
            qsGot = qs.filter(
                        iHitStars__isnull = False,
                        bListExclude = True ).order_by('-iHitStars')
        elif sSelect == 'Z': # iHitStars = 0
            qsGot = qs.filter(
                        iHitStars__eq = 0,
                        bListExclude =  False).order_by('-iHitStars')
        #
        self.queryset = qsGot
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

                setNewDel  = setDelete.difference( setExclSet )
                setNewPics = setGetPics.difference( setPicsSet )
                #
                qsNewDel = UserItemFound.objects.filter(
                                                pk__in = tuple( setNewDel ) )
                #
                for oItem in qsNewDel:
                    #
                    oItem.bListExclude = True
                    oItem.save()
                    #
                #
                qsNewPics = UserItemFound.objects.filter(
                                                pk__in = tuple( setNewPics ) )
                #
                for oItem in qsNewPics:
                    #
                    print( 'saving:', oItem.iItemNumb_id )
                    oItem.bGetPictures = True
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

