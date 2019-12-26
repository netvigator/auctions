from django.contrib                 import messages
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.messages.views  import SuccessMessageMixin

from django.http                    import HttpResponseRedirect

from django.urls                    import reverse_lazy

from django.views.generic           import ListView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import CreateView, UpdateView, DeleteView


from .mixins                        import ( DoesLoggedInUserOwnThisRowMixin,
                                             FormValidMixin, GetFormMixin,
                                             GetModelInContextMixin,
                                             DoPostCanCancelMixin )

from .utils                         import getSaySequence

from keepers.utils                  import deleteKeeperUserItem

# ### keep views thin! ###


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
        elif 'GetOrTrash' in request.POST:
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


class ListViewGotModel(
            LoginRequiredMixin, GetModelInContextMixin, ListView ):
    '''
    Enhanced ListView which also includes the model in the context data,
    so that the template has access to its model class.
    '''

    def get_queryset(self):
        #
        queryset = self.model.objects.filter( iUser = self.request.user )
        #
        return queryset



class CreateViewCanCancel( LoginRequiredMixin,
            SuccessMessageMixin, FormValidMixin, GetFormMixin,
            CreateView ):
    '''
    Enhanced CreateView which includes crispy form Create and Cancel buttons.
    '''

    # value accessed in subclass
    success_message = 'New record successfully saved!!!!'
    # value accessed in subclass

    def get_object(self):
        '''work around obscure bug, sometimes CreateView requires a pk!'''
        # https://github.com/django-guardian/django-guardian/issues/279
        return None

    def get_form(self, form_class=None):
        form = super(CreateViewCanCancel, self).get_form(form_class)
        return form

    def post(self, request, *args, **kwargs):
        # this one is different, cannot use mixin
        if "cancel" in request.POST:
            # different URL in this one
            url = reverse_lazy( '%s:index' % self.model._meta.db_table )
            return HttpResponseRedirect(url)
        else:
            # self.object = self.get_object() # assign the object to the view
            # cannot work, see above
            return ( super( CreateViewCanCancel, self )
                     .post( request, *args, **kwargs ) )



class DeleteViewGotModel( LoginRequiredMixin, GetModelInContextMixin,
                DoesLoggedInUserOwnThisRowMixin, SuccessMessageMixin,
                DoPostCanCancelMixin,
                DeleteView ):
    '''
    Enhanced DeleteView which also includes the model in the context data,
    so that the template has access to its model class.
    '''

    success_message = 'Record successfully deleted!!!!'




class UpdateViewCanCancel(
            LoginRequiredMixin, SuccessMessageMixin, FormValidMixin,
            DoesLoggedInUserOwnThisRowMixin, GetModelInContextMixin,
            GetFormMixin, DoPostCanCancelMixin,
            UpdateView ):
    '''
    Enhanced UpdateView which includes crispy form Update and Cancel buttons.
    '''
    success_message = 'Record successfully saved!!!!'

    def get_form_kwargs(self):
        kwargs = super( UpdateViewCanCancel, self ).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs




class DetailViewGotModel( LoginRequiredMixin,
                DoesLoggedInUserOwnThisRowMixin, GetModelInContextMixin,
                DetailView ):
    '''
    Enhanced DetailView which also includes the model in the context data,
    so that the template has access to its model class.
    '''

    pass



class DetailViewGotModelAlsoPost(
            SuccessMessageMixin,
            GetUserSelectionsOnPost,
            DetailViewGotModel ):

    '''detail view for Brands, Categories & Models shows Keepers & Finders'''


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(
            DetailViewGotModelAlsoPost, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the categories
        #
        oUser = self.request.user
        #
        t = self.object.getKeeperContextForThis( self.object, oUser )
        #
        sHowManyKeepers, oKeeperItems   = t
        #
        context['keepers_list']         = oKeeperItems
        context['sHowManyKeepers']      = sHowManyKeepers
        #
        t = self.object.getFinderContextForThis( self.object, oUser )
        #
        sHowManyFinders, oFinderItems   = t
        #
        context['finders_list']         = oFinderItems
        context['sHowManyFinders']      = sHowManyFinders
        #
        return context



