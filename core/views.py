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

# ### keep views thin! ###


class ListViewGotModel(
            LoginRequiredMixin, GetModelInContextMixin, ListView ):
    '''
    Enhanced ListView which also includes the model in the context data,
    so that the template has access to its model class.
    '''

    def get_context_data( self, **kwargs ):
        '''
        Adds the pagination to the context data.
        '''
        context = super( ListView, self ).get_context_data( **kwargs )

        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        
        oThisPage = context.get('page_obj')
        iPageNumb = oThisPage.number

        iMaxPage = len(paginator.page_range)
        #
        iBeg = iPageNumb - 1 if iPageNumb > 3 else 0
        iEnd = iMaxPage if iPageNumb + 2 == iMaxPage else iPageNumb + 1
        
        iMidLeft = iMidRight = 0
        
        sPrevPage = self.request.GET.get( 'previous', None )

        # on page 1 fresh
        # (<<) (1) 2 ... iM ... iEnd >>
        #
        # on page 1 from prior page
        # (<<) (1) 2 ... iML ... iM ... iEnd >>
        #
        # on page 2
        # << 1 (2) 3 ... iM ... iEnd >>
        #
        # on page 3
        # << 1 2 (3) 4 ... iM ... iEnd >>
        #
        # on page 4
        # << 1 ... 3 (4) 5 ... iM ... iEnd >>
        #
        # mid page
        # << 1 ... iML ... i-1 (i) i+1 ... iMR ... iEnd >>
        #
        # on last -3
        # << 1 ... iML ... iM ... iMR ... iL-4 (iL-3) iL-2 ... iL >>
        #
        # on last -2
        # << 1 ... iML ... iM ... iMR ... iL-3 (iL-2) iL-1 iL >>
        #
        # on last -1
        # << 1 ... iML ... iM ... iMR ... iL-2 (iL-1) iL >>
        #
        # on last page
        # << 1 ... iML ... iM ... iMR ... iL-1 (iL) (>>)

        if sPrevPage is not None:
            #
            iPrevPage = int( sPrevPage )
            #
            iBegAvg = iPrevPage if iPrevPage < iPageNumb else 1
            iEndAvg = iPrevPage if iPrevPage > iPageNumb else iMaxPage
            #
        else:
            #
            iBegAvg = 1
            iEndAvg = iMaxPage
            #
        #
        iMidLeft    = ( ( iBegAvg   + iPageNumb ) // 2
                            if iPageNumb - 1 > 5 else 0 )
        iMidRight   = ( ( iPageNumb + iEndAvg   ) // 2
                            if iEndAvg - iPageNumb > 5 else 0 )

        iStart = iBeg - 1 if iBeg > 0 else 0
        
        show_range = paginator.page_range[ iStart : iEnd ]

        #print( 'iBeg:', iBeg )
        #print( 'iEnd:', iEnd )
        #print( 'iMidRight:', iMidRight )
        #print( 'show_range:', show_range )

        #print( 'iPageNumb', iPageNumb   )
        #print( 'iBegAvg',   iBegAvg     )
        #print( 'iEndAvg',   iEndAvg     )
        #print( 'iBeg',    iBeg      )
        #print( 'iEnd',     iEnd       )
        #print( 'iMidLeft',  iMidLeft    )
        #print( 'iMidRight', iMidRight   )

        context.update({ 'show_range' : show_range,
                         'iBeg'       : iBeg,
                         'iEnd'       : iEnd,
                         'iMidLeft'   : iMidLeft,
                         'iMidRight'  : iMidRight,
                         'iMaxPage'   : iMaxPage })
        #
        return context

    def get_queryset(self):
        return self.model.objects.filter( iUser = self.request.user )



class CreateViewCanCancel( LoginRequiredMixin, 
            SuccessMessageMixin, FormValidMixin, GetFormMixin,
            CreateView ):
    '''
    Enhanced CreateView which includes crispy form Create and Cancel buttons.
    '''

    success_message = 'New record successfully saved!!!!'


    def get_object(self):
        '''work around obscure bug, sometimes CreateView requires a pk!'''
        # https://github.com/django-guardian/django-guardian/issues/279
        return None

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

